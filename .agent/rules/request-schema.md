---
trigger: always_on
---

# request-schema

## Schema de Entrada

- Cada módulo define o **schema HTTP do payload de entrada** usando modelos **Pydantic**.
- Esses schemas são declarados no `main.py` do módulo — o controller é o único arquivo que conhece e declara o contrato de entrada da API.
- Nunca crie uma camada, pasta ou arquivo separado para os schemas de entrada; eles pertencem ao `main.py` do módulo.
- O FastAPI valida o corpo do POST contra o schema antes de o controller executar qualquer lógica. Campos não previstos, tipos inválidos ou valores fora das restrições são rejeitados com `422` pelo próprio Pydantic.

## Schema de Entrada × `transfer`

- O **schema de entrada** é Pydantic, é declarado no `main.py` do módulo e valida o que o consumidor externo envia. Vive na borda da API.
- O **`transfer`** é o DTO interno do pipeline. É classe Python pura. Transporta dados entre as etapas.
- O Pydantic nunca cruza a fronteira interna do pipeline; os transfers nunca aparecem na borda HTTP.
- O `main.py` do módulo recebe o payload validado e, a partir dele, popula o `RequestTransfer`.
- Ver também `transfer-objects.md`.

## Campos do Payload

- `query` é o único campo sempre obrigatório.
- O módulo pode declarar campos opcionais — tipicamente `filters`, `fields` e `limit`.
- Os campos aceitos, seus tipos e restrições são definidos pelos schemas Pydantic do módulo.

## Regra do `AllowedField`

- Todo módulo que suportar o campo `fields` no payload deve declarar explicitamente um `AllowedField` — um `Literal` tipado com os campos permitidos para projeção — no `main.py` do módulo, junto aos demais schemas Pydantic de entrada.
- O Pydantic usa esse `Literal` para validar os valores de `fields` na borda da API, rejeitando com `422` qualquer campo não declarado.
- A projeção em si é responsabilidade do `output`, aplicada após filtros e limite.

## Convenções

- Os modelos Pydantic do schema de entrada seguem `PascalCase`.
- São classes puramente declarativas, sem métodos de lógica e sem o padrão de métodos prefixados das classes do pipeline.
- Ver `naming-conventions.md`.
