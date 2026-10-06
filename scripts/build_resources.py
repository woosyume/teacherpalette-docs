#!/usr/bin/env python3
"""Build crawlable resource HTML with the Python standard library only.

Run from any directory: python3 scripts/build_resources.py [--check]
Generated pages are committed, so the existing static host needs no build step.
"""
import argparse
import html
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "resources/content"
ORIGIN = "https://teacherpalette.com"
LOCALES = json.loads((SOURCE / "locales.json").read_text())
ARTICLES = json.loads((SOURCE / "articles.json").read_text())["articles"]
TEMPLATE = (ROOT / "resources/templates/page.html").read_text()
LABELS = {**{code: data["label"] for code, data in LOCALES.items()}, "zh": "资源（英语）",
          "fr": "Ressources (anglais)", "de": "Ressourcen (Englisch)",
          "es": "Recursos (inglés)", "pt": "Recursos (inglês)", "it": "Risorse (inglese)"}


def esc(value):
    return html.escape(str(value), quote=True)


def plain(value):
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def path(locale, slug=None):
    return f"/{locale}/resources/" + (f"{slug}/" if slug else "")


def render(template, values):
    result = re.sub(r"\{\{(\w+)\}\}", lambda m: str(values[m[1]]), template)
    if "{{" in result:
        raise ValueError("Unresolved template placeholder")
    return result


def translated_articles(locale):
    return [a for a in ARTICLES if locale in a["locales"]]


def article_alternates(article):
    # Preserve the existing localized screen guides when consolidating their EN variant.
    return {**article.get("localeAlternates", {}),
            **{code: path(code, article["id"]) for code in article["locales"]}}


def article_card(article, locale):
    data = article["locales"][locale]
    return card(path(locale, article["id"]), data["title"], data["summary"],
                LOCALES[locale]["categories"][article["category"]], LOCALES[locale]["read"])


def card(url, title, summary, category, read):
    return f'''<a class="resource-card" href="{esc(url)}">
  <span class="resource-category">{esc(category)}</span>
  <h3>{esc(title)}</h3><p>{esc(summary)}</p>
  <span class="resource-read">{esc(read)} <span aria-hidden="true">→</span></span>
</a>'''


def legacy_cards(locale):
    # Existing localized pages remain the source of truth for their own metadata.
    result = []
    for slug in LOCALES[locale]["legacyPaths"]:
        url = f"/{locale}/{slug}/"
        source = (ROOT / url.lstrip("/") / "index.html").read_text()
        title = plain(re.search(r"<h1[^>]*>(.*?)</h1>", source, re.S)[1])
        description = html.unescape(re.search(r'<meta name="description" content="([^"]+)"', source)[1])
        result.append((url, card(url, title, description, LOCALES[locale]["categories"]["guides"], LOCALES[locale]["read"])))
    return result


def spans(values):
    return "".join(f'<span data-lang-{locale}>{esc(text)}</span>' for locale, text in values.items())


def libraries(locale, article=None):
    links = []
    for code, data in LOCALES.items():
        current = ' aria-current="page"' if code == locale and not article else ""
        links.append(f'<a href="{path(code)}" lang="{code}" hreflang="{code}"{current}>{data["name"]}</a>')
    result = f'<nav class="resource-languages" aria-label="{esc(LOCALES[locale]["libraries"])}"><span>{esc(LOCALES[locale]["libraries"])}</span>{"".join(links)}</nav>'
    if article and len(article["locales"]) > 1:
        label = LOCALES[locale]["articleLanguages"]
        article_links = "".join(
            f'<a href="{path(code, article["id"])}" lang="{code}" hreflang="{code}"' +
            (' aria-current="page"' if code == locale else '') + f'>{LOCALES[code]["name"]}</a>'
            for code in article["locales"])
        result += f'<nav class="resource-languages" aria-label="{esc(label)}"><span>{esc(label)}</span>{article_links}</nav>'
    return result


def chrome(locale, article=False):
    l = LOCALES[locale]
    header = f'''<header><div class="header-inner">
  <a class="brand" href="/?lang={locale}" aria-label="TeacherPalette — {esc(l['home'])}"><img class="brand-icon" src="/img/icon-256.png" width="32" height="32" alt=""><img class="brand-logo" src="/img/teacherpalette-title.png" width="123" height="22" alt="TeacherPalette"></a>
  <button class="resource-menu-toggle" type="button" data-resource-menu aria-expanded="false" aria-controls="resource-menu">{esc(l['menu'])} <span aria-hidden="true">⌄</span></button>
  <nav class="resource-nav" id="resource-menu" aria-label="{esc(l['menu'])}">
    <a class="header-link" href="/releases/index.html?lang={locale}">{esc(l['new'])}</a>
    <a class="header-link" href="/faq/index.html?lang={locale}">{esc(l['help'])}</a>
    <a class="header-link" href="{path(locale)}" aria-current="{'true' if article else 'page'}">{esc(l['label'])}</a>
    <a class="header-link" href="/?lang={locale}#pricing">{esc(l['pricing'])}</a>
    <button class="resource-theme" type="button" data-resource-theme aria-label="{esc(l['theme'])}">☾</button>
  </nav>
</div></header>'''
    footer_links = [(f"/?lang={locale}#features", "TeacherPalette"), (path(locale), l["label"]),
                    (f"/faq/index.html?lang={locale}", l["help"]),
                    (f"/?lang={locale}#privacy", l["privacy"]), (f"/?lang={locale}#terms", l["terms"]),
                    (f"/?lang={locale}#support", l["support"])]
    footer = f'<footer class="resource-footer"><nav aria-label="{esc(l["footer"])}">' + "".join(
        f'<a href="{esc(url)}">{esc(label)}</a>' for url, label in footer_links) + '</nav><p>© 2026 TeacherPalette</p></footer>'
    return header, footer


def page(locale, title, description, url, content, available, schema, article=False):
    header, footer = chrome(locale, article)
    alternates = "\n".join(f'  <link rel="alternate" hreflang="{code}" href="{ORIGIN + translated}">' for code, translated in available.items())
    if "en" in available:
        alternates += f'\n  <link rel="alternate" hreflang="x-default" href="{ORIGIN + available["en"]}">'
    return render(TEMPLATE, {
        "locale": locale, "title": esc(title + " | TeacherPalette"), "description": esc(description),
        "canonical": ORIGIN + url, "og_type": "article" if article else "website", "alternates": alternates,
        "schema": json.dumps(schema, ensure_ascii=False).replace("<", "\\u003c"),
        "header": header, "footer": footer, "content": content, "skip": esc(LOCALES[locale]["skip"])
    })


def cta(store, locale, middle=False):
    l = LOCALES[locale]
    if middle:
        return f'<aside class="resource-mid-cta"><p><strong>{esc(l["midCta"])}</strong></p><a class="resource-button resource-button-primary" href="{esc(store)}">{esc(l["trial"])}</a></aside>'
    return f'''<aside class="resource-end-cta" aria-label="{esc(l['trial'])}">
  <h2>{esc(l['ctaHeading'])}</h2>
  <p>{esc(l['ctaBody'])}</p>
  <a class="resource-button resource-button-primary" href="{esc(store)}">{esc(l['trial'])}</a>
  <p class="resource-trial-note">{esc(l['trialNote'])} <a href="/?lang={locale}#terms">{esc(l['subscriptionTerms'])}</a>.</p>
</aside>'''


def build_article(article, locale, store):
    data = article["locales"][locale]
    l = LOCALES[locale]
    body = (SOURCE / data["body"]).read_text().replace("{{mid_cta}}", cta(store, locale, True))
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body, re.S)
    if not headings or len({h[0] for h in headings}) != len(headings):
        raise ValueError(f"Article {article['id']} needs unique H2 IDs")
    toc = f'<nav class="resource-toc" aria-label="{esc(l["toc"])}"><h2>{esc(l["toc"])}</h2><ul>' + "".join(
        f'<li><a href="#{esc(anchor)}">{esc(plain(heading))}</a></li>' for anchor, heading in headings) + '</ul></nav>'
    demo = data["demo"]
    for asset in (demo["video"], demo["poster"]):
        if not (ROOT / "media" / asset).is_file():
            raise ValueError(f"Missing demo asset: {asset}")
    video = f'''<figure id="demo" class="resource-demo">
  <video controls playsinline preload="none" poster="/media/{esc(demo['poster'])}" aria-label="{esc(plain(data['heading']))} — {esc(l['watch'])}">
    <source src="/media/{esc(demo['video'])}" type="video/mp4">
    <p><a href="/media/{esc(demo['video'])}">{esc(l['watch'])}</a></p>
  </video><figcaption>{esc(demo['caption'])}</figcaption>
</figure>'''
    related = []
    for slug in article["related"]:
        target = next(a for a in ARTICLES if a["id"] == slug)
        if locale in target["locales"]:
            related.append(article_card(target, locale))
    if not related:
        # No translated related Resources yet: keep readers in their own local guides.
        guides = legacy_cards(locale)
        related = [guides[i][1] for i in (0, 2)]
    url = path(locale, article["id"])
    content = libraries(locale, article) + f'''<article class="resource-article">
<nav class="resource-breadcrumb" aria-label="{esc(l['breadcrumb'])}"><a href="/?lang={locale}">TeacherPalette</a><span aria-hidden="true">/</span><a href="{path(locale)}">{esc(LOCALES[locale]['label'])}</a></nav>
<p class="resource-eyebrow">{esc(LOCALES[locale]['categories'][article['category']])} · Mac</p>
<h1>{esc(data['heading'])}</h1><p class="resource-lead">{esc(data['lead'])}</p>
<div class="resource-actions"><a class="resource-button resource-button-primary" href="{esc(store)}">{esc(l['trial'])}</a><a class="resource-button resource-button-secondary" href="#demo">{esc(l['action'])}</a></div>
<p class="resource-trial-note">{esc(l['trialNote'])}</p>
{video}{toc}{body}{cta(store, locale)}
<aside class="resource-related"><h2>{esc(LOCALES[locale]['related'])}</h2><div class="resource-grid">{"".join(related)}</div></aside>
</article>'''
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": data["heading"], "description": data["description"],
         "mainEntityOfPage": ORIGIN + url, "url": ORIGIN + url, "inLanguage": locale,
         "articleSection": LOCALES[locale]["categories"][article["category"]],
         "image": ORIGIN + "/media/teacherpalette-social-v2.png",
         "publisher": {"@type": "Organization", "name": "TeacherPalette", "url": ORIGIN + "/"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "TeacherPalette", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": LOCALES[locale]["label"], "item": ORIGIN + path(locale)},
            {"@type": "ListItem", "position": 3, "name": data["title"], "item": ORIGIN + url}]}]}
    available = article_alternates(article)
    return page(locale, data["title"], data["description"], url, content, available, schema, True)


def build_index(locale):
    l = LOCALES[locale]
    articles = translated_articles(locale)
    legacy = legacy_cards(locale)
    content = libraries(locale) + f'<div class="resource-index-hero"><p class="resource-eyebrow">TeacherPalette</p><h1>{esc(l["label"])}</h1><p class="resource-lead">{esc(l["lead"])}</p></div>'
    if articles:
        content += f'<section class="resource-collection"><h2>{esc(l["featured"])}</h2><div class="resource-grid">' + "".join(article_card(a, locale) for a in articles) + '</div></section>'
    content += f'<section class="resource-collection"><h2>{esc(l["practical"])}</h2><p>{esc(l["practicalLead"])}</p><div class="resource-grid">' + "".join(c[1] for c in legacy) + '</div></section>'
    urls = [path(locale, a["id"]) for a in articles] + [c[0] for c in legacy]
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": l["title"],
              "description": l["description"], "url": ORIGIN + path(locale), "inLanguage": locale,
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "url": ORIGIN + url} for i, url in enumerate(urls)]}}
    return page(locale, l["title"], l["description"], path(locale), content,
                {code: path(code) for code in LOCALES}, schema)


def managed(source, name, content):
    start, end = f"<!-- resources:{name}:start -->", f"<!-- resources:{name}:end -->"
    if start not in source or end not in source:
        raise ValueError(f"Missing managed block: {name}")
    return re.sub(re.escape(start) + r".*?" + re.escape(end), lambda _: start + "\n" + content + "\n" + end, source, flags=re.S)


def build_home(source):
    nav = f'<a class="header-link" data-resource-link href="/en/resources/">{spans(LABELS)}</a>'
    footer = f'<a data-resource-link href="/en/resources/">{spans(LABELS)}</a>'
    panels = []
    for locale, l in LOCALES.items():
        featured = translated_articles(locale)
        cards = [article_card(a, locale) for a in featured[:3]]
        if len(cards) < 3:
            guides = legacy_cards(locale)
            cards.extend(guides[i][1] for i in (0, 2, 3))
            cards = cards[:3]
        panels.append(f'<div data-lang-{locale} lang="{locale}"><div class="resource-grid">{"".join(cards)}</div><a class="resource-all" href="{path(locale)}">{esc(l["all"])} <span aria-hidden="true">→</span></a></div>')
    section = f'''<section id="resources" class="home-resources" aria-labelledby="home-resources-title"><div class="section-inner">
<div class="section-header"><h2 id="home-resources-title">{spans(LABELS)}</h2><p>{spans({code: l['homeLead'] for code, l in LOCALES.items()})}</p></div>
<div class="resource-home-panels">{"".join(panels)}</div>
</div></section>'''
    return managed(managed(managed(source, "nav", nav), "footer", footer), "home", section)


def build_sitemap(urls):
    source = (ROOT / "sitemap.xml").read_text()
    # Preserve existing routes except the retired English screen-annotation page.
    source = re.sub(r"\s*<url>\s*<loc>https://teacherpalette\.com/en/draw-on-screen-mac/</loc>\s*</url>", "", source)
    source = re.sub(r"\s*<url>\s*<loc>https://teacherpalette\.com/(?:en|ja|ko)/resources/.*?</url>", "", source, flags=re.S)
    additions = "".join(f"  <url><loc>{ORIGIN + url}</loc></url>\n" for url in urls)
    result = source.replace("</urlset>", additions + "</urlset>")
    ET.fromstring(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if checked-in output differs; write nothing")
    args = parser.parse_args()
    ids = [a["id"] for a in ARTICLES]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate article ID")
    for a in ARTICLES:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a["id"]):
            raise ValueError("Invalid article ID")
        for locale, data in a["locales"].items():
            if locale not in LOCALES or a["category"] not in LOCALES[locale]["categories"]:
                raise ValueError("Unknown locale or category")
            if not (SOURCE / data["body"]).resolve().is_relative_to(SOURCE.resolve()):
                raise ValueError("Content body must remain inside resources/content")
    home_source = (ROOT / "index.html").read_text()
    store = html.unescape(re.search(r'<a href="(https://apps\.apple\.com/[^"]+)" class="btn btn-primary"', home_source)[1])
    outputs = {}
    urls = []
    for locale in LOCALES:
        url = path(locale)
        outputs[ROOT / url.lstrip("/") / "index.html"] = build_index(locale)
        urls.append(url)
    for article in ARTICLES:
        for locale in article["locales"]:
            url = path(locale, article["id"])
            outputs[ROOT / url.lstrip("/") / "index.html"] = build_article(article, locale, store)
            urls.append(url)
    outputs[ROOT / "index.html"] = build_home(home_source)
    outputs[ROOT / "sitemap.xml"] = build_sitemap(urls)
    stale = []
    for output, content in outputs.items():
        if args.check:
            if not output.is_file() or output.read_text() != content:
                stale.append(str(output.relative_to(ROOT)))
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content)
    if stale:
        raise SystemExit("Generated output is stale: " + ", ".join(stale))
    print(f"{'Verified' if args.check else 'Built'} {len(urls)} resource pages, home integration and sitemap.")


if __name__ == "__main__":
    main()
