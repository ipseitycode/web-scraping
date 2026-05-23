---
trigger: always_on
---

# scheduled-jobs

## Tarefas Agendadas

- Um módulo pode declarar tarefas recorrentes — por exemplo, a limpeza periódica do cache.
- Para isso, expõe um arquivo `jobs.py` na raiz do módulo com uma função `register_jobs(scheduler)`.
- `jobs.py` é **opcional**: um módulo sem tarefas agendadas simplesmente não o declara.

## Contrato do `jobs.py`

```python
from {dominio}.{modulo}.shared.infra.cache.cleaner import clean_expired_cache

def register_jobs(scheduler):
    scheduler.add_job(clean_expired_cache, "cron", hour=3)
```

- A função `register_jobs(scheduler)` recebe o agendador compartilhado e registra nele as tarefas do módulo.
- A função e a assinatura têm nome fixo: o `main.py` da raiz só descobre módulos que exponham exatamente `register_jobs(scheduler)`.

## Agendador Global

- O `main.py` da raiz, em seu `lifespan`, cria um único `AsyncIOScheduler` (APScheduler).
- Ele descobre automaticamente todos os `jobs.py` dos módulos e chama o `register_jobs` de cada um, passando o scheduler compartilhado.
- O agendador é iniciado no startup e encerrado no shutdown da aplicação.
- O `main.py` da raiz nunca é editado para isso — a descoberta é genérica.

## Regras

- Tarefas agendadas executam fora do caminho de uma requisição HTTP.
- A rotina de limpeza de cache (`shared/infra/cache/cleaner.py`) é executada exclusivamente de forma agendada, nunca no caminho de uma requisição — ver `cache-rules.md`.
