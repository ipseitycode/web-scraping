---
trigger: always_on
---

# module-and-domain-creation

## Como Adicionar um Novo Módulo

1. Criar a pasta do novo alvo dentro do domínio correspondente.
2. Replicar exatamente a estrutura de pastas e classes definida em `project-structure.md`, incluindo um `__init__.py` vazio em cada pasta.
3. Documentar o módulo: contrato de entrada, contrato de saída, seletores, paginação, estratégia de cache e códigos de exception.
4. Implementar cada classe das três etapas, herdando das respectivas classes base em `shared/base/`.
5. Definir os schemas Pydantic do payload no `main.py` do módulo (ver `request-schema.md`).
6. Adaptar a `configuration` com os parâmetros de acesso do novo site.
7. Adaptar o `service` do extractor com os seletores específicos do novo site.
8. Adaptar o `mapper` do output com as regras de normalização do novo site.
9. Criar o `.env` e o `settings.py` do módulo com sua configuração operacional.
10. Declarar o objeto `router` no `main.py` do módulo, com a rota `/{dominio}/{modulo}`.
11. Opcionalmente, declarar um `jobs.py` com `register_jobs(scheduler)` para tarefas agendadas (ver `scheduled-jobs.md`).
12. Opcionalmente, declarar um `requirements.txt` do módulo com dependências exclusivas.

## Como Adicionar um Novo Domínio

1. Criar a pasta do novo domínio na raiz do projeto com um `__init__.py` vazio.
2. Criar os módulos dentro do domínio seguindo a mesma hierarquia definida em `project-structure.md`.
3. Todos os módulos do novo domínio seguem exatamente a mesma estrutura universal.

## Documentação Obrigatória por Módulo

Cada módulo deve conter um `MAP.md` — documentação das regras técnicas e conceituais do módulo para scraping: campos, seletores CSS, paginação, comportamento específico do site, cache, contrato de entrada, contrato de saída e códigos de exception.

## `main.py` da Raiz — Descoberta Automática

- O `main.py` da raiz tem responsabilidades fixas: gerenciar o agendador de tarefas, registrar o middleware de segurança, registrar o handler global de exceções e descobrir e registrar automaticamente os routers e jobs de todos os módulos.
- Nunca adicione lógica de negócio, regras de domínio ou qualquer outro código neste arquivo.
- O `main.py` da raiz **não conhece módulos específicos** e **não é editado quando um novo módulo é adicionado**.
- Ele varre o projeto em busca dos arquivos `main.py` e `jobs.py` dos módulos e os registra de forma genérica.
- Para que um módulo seja descoberto, basta seu `main.py` expor um objeto `router`. O prefixo `/web-scraping` é aplicado automaticamente no registro.
