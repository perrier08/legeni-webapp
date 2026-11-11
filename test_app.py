from app import app


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_shows_version(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "1.0.42")
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert "Version 1.0.42" in response.get_data(as_text=True)


def test_index_uses_color(monkeypatch):
    monkeypatch.setenv("APP_COLOR", "#2da44e")
    response = app.test_client().get("/")
    assert "#2da44e" in response.get_data(as_text=True)
