from html.parser import HTMLParser
from pathlib import Path

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.lang = False
        self.css = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.h1 += 1
        if tag == "html": self.lang = attrs.get("lang") == "ru"
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.css.append(attrs.get("href", ""))

source = Path("index.html").read_text(encoding="utf-8")
parser = SiteParser()
parser.feed(source)
assert "<!doctype html>" in source.lower(), "Missing HTML5 doctype"
assert parser.lang, "Missing Russian document language"
assert parser.h1 == 1, "Expected one main heading"
assert "<title>" in source and "</title>" in source, "Missing page title"
assert parser.css, "Missing external stylesheet"
for name in parser.css:
    assert Path(name).is_file(), f"Missing stylesheet: {name}"
    assert Path(name).stat().st_size > 0, f"Empty stylesheet: {name}"
print("PASS: document metadata, main heading and linked stylesheets")
