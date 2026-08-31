#!/bin/bash
set -euo pipefail

AUTH_HEADER=()
if [ -n "${GITHUB_TOKEN:-}" ]; then
  AUTH_HEADER=(-H "Authorization: token $GITHUB_TOKEN")
fi

REPO=$(curl -s "${AUTH_HEADER[@]}" "https://api.github.com/users/LucasArais/repos?sort=pushed&per_page=5" \
  | jq -r '[.[] | select(.name != "LucasArais")][0].name')

if [ -z "$REPO" ] || [ "$REPO" = "null" ]; then
  echo "Erro: não foi possível obter o nome do repositório."
  exit 1
fi

sed -i "s/<!-- REPO_ATUAL -->.*<!-- FIM_REPO_ATUAL -->/<!-- REPO_ATUAL -->$REPO<!-- FIM_REPO_ATUAL -->/" README.md

if git diff --quiet README.md; then
  echo "Nenhuma alteração no README.md. Nada a commitar."
  exit 0
else
  git config --global user.name "github-actions[bot]"
  git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
  git add README.md
  git commit -m "📝 Atualiza projeto atual para: $REPO"
  git push
fi
