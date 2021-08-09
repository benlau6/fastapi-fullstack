from conftest import (
    test_database_url,
    test_root_path,
    test_api_root_str,
)

def test_settings(settings):
    assert settings.DATABASE_URL == test_database_url
    assert settings.ROOT_STR == test_api_root_str
    assert settings.FILE_ROOT_PATH == test_root_path