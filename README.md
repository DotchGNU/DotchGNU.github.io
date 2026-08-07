# gwdkim-site

Personal academic homepage. Static, single page, no framework.

Design rationale, discarded alternatives, and open questions live in the
Obsidian vault, not here:
`obsidian://open?vault=notes&file=Writing%2Fhomepage%2Fgwdkim-site-design`

## Layout

```
data/*.yml            content — the only files that change day to day
templates/*.j2        markup
static/               style.css, cv.pdf
build.py              data + template -> docs/
docs/                 build output; GitHub Pages serves this folder
```

`docs/` is committed. GitHub Pages is configured to serve `main` branch `/docs`,
so there is no CI step — pushing a build publishes it.

## Adding a paper

```bash
# ================== COPY FROM HERE ==================
cd /mnt/d/GWK_data/Document/gwdkim-site
vi data/publications.yml          # add one record
python3 build.py                  # prints counts — check them
git add -A && git commit -m "add paper" && git push
# =================== COPY TO HERE ===================
```

Nothing in `templates/` or `static/` needs touching. The same applies to
`awards.yml`, `talks.yml`, `resources.yml`, `education.yml`.

## Conventions

- **Never write `<span class="me">` by hand.** `data/site.yml` holds the author's
  own name once, as `me`; `build.py` finds it in every author list and marks it.
  Change the preferred rendering there and it changes everywhere.
- **Never hand-count anything shown on the page.** The `Presentations (N)`
  count comes from `talks|length`.
- `doi` fields are bare DOIs — no `https://doi.org/` prefix. The template adds it.
- Author lists are display strings. Shorten long ones with `…`, but keep the
  author's own name visible so it can be highlighted.

## Requirements

Python 3 with `PyYAML` and `Jinja2`.

```bash
python3 -c "import yaml, jinja2; print('ok')"
```

## Custom domain

`CUSTOM_DOMAIN` at the top of `build.py` is empty on purpose. Set it to
`gwdkim.com` **only after** the domain is registered and its DNS points at
GitHub Pages:

```
A      @     185.199.108.153  185.199.109.153  185.199.110.153  185.199.111.153
CNAME  www   dotchgnu.github.io
```

Writing a `CNAME` file for a domain that does not resolve yet makes GitHub
redirect `dotchgnu.github.io` to it, which takes the site offline.
