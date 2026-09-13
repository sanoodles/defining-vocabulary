"""Inline pt_levels.json into the template: the page must open over file://.

Writes the same page twice. `defining-pt.html` is the local copy the README points at.
`site/` is the deploy: the page, its headers, and an allowlist that keeps everything else
in that directory — a linked project's OIDC token included — out of the upload.
"""
import pathlib, shutil

here = pathlib.Path(__file__).resolve().parent
root = here.parent
tpl = (here / "page_template.html").read_text(encoding="utf-8")
data = (root / "pt_levels.json").read_text(encoding="utf-8").strip()
page = tpl.replace("__DATA__", data)

(root / "defining-pt.html").write_text(page, encoding="utf-8")

site = root / "site"
site.mkdir(exist_ok=True)
(site / "index.html").write_text(page, encoding="utf-8")
shutil.copyfile(here / "vercel.json", site / "vercel.json")
shutil.copyfile(here / "vercelignore", site / ".vercelignore")
