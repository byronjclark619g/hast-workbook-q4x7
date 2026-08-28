#!/usr/bin/env python3
"""Build the HAST Entrepreneurship workbook site.

Source of truth: /Users/bclark/Curriculum/*_Student_Page.html (embed-style fragments).
This script wraps each fragment in a full HTML document with the site band,
noindex meta, and V4 typography, and writes it to <course>/module-<n>/index.html.

Workflow: edit fragments in the Curriculum repo -> python3 build.py -> git commit & push.
The homepage (index.html) is hand-maintained, not generated.
"""
import pathlib

SRC = pathlib.Path("/Users/bclark/Curriculum")
ROOT = pathlib.Path(__file__).resolve().parent

MODULES = [
    ("POE_M01_Student_Page.html", "poe/module-1", "POE Module 1 — Owners vs. Earners", "Find It — Principles of Entrepreneurship"),
    ("POE_M02_Student_Page.html", "poe/module-2", "POE Module 2 — Buy, Build, or Stay Employed?", "Find It — Principles of Entrepreneurship"),
    ("NVD_M01_Student_Page.html", "nvd/module-1", "NVD Module 1 — Why Buy a Business?", "Buy It — New Venture Development"),
    ("NVD_M02_Student_Page.html", "nvd/module-2", "NVD Module 2 — The Hidden Market", "Buy It — New Venture Development"),
    ("SBO_Case_File_Student_Page.html", "sbo/case-file", "SBO Case File — Calumet Lawn & Snow", "Run It — Small Business Operations"),
    ("SBO_M01_Student_Page.html", "sbo/module-1", "SBO Module 1 — You Own It Now", "Run It — Small Business Operations"),
    ("SBO_M02_Student_Page.html", "sbo/module-2", "SBO Module 2 — The First 120 Days", "Run It — Small Business Operations"),
]

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} · HAST Entrepreneurship</title>
<style>
  body{{margin:0;background:#fff}}
  .siteband{{background:#111;border-bottom:4px solid #C5B358;padding:10px 20px;display:flex;gap:6px 16px;align-items:baseline;flex-wrap:wrap;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
  .siteband a{{color:#C5B358;text-decoration:none;font-weight:800;letter-spacing:1px;font-size:15px}}
  .siteband span{{color:#d9d9d9;font-size:13px;font-family:Georgia,'Times New Roman',serif;font-style:italic}}
  .pagepad{{padding:16px 16px 0}}
</style>
</head>
<body>
<div class="siteband"><a href="{home}">HAST ENTREPRENEURSHIP</a><span>{course}</span></div>
<div class="pagepad">
{fragment}
</div>
</body>
</html>
"""

def main():
    for src_name, out_dir, title, course in MODULES:
        text = (SRC / src_name).read_text()
        for marker in ('<div id="mw">', '<div id="m2wrap">'):
            idx = text.find(marker)
            if idx >= 0:
                break
        if idx < 0:
            raise SystemExit(f"no wrapper div found in {src_name}")
        frag = text[idx:]
        out = ROOT / out_dir / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        depth = "../" * len(out_dir.split("/"))
        out.write_text(TEMPLATE.format(title=title, course=course, home=depth, fragment=frag))
        print(f"built {out_dir}/index.html  <- {src_name}")

if __name__ == "__main__":
    main()
