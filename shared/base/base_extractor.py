import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseExtractor(ABC):

    def executeExtraction(self, raw_content):
        logger.info("[extractor] starting extraction")
        result = self._extract(raw_content)
        logger.info(f"[extractor] extraction complete — {len(result) if isinstance(result, list) else 1} item(s)")
        return result

    @abstractmethod
    def _extract(self, raw_content):
        """
        Aplica os seletores CSS/XPath no conteúdo bruto e retorna os dados extraídos.
        Implementado por cada módulo conforme a estrutura HTML do site alvo.
        Deve retornar lista de dicts com os campos brutos encontrados.
        """
        pass