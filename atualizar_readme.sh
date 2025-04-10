#!/bin/bash

USERNAME="LucasArais"

REPO=$(curl -s "https://api.github.com/users/$USERNAME/repos?sort=updated&per_page=1" | jq -r '.[0].name')

sed -i "s/<!-- PROJETO_ATUAL -->/$REPO/g" README.md
