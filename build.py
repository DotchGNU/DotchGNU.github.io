#!/usr/bin/env python3
"""Build the site: data/*.yml + templates/index.html.j2 -> docs/

Run from anywhere:  python3 build.py
Requires:           PyYAML, Jinja2
"""

# ── config ──────────────────────────────────────────────────────────────
# Leave CUSTOM_DOMAIN empty until gwdkim.com is registered AND its DNS points
# at GitHub Pages. Writing a CNAME for a domain you do not yet control makes
# GitHub redirect <user>.github.io to it, which takes the site offline.
CUSTOM_DOMAIN = ""            # -> "gwdkim.com" once DNS is live
DATA_FILES = ["site", "publications", "resources", "awards", "talks", "education"]
# ── logic (below uses only the values above) ────────────────────────────

import html
import re
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
DATA, TEMPLATES, STATIC, OUT = (ROOT / d for d in ("data", "templates", "static", "docs"))


def load(name):
    path = DATA / f"{name}.yml"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def highlight_me(authors, me):
    """Escape an author list, then wrap every occurrence of the owner's name.

    The name lives in data/site.yml as `me`. Author lists never carry markup,
    so changing the preferred rendering is a one-line edit there.
    """
    escaped = html.escape(authors or "")
    if not me:
        return Markup(escaped)
    marked = re.sub(re.escape(html.escape(me)),
                    r'<span class="me">\g<0></span>', escaped)
    return Markup(marked)


def main():
    data = {name: (load(name) or ([] if name != "site" else {})) for name in DATA_FILES}
    site = data["site"]
    me = site.get("me", "")

    for record in [*data["publications"], *data["talks"]]:
        record["authors_html"] = highlight_me(record.get("authors"), me)

    first = sorted((p for p in data["publications"] if p.get("role") == "first"),
                   key=lambda p: p.get("year", 0), reverse=True)
    co = sorted((p for p in data["publications"] if p.get("role") != "first"),
                key=lambda p: p.get("year", 0), reverse=True)
    talks = sorted(data["talks"], key=lambda t: t.get("year", 0), reverse=True)

    # autoescape=True, not select_autoescape(): that helper keys off the template
    # FILENAME, and "index.html.j2" ends in .j2, so it would silently leave
    # escaping off and emit raw "&" and "<" from the data files.
    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    rendered = env.get_template("index.html.j2").render(
        site=site, first=first, co=co, talks=talks,
        resources=data["resources"], awards=data["awards"], education=data["education"],
    )

    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(rendered, encoding="utf-8")
    for item in sorted(STATIC.iterdir()):
        if item.is_file():
            shutil.copy2(item, OUT / item.name)

    cname = OUT / "CNAME"
    if CUSTOM_DOMAIN:
        cname.write_text(CUSTOM_DOMAIN + "\n", encoding="utf-8")
    elif cname.exists():
        cname.unlink()

    print(f"built  {OUT / 'index.html'}")
    print(f"  publications   {len(first)} first-author + {len(co)} co-authored")
    print(f"  resources      {len(data['resources'])}")
    print(f"  awards         {len(data['awards'])}")
    print(f"  presentations  {len(talks)}")
    print(f"  custom domain  {CUSTOM_DOMAIN or '(none — serving on github.io)'}")
    if not site.get("bio"):
        print("  note: bio is empty, so the intro paragraph is omitted")


if __name__ == "__main__":
    main()
