from config.settings import BASE_DIR, DATA_DIR, DOWNLOADS_DIR, CHROMA_DIR


def test_paths_are_defined() -> None:
    assert BASE_DIR.exists()
    assert DATA_DIR.exists()
    assert DOWNLOADS_DIR.exists()
    assert CHROMA_DIR.exists()
