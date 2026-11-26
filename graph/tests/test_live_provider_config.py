import io
import json
import sys
from types import SimpleNamespace

import pytest

from loop import implement

discover = implement.discover


@pytest.fixture(autouse=True)
def isolate_provider_calls(monkeypatch, tmp_path):
    def unexpected_call(*args, **kwargs):
        pytest.fail("Attempted an external call without a test stub")

    monkeypatch.delenv("ANY_LIVE_BACKENDS", raising=False)
    monkeypatch.setattr(discover, "PROJECT", "")
    monkeypatch.setattr(discover, "AGY", False)
    monkeypatch.setattr(discover, "SPEND_FILE", tmp_path / "spend.json")
    monkeypatch.setattr(discover, "CACHE", {})
    monkeypatch.setattr(discover.subprocess, "run", unexpected_call)
    monkeypatch.setattr(discover.urllib.request, "urlopen", unexpected_call)


@pytest.mark.parametrize(
    "invoke, backend",
    [
        (lambda: discover.argon("prompt", 1, "propose"), "vertex"),
        (lambda: discover.open_cache("prompt"), "vertex"),
        (lambda: discover.agy_call("prompt", 1, "propose", discover.FLASH), "agy"),
        (lambda: discover.gpt("prompt", 1, "audit"), "codex"),
    ],
)
def test_live_providers_are_disabled_by_default(invoke, backend):
    with pytest.raises(SystemExit, match=f"Live backend {backend} is disabled"):
        invoke()


def test_vertex_requires_project_and_budget_before_authentication(monkeypatch):
    monkeypatch.setenv("ANY_LIVE_BACKENDS", "vertex")
    with pytest.raises(SystemExit, match="ANY_VERTEX_PROJECT"):
        discover.argon("prompt", 1, "propose")
    monkeypatch.setattr(discover, "PROJECT", "operator-test-project")
    with pytest.raises(SystemExit, match="Create a valid loop/spend.json"):
        discover.argon("prompt", 1, "propose")
    discover.SPEND_FILE.write_text('{"cap_usd": 10, "spent_usd": 10}')
    with pytest.raises(SystemExit, match="SPEND CAP"):
        discover.argon("prompt", 1, "propose")


def test_vertex_stop_switch_does_not_start_antigravity(monkeypatch):
    monkeypatch.setenv("ANY_LIVE_BACKENDS", "vertex,agy")
    monkeypatch.setattr(discover, "PROJECT", "operator-test-project")
    monkeypatch.setattr(sys, "argv", ["discover.py"])
    discover.SPEND_FILE.write_text('{"cap_usd": 10, "spent_usd": 0, "vertex_disabled": true}')
    with pytest.raises(SystemExit, match="Vertex is disabled"):
        discover.main()
    with pytest.raises(SystemExit, match="Vertex is disabled"):
        discover.argon("prompt", 1, "propose")


def test_disabling_vertex_stops_a_pending_retry(monkeypatch):
    def retryable_error(request, **kwargs):
        discover.SPEND_FILE.write_text('{"cap_usd": 10, "spent_usd": 0, "vertex_disabled": true}')
        raise discover.urllib.error.HTTPError(request.full_url, 503, "try again", {}, None)

    monkeypatch.setenv("ANY_LIVE_BACKENDS", "vertex")
    monkeypatch.setattr(discover, "PROJECT", "operator-test-project")
    monkeypatch.setattr(discover.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(discover.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout="mock-token"))
    monkeypatch.setattr(discover.urllib.request, "urlopen", retryable_error)
    discover.SPEND_FILE.write_text('{"cap_usd": 10, "spent_usd": 0}')
    with pytest.raises(SystemExit, match="Vertex is disabled"):
        discover.argon("prompt", 1, "propose")


def test_vertex_uses_the_same_explicit_resource_and_quota_project(monkeypatch):
    project = "operator-test-project"
    resource = f"projects/{project}/locations/global/cachedContents/example"
    requests = []

    def vertex_response(request, **kwargs):
        requests.append(request)
        if request.get_method() == "DELETE":
            return io.BytesIO()
        if request.full_url.endswith("/cachedContents"):
            return io.BytesIO(json.dumps({"name": resource}).encode())
        return io.BytesIO(b'{"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}')

    monkeypatch.setenv("ANY_LIVE_BACKENDS", "vertex")
    monkeypatch.setattr(discover, "PROJECT", project)
    monkeypatch.setattr(discover, "log", lambda entry: None)
    monkeypatch.setattr(discover.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(stdout="mock-token"))
    monkeypatch.setattr(discover.urllib.request, "urlopen", vertex_response)
    discover.SPEND_FILE.write_text('{"cap_usd": 10, "spent_usd": 0}')

    discover.open_cache("prompt")
    assert discover.argon("prompt", 1, "propose") == "ok"
    discover.close_cache()

    assert [request.get_method() for request in requests] == ["POST", "POST", "DELETE"]
    for request in requests:
        assert request.full_url.startswith(f"https://aiplatform.googleapis.com/v1/projects/{project}/")
        assert dict(request.header_items())["X-goog-user-project"] == project


def test_implementation_does_not_switch_providers_on_missing_codex_output(monkeypatch, tmp_path):
    monkeypatch.setenv("ANY_LIVE_BACKENDS", "codex")
    monkeypatch.setattr(sys, "argv", ["implement.py", "26", "--gpt"])
    monkeypatch.setattr(implement, "LOOP", tmp_path)
    current_round = tmp_path / "rounds" / "026"
    current_round.mkdir(parents=True)
    (current_round / "meta.json").write_text('{"section": 500}')
    (current_round / "04_revise.md").write_text("## §500 Example", encoding="utf-8")
    (current_round / "claims.json").write_text("[]")
    template = tmp_path / "template.py"
    template.touch()
    monkeypatch.setattr(implement, "TEMPLATE", template)
    monkeypatch.setattr(implement, "TEST_TEMPLATE", template)
    monkeypatch.setattr(discover, "gpt", lambda *args: None)

    with pytest.raises(SystemExit, match="Codex returned no implementation"):
        implement.main()
    assert not (current_round / "05_implement_raw.md").exists()
