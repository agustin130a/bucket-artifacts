#!/usr/bin/env python3
"""Genera index.html con la lista de páginas, agrupadas por carpeta.

Una página es cualquier .html fuera de la raíz (se ignoran scripts/, .github/ y carpetas que
empiezan con punto o guion bajo). El nombre que se muestra sale del <title> de cada página.
Uso: python3 scripts/build_index.py [directorio]  (por defecto, la raíz del repo).
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
SKIP = {"scripts"}
TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def title_of(path: Path) -> str:
    match = TITLE.search(path.read_text(encoding="utf-8", errors="ignore")[:8192])
    return html.unescape(match.group(1).strip()) if match else path.stem


def pages() -> dict[str, list[tuple[str, str]]]:
    groups: dict[str, list[tuple[str, str]]] = {}
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        top = rel.parts[0]
        if len(rel.parts) == 1 or top in SKIP or top.startswith((".", "_")):
            continue
        groups.setdefault(top, []).append((rel.as_posix(), title_of(path)))
    return groups


def render(groups: dict[str, list[tuple[str, str]]]) -> str:
    sections = []
    for folder, items in groups.items():
        links = "\n".join(
            f'      <li><a href="{html.escape(href)}">{html.escape(name)}</a>'
            f" <code>{html.escape(href)}</code></li>"
            for href, name in items
        )
        sections.append(f"  <h2>{html.escape(folder)}</h2>\n  <ul>\n{links}\n  </ul>")
    body = "\n".join(sections) or "  <p>Todavía no hay páginas.</p>"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>bucket-artifacts</title>
<style>
  :root {{ color-scheme: light dark; --fg: #1b2129; --muted: #66707c; --bg: #fafbfc; --link: #1f6feb; }}
  @media (prefers-color-scheme: dark) {{ :root {{ --fg: #e6edf3; --muted: #8b96a3; --bg: #0f141a; --link: #6aa8ff; }} }}
  body {{ margin: 0; background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, sans-serif; }}
  main {{ max-width: 720px; margin: 0 auto; padding: 40px 16px; }}
  h1 {{ margin: 0 0 4px; font-size: 1.6rem; }}
  h2 {{ margin: 28px 0 6px; font-size: 1.05rem; }}
  p {{ margin: 0; color: var(--muted); }}
  ul {{ margin: 0; padding-left: 1.2em; }}
  a {{ color: var(--link); }}
  code {{ color: var(--muted); font-size: .8em; }}
</style>
</head>
<body>
<main>
  <h1>bucket-artifacts</h1>
  <p>Páginas estáticas publicadas, por carpeta.</p>
{body}
</main>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "index.html").write_text(render(pages()), encoding="utf-8")
    print(f"index.html: {sum(len(v) for v in pages().values())} páginas")
