"""
SCRIPT DE EXPLORAÇÃO — OLX
Bloco 2 do ROADMAP: descoberta de acesso, seletores e paginação.

Uso:
  python devtools/scripts/modules/script-olx-scraping.py <query> [--estado <slug>] [--paginas <n>] [--saida <arquivo.json>]

Exemplos:
  python devtools/scripts/modules/script-olx-scraping.py celular
  python devtools/scripts/modules/script-olx-scraping.py notebook --estado estado-ba
  python devtools/scripts/modules/script-olx-scraping.py iphone --estado estado-sp --paginas 3
  python devtools/scripts/modules/script-olx-scraping.py sofa --estado estado-rj --paginas 2 --saida resultado.json

Dependências:
  pip install playwright beautifulsoup4
  playwright install chromium
"""

import argparse
import json
import sys
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

BASE_URL       = "https://www.olx.com.br"
WAIT_SELECTOR  = "section.olx-adcard"
TIMEOUT_MS     = 30_000
DELAY_PAGINAS  = 2  # segundos

BROWSER_CONFIG = {
    "user_agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "viewport":   {"width": 1366, "height": 768},
    "locale":     "pt-BR",
    "timezone":   "America/Sao_Paulo",
    "launch_args": [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ],
}

# ---------------------------------------------------------------------------
# URL
# ---------------------------------------------------------------------------

def build_url(estado: str, query: str, pagina: int) -> str:
    slug = query.strip().replace(" ", "+")
    if pagina == 1:
        return f"{BASE_URL}/{estado}?q={slug}"
    return f"{BASE_URL}/{estado}?q={slug}&o={pagina}"

# ---------------------------------------------------------------------------
# Extração
# ---------------------------------------------------------------------------

def extract_text(element, selector: str) -> str | None:
    found = element.select_one(selector)
    return found.get_text(strip=True) if found else None


def extract_attr(element, selector: str, attr: str) -> str | None:
    found = element.select_one(selector)
    return found.get(attr) if found else None


def extract_cards(soup: BeautifulSoup) -> list[dict]:
    cards = soup.select("section.olx-adcard")

    if not cards:
        print("  [AVISO] Nenhum card encontrado — seletores podem estar desatualizados.", file=sys.stderr)
        return []

    print(f"  → Cards encontrados: {len(cards)}", file=sys.stderr)

    results = []
    for card in cards:
        title    = extract_text(card, "h2.olx-adcard__title")
        price    = extract_text(card, "h3.olx-adcard__price")
        url      = extract_attr(card, "a[data-testid='adcard-link']", "href")
        location = extract_text(card, "p.olx-adcard__location")
        date     = extract_text(card, "p.olx-adcard__date")
        image    = extract_attr(card, ".olx-adcard__media img", "src")

        installments_el = card.select_one("[data-testid='adcard-price-info']")
        installments = installments_el.get_text(strip=True) if installments_el else None

        badges_els = card.select(".olx-adcard__badges div")
        badges = [b.get_text(strip=True) for b in badges_els] if badges_els else None

        bullets = card.select(".olx-adcard__carousel--bullet")
        image_count = len(bullets) if bullets else None

        if not title or not url:
            print("  [DESCARTADO] Item sem título ou URL.", file=sys.stderr)
            continue

        results.append({
            "title":        title,
            "price":        price,
            "url":          url,
            "location":     location,
            "date":         date,
            "image":        image,
            "installments": installments,
            "badges":       badges,
            "image_count":  image_count,
        })

    return results

# ---------------------------------------------------------------------------
# Scraping com Playwright
# ---------------------------------------------------------------------------

def scrape(query: str, estado: str, paginas: int) -> list[dict]:
    all_items = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=BROWSER_CONFIG["launch_args"],
        )
        context = browser.new_context(
            user_agent=BROWSER_CONFIG["user_agent"],
            viewport=BROWSER_CONFIG["viewport"],
            locale=BROWSER_CONFIG["locale"],
            timezone_id=BROWSER_CONFIG["timezone"],
        )

        # Oculta navigator.webdriver
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = context.new_page()

        for pagina in range(1, paginas + 1):
            print(f"\n[Página {pagina}]", file=sys.stderr)

            url = build_url(estado, query, pagina)
            print(f"  → Acessando: {url}", file=sys.stderr)

            try:
                page.goto(url, timeout=TIMEOUT_MS)
                page.wait_for_selector(WAIT_SELECTOR, timeout=TIMEOUT_MS)
            except PlaywrightTimeoutError:
                print("  [FIM] Timeout aguardando cards — paginação encerrada.", file=sys.stderr)
                break

            soup  = BeautifulSoup(page.content(), "html.parser")
            items = extract_cards(soup)

            if not items:
                print("  [FIM] Página sem itens — paginação encerrada.", file=sys.stderr)
                break

            all_items.extend(items)

            if pagina < paginas:
                print(f"  → Aguardando {DELAY_PAGINAS}s...", file=sys.stderr)
                time.sleep(DELAY_PAGINAS)

        browser.close()

    return all_items

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Script de exploração de scraping — OLX Brasil"
    )
    parser.add_argument("query", help="Termo de busca (ex: celular, notebook)")
    parser.add_argument(
        "--estado",
        default="brasil",
        help="Slug do estado (ex: estado-ba, estado-sp). Padrão: brasil",
    )
    parser.add_argument(
        "--paginas",
        type=int,
        default=1,
        help="Número máximo de páginas a raspar. Padrão: 1",
    )
    parser.add_argument(
        "--saida",
        default=None,
        help="Arquivo JSON de saída. Se omitido, imprime no stdout.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  OLX Scraper — Exploração", file=sys.stderr)
    print(f"  Query:   {args.query}", file=sys.stderr)
    print(f"  Estado:  {args.estado}", file=sys.stderr)
    print(f"  Páginas: {args.paginas}", file=sys.stderr)
    print(f"{'='*50}", file=sys.stderr)

    all_items = scrape(args.query, args.estado, args.paginas)

    print(f"\n{'='*50}", file=sys.stderr)
    print(f"  Total extraído: {len(all_items)} itens", file=sys.stderr)
    print(f"{'='*50}\n", file=sys.stderr)

    output = json.dumps(all_items, ensure_ascii=False, indent=2)

    if args.saida:
        with open(args.saida, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"  Salvo em: {args.saida}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()