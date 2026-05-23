---
trigger: always_on
---

# filters-projection-and-limit

## Visão Geral

Além de `query`, o schema de entrada de um módulo pode aceitar campos opcionais que moldam a resposta sem alterar o scraping:

- **`filters`** — critérios que removem itens do conjunto de resultados (ex: faixa de preço, atributos booleanos).
- **`limit`** — teto inteiro positivo para o número de itens retornados.
- **`fields`** — lista de campos a projetar; quando omitida, todos os campos do contrato de saída são retornados.

## Declaração e Aplicação

- Esses campos são **declarados e validados** pelos schemas Pydantic de entrada, no `main.py` do módulo — ver `request-schema.md`.
- Esses campos são **aplicados** pelo `output`, sobre o resultado já mapeado.
- A ordem de aplicação é fixa e inviolável: **filtros → limite → projeção**.
- Os campos aceitos, seus tipos e seus efeitos são definidos pelo módulo em sua documentação.

## Projeção e `AllowedField`

- Todo módulo que suportar o campo `fields` deve declarar um `AllowedField` (`Literal` tipado) no `main.py` do módulo.
- O Pydantic valida os valores de `fields` contra esse `Literal`, rejeitando com `422` qualquer campo não declarado.
- A projeção em si é responsabilidade do `output`.

## Relação com o Cache

- O cache armazena sempre o resultado **completo e não-filtrado** do pipeline.
- Filtros, limite e projeção são aplicados na montagem da resposta — tanto no caminho de cache hit quanto no de pipeline executado.
- Isso permite que a mesma entrada de cache atenda requisições com filtros diferentes.
- Ver `cache-rules.md`.
