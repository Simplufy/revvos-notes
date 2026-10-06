#!/usr/bin/env python3
"""Rebuild index.html and sitemap.xml from articles/<slug>/index.html. Run after adding an article."""
import pathlib, re, html, datetime
R = pathlib.Path(__file__).parent; CFG = dict(l.split("=", 1) for l in (R / "site.cfg").read_text().split("\n") if "=" in l)
rows = []
for p in sorted((R / "articles").glob("*/index.html")):
    t = p.read_text(encoding="utf-8")
    title = html.unescape(re.search(r"<h1>(.*?)</h1>", t, re.S).group(1)); date = re.search(r'"datePublished":"([^"]+)"', t).group(1)
    desc = html.unescape(re.search(r'name="description" content="([^"]*)"', t).group(1))
    rows.append((date, p.parent.name, title, desc))
rows.sort(reverse=True)
items = "\n".join(f'<li><a href="articles/{s}/">{html.escape(ti)}</a><br><small>{d} · {html.escape(de)}</small></li>' for d, s, ti, de in rows)
(R / "index.html").write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{CFG['name']} notes</title><meta name="description" content="{html.escape(CFG['blurb'])}"><link rel="canonical" href="{CFG['base']}">
<link rel="stylesheet" href="style.css"></head><body><header><a href="{CFG['site']}">{CFG['site']}</a></header><main><h1>{CFG['name']} notes</h1>
<p>{html.escape(CFG['blurb'])}</p><ul>{items or '<li>First notes coming soon.</li>'}</ul></main><footer>&copy; {CFG['name']}</footer></body></html>
""", encoding="utf-8", newline="\n")
urls = [CFG["base"]] + [f"{CFG['base']}articles/{s}/" for _, s, _, _ in rows]
(R / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{u}</loc><lastmod>{datetime.date.today()}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8", newline="\n")
print(len(rows), "articles")
