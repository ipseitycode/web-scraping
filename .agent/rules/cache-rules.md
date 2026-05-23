---
trigger: always_on
---

# cache-rules

## Responsabilidade

- O cache é responsabilidade do **downloader**, gerenciado pelo seu `repository`.
- Nunca implemente lógica de cache no extractor, no output ou no `main.py`.

## Localização

- O cache é armazenado localmente no módulo em `shared/infra/cache/`, em arquivos JSON no disco.
- Cada entrada guarda um timestamp de gravação, usado para calcular a expiração contra o TTL configurado.
- Não há dependência de serviços externos como Redis.

## Fluxo Obrigatório

```
main.py aciona o repository do downloader
     ↓
repository verifica o cache local
     ↓ (hit — resultado recente encontrado)
retorna o resultado completo sem executar o pipeline
     ↓ (miss — cache expirado ou inexistente)
executa o pipeline completo (downloader → extractor → output)
     ↓
repository grava o resultado completo no cache
     ↓
main.py aplica filtros/limite/projeção e retorna o JSON ao cliente
```

- Toda vez que um módulo for acionado, é obrigatório verificar o cache antes de iniciar o pipeline.
- Em caso de cache hit, o pipeline completo (downloader → extractor → output) não deve ser executado.
- O repository grava o resultado no cache após o output processar e retornar a coleção final.

## Conteúdo do Cache

- O cache armazena sempre o resultado **completo e não-filtrado** do pipeline.
- Filtros, `limit` e projeção (`fields`) são aplicados na montagem da resposta — tanto no cache hit quanto no pipeline executado.
- Isso permite que a mesma entrada de cache atenda requisições com filtros diferentes.

## Limpeza de Cache

- `shared/infra/cache/cleaner.py` contém a rotina de housekeeping que remove do disco entradas de cache expiradas ou corrompidas.
- A limpeza é executada de forma agendada (ver `scheduled-jobs.md`), nunca no caminho de uma requisição.

## Configuração

- A estratégia de chave de cache (quais parâmetros a compõem) é definida pelo módulo.
- O TTL padrão é definido pelo módulo.
- O comportamento global do cache (habilitado/desabilitado e expiração) é controlado pela configuração do módulo, em `{modulo}/.env` e `{modulo}/shared/config/settings.py` — ver `settings-and-env.md`.
