---
trigger: always_on
---

# output-stage

## Responsabilidade

O output tem responsabilidade única: receber os dados extraídos brutos, transformá-los em dados limpos, tipados e padronizados, montar a coleção final de resultados e aplicar filtros e projeção de campos antes de retornar ao cliente. Remove sujeira, converte tipos, preenche campos ausentes com `null` e garante que a saída sempre segue o contrato definido pelo módulo.

## Classes

### `service/service.py`
- Orquestra a etapa.
- Recebe os dados brutos do `main.py`, utiliza o `mapper` para converter cada item e o `validator` para garantir o schema final.
- Retorna a coleção de `ResponseTransfer` pronta para serialização.
- Herda de `BaseOutput` e implementa `_process(raw_data)`.
- Concentra também a aplicação de filtros e projeção de campos sobre a coleção de resultados. Como essa lógica opera sobre o resultado já serializado, pode ser exposta como função(ões) auxiliar(es) no próprio arquivo do `service`, reutilizável tanto no caminho de pipeline executado quanto no caminho de cache hit.

### `mapper/mapper.py`
- Converte o `RequestTransfer` do extractor em `ResponseTransfer`.
- Aplica todas as transformações campo a campo (limpeza, conversão de tipo, normalização) conforme as regras definidas pelo módulo.
- Método principal: `map[Entidade]`, conforme a entidade alvo do módulo.

### `validator/validator.py`
- Valida o `ResponseTransfer` final antes de retornar ao cliente.
- Garante que campos obrigatórios estão presentes e os tipos estão corretos.
- Os campos obrigatórios são definidos pelo módulo.
- Método principal: `validateOutput(transfer)`.

### `transfer/response_transfer.py`
- DTO interno de saída do pipeline.
- Carrega os dados limpos, tipados e prontos para serialização.
- Implementa o método `toJson()`, que serializa o transfer em dicionário.
- Os atributos, seus getters, setters e o método `toJson()` são definidos pelo módulo conforme o contrato de saída estabelecido em sua documentação.

### `exception/exception.py`
- Contém os erros específicos do output.
- Herda de `BaseApiException`.
- Os códigos de erro são definidos pelo módulo.

## Filtros, Limite e Projeção

- Filtros, `limit` e projeção de campos (`fields`) são aplicados pelo output sobre o resultado já mapeado.
- A ordem de aplicação é fixa: **filtros → limite → projeção**.
- O detalhamento desse comportamento está em `filters-projection-and-limit.md`.

## Tabela de Classes

| Classe                       | Presente no Output |
|------------------------------|--------------------|
| `configuration`              | Não                |
| `service`                    | Sim                |
| `validator`                  | Sim                |
| `repository`                 | Não                |
| `transfer/request_transfer`  | Não                |
| `transfer/response_transfer` | Sim                |
| `mapper`                     | Sim                |
