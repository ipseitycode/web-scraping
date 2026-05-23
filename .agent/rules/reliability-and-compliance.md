---
trigger: always_on
---

# reliability-and-compliance

## Evasão de Bloqueio de IP

- Quando necessário, use proxies residenciais rotativos para evitar bloqueio de IP.
- A configuração de proxies é feita na `configuration` do downloader do módulo.

## Resolução de Captcha

- Quando necessário, integre com serviços especializados de resolução de captcha.
- Essa integração é responsabilidade do downloader do módulo.

## Mudança de Estrutura do Site

- Quando o site alvo muda seu HTML, o extractor para de funcionar.
- O `validator` do extractor é responsável por detectar essa condição.
- Ao detectar que os seletores não retornam os campos esperados, o `validator` deve lançar exception com código específico definido pelo módulo.

## Rate Limiting

- Configure delays entre requisições por meio da configuração do módulo (`{modulo}/.env` e `{modulo}/shared/config/settings.py`).
- Nunca faça requisições em rajada sem respeitar o delay configurado.

## Conformidade Legal

- Sempre respeite o arquivo `robots.txt` dos sites alvo.
- Siga as diretrizes da LGPD.
- A API não tem responsabilidade sobre o que o consumidor faz com os dados retornados.
