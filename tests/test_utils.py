from backend.utils import duplicate_key, normalize_text


def test_normalize_text_collapses_whitespace():
    html = "<p>  Hello   <strong>world</strong>  </p>"
    assert normalize_text(html) == "hello world"


def test_duplicate_key_is_stable():
    html = "<p>Sample text</p>"
    url = "https://example.com/article"
    assert duplicate_key(url, html) == duplicate_key(url, html)


def test_duplicate_key_changes_with_url():
    html = "<p>Sample text</p>"
    assert duplicate_key("https://example.com/a", html) != duplicate_key(
        "https://example.com/b", html
    )
