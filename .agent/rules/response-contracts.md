---
trigger: always_on
---

# response-contracts

## Contrato de Resposta de Sucesso

O envelope de resposta de sucesso é universal para todos os módulos. Nunca altere a estrutura deste envelope.

```json
{
    "success": true,
    "domain": "{dominio}",
    "target": "{modulo}",
    "query": "{termo buscado}",
    "total": 48,
    "cached": false,
    "results": [
        { ... }
    ]
}
```

- O schema de cada objeto dentro de `results` é definido pelo módulo, conforme seu contrato de saída.
- O campo `cached` indica se o resultado veio do cache (`true`) ou do pipeline executado (`false`).
- O campo `total` representa o número de itens em `results` após filtros, limite e projeção.

## Contrato de Resposta de Erro

Toda resposta de erro deve seguir o formato definido em `exception-contract.md`. Consulte esse arquivo para o schema completo e os status HTTP aplicáveis.

## Regras de Serialização

- O `ResponseTransfer` implementa `toJson()`, usado para serializar cada item da coleção final.
- Nunca serialize o `ResponseTransfer` diretamente sem passar pelo método `toJson()`.
- A API não persiste definitivamente os dados. A responsabilidade de persistir os dados retornados é do sistema consumidor.
