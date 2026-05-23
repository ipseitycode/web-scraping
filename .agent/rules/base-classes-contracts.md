---
trigger: always_on
---

# base-classes-contracts

## Regra Geral

- Todo módulo que implementar um downloader, extractor ou output deve herdar da respectiva classe base em `shared/base/`.
- Nunca implemente uma etapa sem herdar da classe base correspondente.
- As classes base encapsulam comportamentos universais — como retry e logging — no método público.
- O módulo implementa apenas o método interno (`_fetch`, `_extract` ou `_process`), contendo exclusivamente a lógica específica do site alvo.
- Nunca sobrescreva o método público da classe base. Apenas implemente o método abstrato interno.

## Contrato de `BaseDownloader`

- O construtor recebe os parâmetros de retry e delay. O `service` do downloader os repassa a partir da configuração do módulo.
- O método público `executeDownload` aplica retry automático com delay entre tentativas — lógica universal.

```python
# shared/base/base_downloader.py
class BaseDownloader(ABC):

    def __init__(self, retry_attempts: int, delay_seconds: int):
        self.__retry_attempts = retry_attempts
        self.__delay_seconds = delay_seconds

    def executeDownload(self, request):
        # retry automático com delay entre tentativas — lógica universal
        ...

    @abstractmethod
    def _fetch(self, request):
        # implementado pelo módulo: faz a requisição HTTP de fato
        pass
```

## Contrato de `BaseExtractor`

- Não possui construtor. O método público `executeExtraction` aplica logging universal.

```python
# shared/base/base_extractor.py
class BaseExtractor(ABC):
    def executeExtraction(self, raw_content):
        # logging universal
        ...

    @abstractmethod
    def _extract(self, raw_content):
        # implementado pelo módulo: aplica os seletores no conteúdo bruto
        pass
```

## Contrato de `BaseOutput`

- Não possui construtor. O método público `executeOutput` aplica logging universal.

```python
# shared/base/base_output.py
class BaseOutput(ABC):
    def executeOutput(self, raw_data):
        # logging universal
        ...

    @abstractmethod
    def _process(self, raw_data):
        # implementado pelo módulo: converte dados brutos em ResponseTransfer
        pass
```
