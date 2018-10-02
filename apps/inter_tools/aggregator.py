from typing import Dict
from apps.scoring.multiscale import Multiscale


class Aggregator:
    """
    Агрегатор результатов обработки цифрового следа.
    Получает результаты обработки в виде различных подклассов
    Multiscale и компилирует в одну Multiscale, соответствующую
    метамодели интерпретации
    """

    DP_FORMAT = None

    def __init__(self, config, **kwargs):
        """
        Можно передавать различные параметры агрегации, например, веса
        различных оценок в общей оценке
        """
        self.config = config

    def get_dp(self, **kwargs: Multiscale) -> DP_FORMAT:
        """
        Возвращает результат интерпретации в формате метамодели
        """
        raise NotImplemented