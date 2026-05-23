---
trigger: always_on
---

# extractor-stage

## Responsabilidade

O extractor tem responsabilidade única: ler o conteúdo bruto recebido do downloader e localizar os campos de interesse. Conhece a estrutura do HTML ou JSON do site alvo. Não limpa, não formata, não valida semanticamente — apenas extrai os campos no estado bruto em que estão. Os campos extraídos e os seletores utilizados são definidos pelo módulo.

## Classes

### `service/service.py`
- Orquestra a etapa.
- Recebe o conteúdo bruto do `main.py`, aplica os seletores específicos do site alvo e coleta os campos de interesse de cada item encontrado.
- Retorna os dados brutos extraídos para o `main.py`.
- Herda de `BaseExtractor` e implementa `_extract(raw_content)`.
- Nunca limpa, converte tipos ou transforma os dados — essa responsabilidade pertence ao output.

### `validator/validator.py`
- Valida se os campos obrigatórios foram extraídos antes de seguir para o output.
- Os campos considerados obrigatórios são definidos pelo módulo.
- Quando o site alvo muda seu HTML e os seletores param de funcionar, este validator detecta e lança exception com código específico.
- Método principal: `validateExtraction(data)`.

### `transfer/request_transfer.py`
- DTO interno de transporte dos dados extraídos brutos.
- Carrega os campos no estado exato em que foram encontrados no conteúdo, sem nenhum tratamento.
- Os atributos desse transfer correspondem aos campos definidos pelo módulo.
- Implementado como classe Python pura com atributos privados, getters e setters.

### `exception/exception.py`
- Contém os erros específicos do extractor.
- Herda de `BaseApiException`.
- Os códigos de erro são definidos pelo módulo.

## Tabela de Classes

| Classe                       | Presente no Extractor |
|------------------------------|-----------------------|
| `configuration`              | Não                   |
| `service`                    | Sim                   |
| `validator`                  | Sim                   |
| `repository`                 | Não                   |
| `transfer/request_transfer`  | Sim                   |
| `transfer/response_transfer` | Não                   |
| `mapper`                     | Não                   |
