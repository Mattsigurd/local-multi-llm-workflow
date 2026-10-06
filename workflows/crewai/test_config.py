from workflows.crewai.config import is_endpoint_available


def test_remote_endpoint_is_not_used_by_default() -> None:
    assert is_endpoint_available("https://example.com") is False