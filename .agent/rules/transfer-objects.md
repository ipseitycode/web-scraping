---
trigger: always_on
---

# transfer-objects

## Schema de Entrada × `transfer` — Distinção Obrigatória

São camadas diferentes, com responsabilidades diferentes, e nunca devem ser confundidas.

- O **schema de entrada** é o **schema HTTP do payload**. Usa Pydantic. Valida o que o consumidor externo envia no corpo do POST. É declarado no `main.py` do módulo. Ver `request-schema.md`.
- O **`transfer`** é o **DTO interno do pipeline**. É uma classe Python pura. Transporta dados entre as etapas. Nunca usa Pydantic.

O `main.py` do módulo recebe o payload validado e, a partir dele, popula o `RequestTransfer`. O Pydantic nunca cruza a fronteira interna do pipeline; os transfers nunca aparecem na borda HTTP.

## Regra Geral dos Transfers

- Todos os DTOs (transfers) são implementados como classes Python puras.
- Nunca use dataclasses, Pydantic ou bibliotecas externas para implementar transfers.
- Todos os atributos devem ser privados (prefixo `__`).
- Toda propriedade privada deve ter getter e setter explícito.
- O `RequestTransfer` transporta dados de entrada ou dados extraídos brutos — nunca dados tratados.
- O `ResponseTransfer` transporta dados limpos, tipados e prontos para serialização.

## Contrato Base do `RequestTransfer` (Downloader)

```python
class RequestTransfer:
    def __init__(self):
        self.__query = None
        self.__domain = None
        self.__target = None
        self.__filters = {}

    def getQuery(self): return self.__query
    def setQuery(self, query: str): self.__query = query

    def getDomain(self): return self.__domain
    def setDomain(self, domain: str): self.__domain = domain

    def getTarget(self): return self.__target
    def setTarget(self, target: str): self.__target = target

    def getFilters(self): return self.__filters
    def setFilters(self, filters: dict): self.__filters = filters
```

## `RequestTransfer` do Extractor

- Carrega os campos no estado exato em que foram encontrados no conteúdo, sem nenhum tratamento.
- Os atributos desse transfer correspondem aos campos definidos pelo módulo.
- Segue o mesmo padrão de implementação: atributos privados, getters e setters.

## `ResponseTransfer` do Output

- Carrega os dados limpos, tipados e prontos para serialização.
- Deve implementar o método `toJson()`, que serializa o transfer em dicionário.
- Os atributos, seus getters, setters e o método `toJson()` são definidos pelo módulo conforme o contrato de saída estabelecido em sua documentação.
