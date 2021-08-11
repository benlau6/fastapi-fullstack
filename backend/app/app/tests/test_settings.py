from conftest import (
    test_mongo_db_name,
    test_file_root_path,
    test_api_root_str,
)

def test_settings(settings):
    assert settings.MONGO_DB_NAME == test_mongo_db_name
    assert settings.ROOT_STR == test_api_root_str
    assert settings.FILE_ROOT_PATH == test_file_root_path