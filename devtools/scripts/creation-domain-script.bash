#!/bin/bash
# USO: bash devtools/scripts/creation-domain-script.bash marketplace shopee

DOMAIN=$1
MODULE=$2

if [ -z "$DOMAIN" ] || [ -z "$MODULE" ]; then
  echo "Erro: informe o dominio e o modulo."
  echo "Uso: bash scripts/creation-domain-script.bash {dominio} {modulo}"
  exit 1
fi

BASE="$DOMAIN/$MODULE"

echo "Criando estrutura: $BASE"

# Dominio
touch "$DOMAIN/__init__.py"

# Modulo raiz
mkdir -p "$BASE"
touch "$BASE/__init__.py"
touch "$BASE/.env"
touch "$BASE/jobs.py"
touch "$BASE/main.py"
touch "$BASE/requirements.txt"
touch "$BASE/MAP.md"
touch "$BASE/VALIDATION_REPORT.md"

# Downloader
for DIR in configuration exception repository service transfer validator; do
  mkdir -p "$BASE/downloader/$DIR"
  touch "$BASE/downloader/$DIR/__init__.py"
done
touch "$BASE/downloader/__init__.py"
touch "$BASE/downloader/configuration/configuration.py"
touch "$BASE/downloader/exception/exception.py"
touch "$BASE/downloader/repository/repository.py"
touch "$BASE/downloader/service/service.py"
touch "$BASE/downloader/transfer/request_transfer.py"
touch "$BASE/downloader/validator/validator.py"

# Extractor
for DIR in exception service transfer validator; do
  mkdir -p "$BASE/extractor/$DIR"
  touch "$BASE/extractor/$DIR/__init__.py"
done
touch "$BASE/extractor/__init__.py"
touch "$BASE/extractor/exception/exception.py"
touch "$BASE/extractor/service/service.py"
touch "$BASE/extractor/transfer/request_transfer.py"
touch "$BASE/extractor/validator/validator.py"

# Output
for DIR in exception mapper service transfer validator; do
  mkdir -p "$BASE/output/$DIR"
  touch "$BASE/output/$DIR/__init__.py"
done
touch "$BASE/output/__init__.py"
touch "$BASE/output/exception/exception.py"
touch "$BASE/output/mapper/mapper.py"
touch "$BASE/output/service/service.py"
touch "$BASE/output/transfer/response_transfer.py"
touch "$BASE/output/validator/validator.py"

# Shared
mkdir -p "$BASE/shared/config"
mkdir -p "$BASE/shared/infra/cache"
touch "$BASE/shared/__init__.py"
touch "$BASE/shared/config/__init__.py"
touch "$BASE/shared/config/settings.py"
touch "$BASE/shared/infra/__init__.py"
touch "$BASE/shared/infra/cache/__init__.py"
touch "$BASE/shared/infra/cache/cleaner.py"

echo "Estrutura criada com sucesso: $BASE"