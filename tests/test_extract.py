"""HTML extraction tests."""

from seeklet.extract import extract_content


def test_extract_content_returns_title_text_and_links() -> None:
    """HTML extraction should keep visible text and normalized links."""
    html = """
    <html>
      <head>
        <title> Example Page </title>
        <style>.hidden { display: none; }</style>
        <script>console.log("ignore me");</script>
      </head>
      <body>
        <h1>Hello</h1>
        <p>Welcome to Seeklet.</p>
        <a href="/docs/start">Start</a>
        <a href="https://example.com/docs/start#intro">Duplicate</a>
        <a href="mailto:test@example.com">Email</a>
      </body>
    </html>
    """

    content = extract_content(html, "https://example.com/")

    assert content.title == "Example Page"
    assert content.text == "Hello Welcome to Seeklet. Start Duplicate Email"
    assert content.links == ["https://example.com/docs/start"]
