# TeacherPalette Resources

Resources uses the existing static HTML hosting. No framework, CMS, package
installation, or hosting build configuration is required. Commit the generated
HTML alongside its source. Python 3.9+ is only needed when editing content.

## Source of truth

- `content/articles.json`: stable article IDs, category, related IDs, and metadata
  grouped by locale. The order controls the index and featured home cards.
- `content/en/*.html`: editorial body fragments. Each section needs a unique
  `<h2 id="...">` for the generated table of contents.
- `content/locales.json`: localized interface copy and existing practical-guide
  paths. Existing guide titles and descriptions are read from those HTML files.
- `templates/page.html`: shared document, metadata, scripts and stylesheet.
- `style.css`, `theme.js`, `site.js`: product colors, native typography, responsive
  cards, theme preference (`tp.theme`) and collapsible navigation.
- `../scripts/build_resources.py`: generates the pages, managed home sections and
  resource entries in the existing sitemap. All non-resource sitemap entries are
  preserved. The official App Store URL is read from the homepage's primary CTA.
- `../scripts/verify_resources.py`: checks generated output, metadata, schemas,
  local links, assets, sitemap coverage and existing URL preservation.

The existing `/guides/` editorial collection and all practical-guide URLs remain
available. The new library links to them without moving or redirecting them.

## Add a new article

1. Write `resources/content/en/draw-screen-presenting-mac.html`, for example:

   ```html
   <section aria-labelledby="prepare">
     <h2 id="prepare">Prepare the screen you will present</h2>
     <p>Write the actual, verified instructions here.</p>
   </section>
   ```

2. Append an entry to the `articles` array in `resources/content/articles.json`:

   ```json
   {
     "id": "draw-screen-presenting-mac",
     "category": "guides",
     "related": ["annotate-screen-mac", "screen-annotation-teachers-mac"],
     "locales": {
       "en": {
         "title": "How to Draw on Your Screen While Presenting on Mac",
         "heading": "How to Draw on Your Screen While Presenting on Mac",
         "description": "Write a unique description that matches the finished guide.",
         "summary": "Write a short, useful card description.",
         "lead": "Write the opening paragraph for this search intent.",
         "body": "en/draw-screen-presenting-mac.html",
         "demo": {
           "video": "drawing-shortcuts.mp4",
           "poster": "drawing-shortcuts-poster.jpg",
           "caption": "Describe what this existing demo shows."
         }
       }
     }
   }
   ```

3. From the repository root, run:

   ```sh
   python3 scripts/build_resources.py
   python3 scripts/verify_resources.py
   ```

4. Inspect desktop, tablet and mobile views. Commit the source and generated
   `en/resources/draw-screen-presenting-mac/index.html`, index pages, home and
   sitemap. The host still serves plain HTML; there is no client-side content
   fetch. `--check` verifies reproducibility without writing files.

Supported categories are `guides`, `comparisons`, and `use-cases`. There are no
invented author names, publication dates, ratings or reviews. Add accurate dates
and attribution deliberately if the editorial workflow later requires them.

## Localization

The EN, JA and KO library indexes are localized now. JA and KO currently list
their existing local practical guides; they do not display the English articles.

To publish an article in Japanese or Korean, add a `ja` or `ko` entry under that
article's `locales` with its own metadata, heading, lead, demo caption and body
path, and write the corresponding HTML fragment. Only published variants appear
in an article's hreflang links or local related cards. Libraries remain separate
from article translations: the language links explicitly say “Resource libraries.”
Do not create English fallback pages under Japanese or Korean article URLs.

The homepage preserves its existing nine-language switch. EN/JA/KO point to their
own libraries. The other six languages clearly label the English library in the
menu and section heading, following the existing English fallback behavior.

When a locale gains articles, the home builder uses those article cards instead
of the existing practical-guide selection. Do not modify generated pages directly.
The index has no hard item limit; the home shows up to three articles. For larger
collections, category filtering or pagination can be added to this registry later.

## Verification and preview

```sh
python3 scripts/build_resources.py --check
python3 scripts/verify_resources.py
python3 -m http.server 8765 --bind 127.0.0.1
# In another terminal:
python3 scripts/verify_resources.py --base-url http://127.0.0.1:8765
```

Preview `/en/resources/`, `/ja/resources/` and `/ko/resources/`. Resource videos
use existing posters, explicit native playback controls, `playsinline` and
`preload="none"`. No video autoplays or third-party iframe is added. Video layout
reserves its aspect ratio. Articles include a keyboard-accessible table of
contents; the comparison table scrolls inside its own region on narrow screens.

The generated HTML is the production artifact. The existing homepage's SEO,
analytics behavior, canonical and product conversion sections are retained.
Core Web Vitals and live search indexation require measurement after deployment;
local layout checks alone do not establish either.
