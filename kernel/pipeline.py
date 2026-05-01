"""
Pipeline — управляет последовательным выполнением агентов.

Это уже зачаток orchestration layer.
"""

from typing import Dict, Any

from kernel.agents.ingestion_agent import IngestionAgent
from kernel.agents.processing_agent import ProcessingAgent
from kernel.agents.generation_agent import GenerationAgent
from kernel.agents.style_agent import StyleAgent


class Pipeline:
    """
    Основной pipeline системы.
    """

    def __init__(self):
        # инициализируем агентов
        self.ingestion = IngestionAgent()
        self.processing = ProcessingAgent()
        self.generation = GenerationAgent()
        self.style = StyleAgent()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Запускает pipeline.

        :param input_data: входные данные
        :return: результат pipeline
        """

        print("🚀 [Pipeline] Starting...\n")

        data = self.ingestion.run(input_data)
        data = self.processing.run(data)
        data = self.generation.run(data)
        data = self.style.run(data)

        print("\n✅ [Pipeline] Finished")

        return data
