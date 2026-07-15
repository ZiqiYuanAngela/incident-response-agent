def test_app_imports_without_openai_client():
    from app.main import app

    assert app is not None
