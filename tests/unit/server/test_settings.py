def test_server_settings_parsing(monkeypatch):
    monkeypatch.setenv("SEEKMEM_SERVER_AUTH_ENABLED", "false")
    monkeypatch.setenv("SEEKMEM_SERVER_LOG_FILE", "")
    monkeypatch.setenv("SEEKMEM_SERVER_API_KEYS", " a, b ,, c ")
    monkeypatch.setenv(
        "SEEKMEM_SERVER_CORS_ORIGINS", "https://a.example, https://b.example"
    )
    monkeypatch.setenv("SEEKMEM_SERVER_RELOAD", "enabled")

    from server.config import ServerSettings

    settings = ServerSettings(_env_file=None)

    assert settings.auth_enabled is False
    assert settings.log_file is None
    assert settings.get_api_keys_list() == ["a", "b", "c"]
    assert settings.get_cors_origins_list() == [
        "https://a.example",
        "https://b.example",
    ]
