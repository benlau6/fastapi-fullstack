def test_settings(settings):
    assert settings.DATABASE_URL == 'sqlite:///data/fastapi/test.db'
    assert settings.ROOT_STR == ''
    assert settings.FILE_ROOT_PATH == '/data/fastapi'