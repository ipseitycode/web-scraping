#!/bin/bash
# Instala as dependências do projeto e dos módulos sem excessão, e os browsers do Playwright.
set -e

echo "Installing root dependencies..."
pip install -r requirements.txt

echo "Installing module dependencies..."
find . -name "requirements.txt" -not -path "./requirements.txt" | while read req; do
    echo "  -> $req"
    pip install -r "$req"
done

echo "Installing Playwright browsers..."
playwright install chromium

echo "Done."