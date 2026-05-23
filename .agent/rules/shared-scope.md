---
trigger: always_on
---

# shared-scope

## `shared/` Global (raiz do projeto)

- A `shared/` global contém exclusivamente o que é relevante para o projeto inteiro, independente de qualquer domínio.
- Nunca adicione lógica de negócio específica de um módulo na `shared/` global.
- Contém apenas: classes base abstratas (`base/`), configuração de infraestrutura global (`config/`), contrato global de exceção (`exception/`) e segurança global da API (`security/`).

### Subpastas da `shared/` global

**`shared/base/`**
Classes abstratas que definem os contratos obrigatórios de cada etapa. Todo módulo que implementar downloader, extractor ou output deve herdar da respectiva classe base.

**`shared/config/`**
Contém `settings.py`, que lê o `.env` da raiz e expõe as variáveis de infraestrutura global como constantes Python. Nenhuma parte do sistema deve ler o `.env` diretamente — sempre importa de `settings.py`.

**`shared/exception/`**
Contém `base_exception.py`, que define o contrato global do JSON de erro. Todas as exceptions específicas das etapas herdam desta classe base.

**`shared/security/`**
Contém `api_key_middleware.py`, o middleware global de autenticação. Intercepta toda requisição antes de chegar a qualquer módulo. Nenhum módulo conhece ou depende deste arquivo. Nenhuma lógica de autenticação deve existir fora desta pasta.

## `shared/` Local (por módulo)

- Cada módulo possui sua própria pasta `shared/` para recursos internos compartilhados entre suas etapas.
- Nunca acesse o conteúdo da `shared/` local de um módulo a partir de outro módulo.
- Nunca acesse o conteúdo da `shared/` local de um módulo a partir do projeto global.
- A `shared/` local do módulo contém:
  - `config/settings.py` — carrega o `.env` do módulo e expõe sua configuração operacional como constantes Python.
  - `infra/cache/` — infraestrutura interna de cache do módulo, incluindo a rotina de limpeza (`cleaner.py`) e os arquivos JSON de cache gerados em tempo de execução.

## Isolamento entre Módulos

- A lógica de cada módulo é completamente isolada.
- Nenhum módulo acessa pastas ou classes de outro módulo.
- A única dependência cruzada permitida é o uso das classes base e da configuração global em `shared/`.
