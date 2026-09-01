#!/bin/bash
set -euo pipefail

python3 update_readme.py

if git diff --quiet README.md; then
  echo "Nenhuma alteração no README.md. Nada a commitar."
  exit 0
else
  git config --global user.name "github-actions[bot]"
  git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git add README.md
  git commit -m "📝 Atualiza projeto atual e projetos em destaque"
  git push
fi
