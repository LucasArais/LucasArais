#!/bin/bash

# Busca o commit mais recente do usuário via API do GitHub
latest_repo=$(curl -s "https://api.github.com/users/LucasArais/events/public" | \
  jq -r '[.[] | select(.type=="PushEvent")][0].repo.name')

# Atualiza a seção no README.md
sed -i "s|<!-- REPO_ATUAL -->.*<!-- FIM_REPO_ATUAL -->|<!-- REPO_ATUAL --> $latest_repo <!-- FIM_REPO_ATUAL -->|" README.md
