#!/bin/bash

# Pega o repositório com o commit mais recente (usuário LucasArais)
REPO=$(curl -s "https://api.github.com/users/LucasArais/repos?sort=pushed&per_page=1" | jq -r '.[0].name')

# Faz o replace dentro do README
sed -i "s/<!-- REPO_ATUAL -->.*<!-- FIM_REPO_ATUAL -->/<!-- REPO_ATUAL -->$REPO<!-- FIM_REPO_ATUAL -->/" README.md
