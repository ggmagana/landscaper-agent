from landscaper.i18n import detect_language


def test_language_detection():
    assert detect_language("Hola, necesito césped para mi patio") == "es"
    assert detect_language("Hello I need sod for my yard") == "en"
    assert detect_language("") == "en"
