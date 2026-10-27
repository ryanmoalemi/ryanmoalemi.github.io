"""Build /feed.xml (Atom) from blog/*.html post meta tags. Run: python3 scripts/build_feed.py"""
import glob, html, re, os
from datetime import datetime, timezone
SITE = "https://ryanmoalemi.blog"
def meta(src, attr, name):
    m = re.search(r'<meta\s+%s="%s"\s+content="([^"]*)"' % (attr, re.escape(name)), src)
    return html.unescape(m.group(1)) if m else ""
posts = []
for p in glob.glob("blog/*.html"):
    if p.endswith("index.html"): continue
    s = open(p, encoding="utf-8").read()
    date = meta(s, "property", "article:published_time")
    if not date: continue
    mod = meta(s, "property", "article:modified_time") or date
    posts.append(dict(url=meta(s, "property", "og:url") or f"{SITE}/{p}", title=meta(s, "property", "og:title"),
        summary=meta(s, "name", "description"), image=meta(s, "property", "og:image"), date=date, mod=mod))
posts.sort(key=lambda x: x["date"], reverse=True)
ts = lambda d: (d if "T" in d else d + "T00:00:00Z")
e = lambda t: html.escape(t, quote=True)
updated = ts(max((p["mod"] for p in posts), default="2026-09-17"))
out = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom">',
  '  <title>Ryan Moalemi | Blog</title>', '  <subtitle>Writing from Ryan Moalemi. Latest posts first.</subtitle>',
  f'  <link href="{SITE}/feed.xml" rel="self" type="application/atom+xml"/>',
  f'  <link href="{SITE}/" rel="alternate" type="text/html"/>',
  '  <link href="https://pubsubhubbub.appspot.com/" rel="hub"/>',
  f'  <id>{SITE}/</id>', f'  <updated>{updated}</updated>',
  '  <author><name>Ryan Moalemi</name><uri>https://ryanmoalemi.blog/about.html</uri></author>',
  f'  <icon>{SITE}/favicon-32.png</icon>']
for p in posts:
    out += ['  <entry>', f'    <title>{e(p["title"])}</title>', f'    <link href="{e(p["url"])}" rel="alternate" type="text/html"/>',
      f'    <id>{e(p["url"])}</id>', f'    <published>{ts(p["date"])}</published>', f'    <updated>{ts(p["mod"])}</updated>',
      f'    <summary>{e(p["summary"])}</summary>', '  </entry>']
out.append('</feed>')
open("feed.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
TAG = '<link rel="alternate" type="application/atom+xml" title="Ryan Moalemi | Blog" href="https://ryanmoalemi.blog/feed.xml">'
for f in glob.glob("*.html") + glob.glob("blog/*.html"):
    s = open(f, encoding="utf-8").read()
    if 'application/atom+xml' not in s:
        open(f, "w", encoding="utf-8").write(s.replace("</head>", f"  {TAG}\n</head>", 1))
print(f"feed.xml: {len(posts)} posts")
