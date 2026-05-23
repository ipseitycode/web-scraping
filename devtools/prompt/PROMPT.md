# PROMPT BASE

# Projeto: web-scraping-api

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 1. IDENTIFICAÇÃO DO MÓDULO

Domínio:
[dominio]

Módulo:
[modulo]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 2. CONTEXTO

O `web-scraping-api` é uma API de web scraping modular e escalável. Cada módulo representa um site alvo dentro de um domínio e segue uma arquitetura universal obrigatória composta por três etapas sequenciais: downloader → extractor → output, orquestradas pelo `main.py` do módulo.

Todo o código gerado deve respeitar dois documentos que juntos formam a única fonte de verdade deste pipeline:

- `.agent/rules/` — conjunto de arquivos que definem os contratos, convenções e comportamentos universais que todo código do projeto deve seguir. Leia todos os arquivos desta pasta.
- `[dominio]/[modulo]/MAP.md` — documento que define as regras técnicas e conceituais específicas do módulo: campos, seletores CSS, exceções, paginação, cache, contrato de entrada e contrato de saída.

Nenhum agente inventa, infere ou toma decisões fora do que está documentado nessas duas fontes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 3. ORQUESTRAÇÃO DE AGENTES (SEQUENCIAL — SEGUIR OBRIGATORIAMENTE)

Este prompt orquestra a execução dos agentes na ordem abaixo.
Cada etapa só inicia após a conclusão total da etapa anterior.
Nenhum agente pode pular etapas, agir fora de ordem ou iniciar sem confirmação da etapa anterior.

────────────────────────────────
ETAPA 1 — AGENT-CREATOR
────────────────────────────────

Responsabilidade: escrever o código de todos os arquivos do módulo.

Antes de qualquer geração:

- Leia COMPLETAMENTE: .agent/skills/agent-creator/SKILL.md
- Leia TODOS os arquivos em: .agent/rules/
- Leia COMPLETAMENTE: [dominio]/[modulo]/MAP.md
- A SKILL, as rules e o MAP são soberanos sobre qualquer outra instrução.

Execute na seguinte ordem:

1. Escrever o código dentro dos arquivos existentes nos caminhos abaixo, respeitando a ordem de dependência:

    [dominio]/[modulo]/.env
    [dominio]/[modulo]/requirements.txt
    [dominio]/[modulo]/shared/config/settings.py
    [dominio]/[modulo]/shared/infra/cache/cleaner.py
    [dominio]/[modulo]/downloader/transfer/request_transfer.py
    [dominio]/[modulo]/downloader/configuration/configuration.py
    [dominio]/[modulo]/downloader/exception/exception.py
    [dominio]/[modulo]/downloader/repository/repository.py
    [dominio]/[modulo]/downloader/validator/validator.py
    [dominio]/[modulo]/downloader/service/service.py
    [dominio]/[modulo]/extractor/transfer/request_transfer.py
    [dominio]/[modulo]/extractor/exception/exception.py
    [dominio]/[modulo]/extractor/validator/validator.py
    [dominio]/[modulo]/extractor/service/service.py
    [dominio]/[modulo]/output/transfer/response_transfer.py
    [dominio]/[modulo]/output/exception/exception.py
    [dominio]/[modulo]/output/mapper/mapper.py
    [dominio]/[modulo]/output/validator/validator.py
    [dominio]/[modulo]/output/service/service.py
    [dominio]/[modulo]/main.py
    [dominio]/[modulo]/jobs.py
    [dominio]/[modulo]/MAP.md
    [dominio]/[modulo]/README.md
    [dominio]/[modulo]/VALIDATION_REPORT.md

2. Não criar pastas ou arquivos além dos especificados. Apenas escrever.
3. Não explicar. Não justificar. Entregar apenas os arquivos escritos.

Conclusão da ETAPA 1: todos os arquivos escritos em disco com sucesso.

────────────────────────────────
ETAPA 2 — AGENT-VALIDATOR
────────────────────────────────

Responsabilidade: validar se o código gerado está em conformidade com as fontes de verdade.

Inicia somente após a conclusão confirmada da ETAPA 1.

Antes de qualquer validação:

- Leia COMPLETAMENTE: .agent/skills/agent-validator/SKILL.md
- Leia TODOS os arquivos em: .agent/rules/
- Leia COMPLETAMENTE: [dominio]/[modulo]/MAP.md
- A SKILL, as rules e o MAP são soberanos sobre qualquer outra instrução.

Execute na seguinte ordem:

1. Ler todos os arquivos escritos na ETAPA 1.
2. Validar cada arquivo contra as rules e o MAP simultaneamente.
3. Escrever o resultado no arquivo:

    [dominio]/[modulo]/VALIDATION_REPORT.md

────────────────────────────────
CAMINHO OK (STATUS: APPROVED):

- Encerrar o pipeline.
- Resultado: CONCLUÍDO.
────────────────────────────────
CAMINHO NOK (STATUS: REJECTED):
- O VALIDATION_REPORT.md deve estar escrito em disco com todos os erros detalhados antes de acionar a ETAPA 3.
- Somente após confirmação de escrita, acionar a ETAPA 3.
────────────────────────────────

Conclusão da ETAPA 2: VALIDATION_REPORT.md escrito em disco com sucesso.

────────────────────────────────
ETAPA 3 — AGENT-BROKER
────────────────────────────────

Responsabilidade: corrigir exatamente o que foi reportado pelo agent-validator.

Inicia somente após confirmação de escrita do VALIDATION_REPORT.md com STATUS: REJECTED.
Não inicia se o resultado da ETAPA 2 for STATUS: APPROVED.

Antes de qualquer correção:

- Leia COMPLETAMENTE: .agent/skills/agent-broker/SKILL.md
- Leia TODOS os arquivos em: .agent/rules/
- Leia COMPLETAMENTE: [dominio]/[modulo]/MAP.md
- Leia COMPLETAMENTE: [dominio]/[modulo]/VALIDATION_REPORT.md
- A SKILL, as rules, o MAP e o VALIDATION_REPORT são soberanos sobre qualquer outra instrução.

Execute na seguinte ordem:

1. Ler o VALIDATION_REPORT.md e identificar todos os erros listados.
2. Corrigir exatamente o que está descrito, nos arquivos apontados.
3. Não alterar nada além do que está descrito no relatório.
4. Não criar arquivos adicionais.
5. Ao finalizar todas as correções, limpar o VALIDATION_REPORT.md deixando-o vazio.

Conclusão da ETAPA 3: arquivos corrigidos escritos em disco com sucesso.
Resultado: CONCLUÍDO.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 4. REGRAS GLOBAIS DO PIPELINE

- Nenhum agente age fora de sua etapa.
- Nenhum agente escreve código sem ter lido as rules e o MAP primeiro.
- Nenhum agente corrige sem VALIDATION_REPORT.md. Nenhum agente valida sem arquivos gerados.
- A ordem ETAPA 1 → ETAPA 2 → ETAPA 3 é inviolável.
- Em caso de falha bloqueante em qualquer etapa, o pipeline para imediatamente e reporta a falha.
- Nenhuma etapa simula sucesso. Confirmação de sucesso = arquivo escrito em disco e verificado.
- Nenhum agente inventa, infere ou decide fora do que está documentado nas fontes de verdade.