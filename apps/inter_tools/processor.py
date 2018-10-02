from typing import List
from apps.scoring import Multiscale
from apps.scoring.scorer import Scorer


class Processor:
    """
    Обработчик цифрового следа. Рассчитывает по сырому ЦС
    структурированное представление в виде Multiscale.
    Параметризуется списком Scorer, которые должны все возвращать
    один подкласс Multiscale.
    Пример использования: для диагностического теста задется ряд
    Scorer-ов, которые применяются к результатам прохождения
    теста определенного пользователя.
    """

    def __init__(self, scorers: List[Scorer], scale: Multiscale):
        self.scorers = scorers
        self.scale = scale

    def get_structured(self, content) -> Multiscale:
        total = self.scale.from_numeric(0)
        try:
            for sc in self.scorers:
                total += sc.apply(content)
        except TypeError:
            # TODO: в составе оценщиков есть возвращающей результат в разном формате
            return self.scale(0)
        return total
