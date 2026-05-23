import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseOutput(ABC):

    def executeOutput(self, raw_data):
        logger.info(f"[output] processing {len(raw_data) if isinstance(raw_data, list) else 1} item(s)")
        result = self._process(raw_data)
        logger.info("[output] output ready")
        return result

    @abstractmethod
    def _process(self, raw_data):
        """
        Converte os dados brutos do extractor em ResponseTransfer(s) limpos e tipados.
        Implementado por cada módulo conforme as regras de normalização do site alvo.
        """
        pass