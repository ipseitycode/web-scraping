---
trigger: always_on
---

# project-structure

## Hierarquia Conceitual

O projeto é organizado em exatamente cinco níveis hierárquicos. Nunca crie níveis intermediários ou alternativos.

1. **Projeto** — `web-scraping-api`: raiz de tudo.
2. **Pacote / Domínio** — agrupa módulos de um mesmo domínio de interesse.
3. **Módulo / Alvo** — representa um site ou fonte específica dentro de um domínio.
4. **Etapa** — `downloader`, `extractor`, `output`: as três fases universais e obrigatórias do pipeline.
5. **Classe** — `service`, `validator`, `exception`, etc.: a lógica interna de cada etapa.

## Regra do `__init__.py`

Todo diretório do projeto deve conter um arquivo `__init__.py` vazio. Isso é obrigatório para que o Python reconheça cada pasta como um pacote importável. Nenhum diretório pode existir sem ele. Nunca omita o `__init__.py` em nenhuma pasta, incluindo as mais profundas.

## Estrutura de Pastas

Replique exatamente esta estrutura para todo novo módulo. Nenhuma pasta ou arquivo extra deve ser criado fora do que está aqui definido.

```
web-scraping-api/
│
├── shared/
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── base_downloader.py
│   │   ├── base_extractor.py
│   │   └── base_output.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── base_exception.py
│   └── security/
│       ├── __init__.py
│       └── api_key_middleware.py
│
├── {dominio}/
│   ├── __init__.py
│   └── {modulo}/
│       ├── __init__.py
│       ├── downloader/
│       │   ├── __init__.py
│       │   ├── configuration/
│       │   │   ├── __init__.py
│       │   │   └── configuration.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── repository/
│       │   │   ├── __init__.py
│       │   │   └── repository.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── request_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── extractor/
│       │   ├── __init__.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── request_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── output/
│       │   ├── __init__.py
│       │   ├── exception/
│       │   │   ├── __init__.py
│       │   │   └── exception.py
│       │   ├── mapper/
│       │   │   ├── __init__.py
│       │   │   └── mapper.py
│       │   ├── service/
│       │   │   ├── __init__.py
│       │   │   └── service.py
│       │   ├── transfer/
│       │   │   ├── __init__.py
│       │   │   └── response_transfer.py
│       │   └── validator/
│       │       ├── __init__.py
│       │       └── validator.py
│       │
│       ├── shared/
│       │   ├── __init__.py
│       │   ├── config/
│       │   │   ├── __init__.py
│       │   │   └── settings.py
│       │   └── infra/
│       │       ├── __init__.py
│       │       └── cache/
│       │           ├── __init__.py
│       │           └── cleaner.py
│       │
│       ├── .env
│       ├── jobs.py
│       ├── main.py
│       ├── MAP.md
│       └── requirements.txt
│
├── .env
├── Dockerfile
├── install.sh
├── main.py
└── requirements.txt
```

## Arquivos Opcionais do Módulo

- `jobs.py` — declarado apenas por módulos que possuem tarefas agendadas.
- `requirements.txt` — declarado apenas por módulos com dependências exclusivas.

Todos os demais arquivos e pastas da estrutura são obrigatórios.

## Invariância da Estrutura

- Todos os módulos, independente do domínio, seguem exatamente a mesma estrutura de pastas, etapas e classes.
- O que muda entre módulos é exclusivamente a implementação interna de cada classe, adaptada às regras do site alvo.
- Nunca altere a estrutura universal para acomodar particularidades de um módulo.
- Todo diretório deve conter um `__init__.py` vazio, sem exceção.
