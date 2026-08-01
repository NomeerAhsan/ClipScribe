from bs4 import BeautifulSoup, NavigableString, Tag


def parse_html_fragment(html: str) -> BeautifulSoup:
    wrapped = f"<div class='clipscribe-root'>{html}</div>"
    return BeautifulSoup(wrapped, "lxml")


def extract_plain_text(html: str) -> str:
    soup = parse_html_fragment(html)
    root = soup.select_one(".clipscribe-root")
    if root is None:
        return ""
    return root.get_text("\n", strip=True)
