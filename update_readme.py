#!/usr/bin/env python3
"""Atualiza o README com o projeto atual e os projetos em destaque.

Busca os repositórios públicos mais recentemente atualizados do usuário
(excluindo este próprio repositório de perfil e forks) e reescreve os
blocos entre os marcadores REPO_ATUAL e FEATURED_PROJECTS_* no README.md.
"""
import json
import os
import re
import urllib.request

USERNAME = "LucasArais"
SELF_REPO = "LucasArais"
README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
FEATURED_COUNT = 4

# emoji, badge "label-color", ícone shields, cor do texto do badge
LANG_BADGES = {
    "Python": ("🐍", "Python-3776AB", "python", "white"),
    "TypeScript": ("🔷", "TypeScript-3178C6", "typescript", "white"),
    "JavaScript": ("🟨", "JavaScript-F7DF1E", "javascript", "black"),
    "Jupyter Notebook": ("📓", "Jupyter-F37626", "jupyter", "white"),
    "Java": ("☕", "Java-ED8B00", "openjdk", "white"),
    "HTML": ("🌐", "HTML5-E34F26", "html5", "white"),
    "CSS": ("🎨", "CSS3-1572B6", "css3", "white"),
    "C": ("🔧", "C-A8B9CC", "c", "black"),
    "PHP": ("🐘", "PHP-777BB4", "php", "white"),
    "Shell": ("🐚", "Shell-4EAA25", "gnubash", "white"),
    "Dart": ("🎯", "Dart-0175C2", "dart", "white"),
}
DEFAULT_BADGE = ("📦", "Code-6e7781", "github", "white")


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-readme-bot")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def esc(text):
    text = text or ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_card(repo):
    name = repo["name"]
    desc = esc(repo.get("description"))
    url = repo["html_url"]
    emoji, badge_slug, logo, logo_color = LANG_BADGES.get(repo.get("language"), DEFAULT_BADGE)
    lang_badge = f"https://img.shields.io/badge/{badge_slug}?style=flat-square&logo={logo}&logoColor={logo_color}"
    commit_badge = f"https://img.shields.io/github/last-commit/{USERNAME}/{name}?style=flat-square&color=1488CC"
    cta_badge = "https://img.shields.io/badge/Ver_reposit%C3%B3rio-%E2%86%92-181717?style=for-the-badge&logo=github&logoColor=white"
    desc_html = f"\n      <sub>{desc}</sub>" if desc else ""
    lang_alt = esc(repo.get("language") or "código")
    return f"""    <td width="50%" valign="top" align="center">
      <h4>{emoji} &nbsp;<a href="{url}">{esc(name)}</a></h4>{desc_html}
      <br/><br/>
      <img src="{lang_badge}" alt="{lang_alt}"/>
      <img src="{commit_badge}" alt="último commit"/>
      <br/><br/>
      <a href="{url}"><img src="{cta_badge}" alt="Ver repositório"/></a>
    </td>"""


def build_table(repos):
    cards = [build_card(r) for r in repos]
    rows = []
    for i in range(0, len(cards), 2):
        pair = cards[i : i + 2]
        rows.append("  <tr>\n" + "\n".join(pair) + "\n  </tr>")
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def replace_between(content, start_marker, end_marker, new_inner, inline=False):
    pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL)
    sep = "" if inline else "\n"
    replacement = f"{start_marker}{sep}{new_inner}{sep}{end_marker}"
    return pattern.sub(lambda _match: replacement, content, count=1)


def main():
    repos = api(f"/users/{USERNAME}/repos?sort=pushed&per_page=15")
    candidates = [r for r in repos if not r.get("fork") and r["name"] != SELF_REPO]
    candidates = candidates[:FEATURED_COUNT]

    if not candidates:
        print("Nenhum repositório encontrado para destaque.")
        return

    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    original = content

    content = replace_between(
        content,
        "<!-- REPO_ATUAL -->",
        "<!-- FIM_REPO_ATUAL -->",
        esc(candidates[0]["name"]),
        inline=True,
    )

    table = build_table(candidates)
    content = replace_between(
        content,
        "<!-- FEATURED_PROJECTS_START -->",
        "<!-- FEATURED_PROJECTS_END -->",
        table,
    )

    if content != original:
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"README.md atualizado. Projeto atual: {candidates[0]['name']}")
    else:
        print("Nenhuma alteração no README.md.")


if __name__ == "__main__":
    main()
