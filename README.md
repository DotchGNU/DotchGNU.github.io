# gwdkim-site

Personal academic homepage. Static, single page, no framework.

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
cd path/to/gwdkim-site
vi data/publications.yml          # add one record
python3 build.py                  # prints counts — check them
git add -A && git commit -m "add paper" && git push
# =================== COPY TO HERE ===================
```

Nothing in `templates/` or `static/` needs touching. The same applies to
`awards.yml`, `talks.yml`, `resources.yml`, `education.yml`.

## Conventions

- **No HTML in the data files.** `data/site.yml` holds the author's own name once,
  as `me`; `build.py` finds it in every author list and wraps it in
  `<span class="me">`. The bio works the same way: `bio` is a list of plain
  paragraphs and `bio_links` maps a phrase to a URL, which `build.py` turns into
  an anchor on its first occurrence. Reword a phrase there and the link follows
  it; write `<a href>` into the YAML and it will be escaped and shown literally.
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

Live at **https://gwdkim.com** since 2026-08-07. `dotchgnu.github.io` redirects
to it. The certificate (Let's Encrypt, via GitHub) covers both `gwdkim.com` and
`www.gwdkim.com` and renews automatically.

`CUSTOM_DOMAIN` at the top of `build.py` writes `docs/CNAME`, which is what
GitHub reads. Registered at Cloudflare; DNS is nine records, all **DNS only**
(grey cloud — proxying them blocks GitHub's certificate issuance):

```
A      @     185.199.108.153  185.199.109.153  185.199.110.153  185.199.111.153
AAAA   @     2606:50c0:8000::153  ::8001::153  ::8002::153  ::8003::153
CNAME  www   dotchgnu.github.io
```

**Order matters if this is ever redone.** Point DNS first and confirm it
resolves; only then set `CUSTOM_DOMAIN`. Writing a `CNAME` file for a name that
does not resolve yet makes GitHub redirect the .github.io address to it, which
takes the site offline with no obvious cause.
