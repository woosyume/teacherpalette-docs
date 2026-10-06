#!/usr/bin/env python3
"""Check resource metadata, links, media, sitemap and existing static pages."""
import argparse
import json
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import urlopen
from xml.etree import ElementTree as ET

from build_resources import ARTICLES, LOCALES, ORIGIN, ROOT, path


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements, self.schemas, self.ids = [], [], []
        self.schema = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.schema = ""

    def handle_data(self, data):
        if self.schema is not None:
            self.schema += data

    def handle_endtag(self, tag):
        if tag == "script" and self.schema is not None:
            self.schemas.append(json.loads(self.schema))
            self.schema = None

    def find(self, tag, **attrs):
        return [a for t, a in self.elements if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def file_for(url):
    filename = ROOT / unquote(urlsplit(url).path).lstrip("/")
    return filename / "index.html" if filename.is_dir() else filename


def check_links(filename, parsed, pages):
    failures = []
    base = ORIGIN + "/" + str(filename.relative_to(ROOT))
    for tag, attrs in parsed.elements:
        for key in ("href", "src", "poster"):
            value = attrs.get(key)
            if not value:
                continue
            url = urlsplit(urljoin(base, value))
            if url.scheme not in ("https", "http") or url.netloc != "teacherpalette.com":
                continue
            target = file_for(url.geturl())
            if not target.is_file():
                failures.append(f"{filename.relative_to(ROOT)}: missing {value}")
            elif url.fragment and target.suffix == ".html":
                if target not in pages:
                    pages[target] = Page(target.read_text())
                if unquote(url.fragment) not in pages[target].ids:
                    failures.append(f"{filename.relative_to(ROOT)}: missing fragment {value}")
    return failures


def sitemap_urls(source):
    return {e.text for e in ET.fromstring(source).iter() if e.tag.endswith("}loc")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", help="Also check generated HTTP routes, e.g. http://127.0.0.1:8765")
    args = parser.parse_args()
    subprocess.run(["python3", str(ROOT / "scripts/build_resources.py"), "--check"], check=True)
    pages = {p: Page(p.read_text()) for p in ROOT.rglob("index.html") if "resources/content" not in str(p)}
    generated = [path(locale) for locale in LOCALES] + [path(locale, a["id"]) for a in ARTICLES for locale in a["locales"]]
    sitemap = sitemap_urls((ROOT / "sitemap.xml").read_text())
    errors = []
    titles, descriptions = [], []
    # Every pre-existing sitemap URL and HTML page remains reachable.
    original = subprocess.check_output(["git", "show", "HEAD:sitemap.xml"], cwd=ROOT, text=True)
    assert sitemap_urls(original) <= sitemap, "Existing sitemap URLs removed"
    for url in sitemap:
        assert file_for(url).is_file(), f"Missing sitemap destination: {url}"
    for url in generated:
        filename = file_for(url)
        page = pages[filename]
        canonical = page.find("link", rel="canonical")
        assert len(canonical) == 1 and canonical[0]["href"] == ORIGIN + url, url
        assert len(page.find("h1")) == 1 and len(page.ids) == len(set(page.ids)), url
        assert page.find("meta", property="og:url")[0]["content"] == ORIGIN + url, url
        description = page.find("meta", name="description")[0]["content"]
        assert page.find("meta", property="og:description")[0]["content"] == description, url
        assert page.find("meta", name="twitter:description")[0]["content"] == description, url
        assert ORIGIN + url in sitemap and page.schemas, url
        for tag, attrs in page.elements:
            if tag == "a" and "apps.apple.com" in attrs.get("href", ""):
                assert "id6783567350" in attrs["href"] and "teacherpalette/id" in attrs["href"], url
            if tag == "video":
                assert attrs.get("preload") == "none" and "controls" in attrs and "playsinline" in attrs and "autoplay" not in attrs, url
        alternates = page.find("link", rel="alternate")
        if url.count("/") > 3:  # Article equivalents must actually be published in that language.
            article = next(a for a in ARTICLES if a["id"] == url.rstrip("/").split("/")[-1])
            expected = set(article["locales"]) | ({"x-default"} if "en" in article["locales"] else set())
            assert {a["hreflang"] for a in alternates} == expected, url
            schema_article = next(s for s in page.schemas[0]["@graph"] if s["@type"] == "Article")
            assert not any(k in schema_article for k in ("aggregateRating", "review", "author")), url
        descriptions.append(description)
        titles.append(page.find("meta", property="og:title")[0]["content"])
        if args.base_url:
            with urlopen(args.base_url.rstrip("/") + url) as response:
                assert response.status == 200 and response.read().decode() == filename.read_text(), url
    assert len(set(titles)) == len(titles) and len(set(descriptions)) == len(descriptions), "Duplicate resource metadata"
    for filename, page in list(pages.items()):
        errors.extend(check_links(filename, page, pages))
    # Distinguish pre-existing link errors instead of silently changing unrelated content.
    baseline_errors = set()
    for filename in pages:
        relative = str(filename.relative_to(ROOT))
        original = subprocess.run(["git", "show", "HEAD:" + relative], cwd=ROOT, text=True, capture_output=True)
        if original.returncode == 0:
            baseline_errors.update(check_links(filename, Page(original.stdout), pages))
    introduced = set(errors) - baseline_errors
    assert not introduced, "New broken internal links:\n" + "\n".join(sorted(introduced))
    robots = (ROOT / "robots.txt").read_text()
    assert "Allow: /" in robots and "Disallow: /en/resources" not in robots
    print(f"Verified {len(generated)} resources: unique SEO metadata, schemas, CTA IDs, media and sitemap.")
    print(f"Checked links and assets across {len(pages)} static HTML pages: {len(introduced)} new broken links.")
    print(f"Pre-existing broken links: {len(set(errors) & baseline_errors)}.")
    print(f"Sitemap: {len(sitemap)} valid destinations; all original URLs preserved. HTTP: {'passed' if args.base_url else 'not requested'}.")


if __name__ == "__main__":
    main()
