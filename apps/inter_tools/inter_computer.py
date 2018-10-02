from typing import Dict
from apps.scoring import Multiscale


class InterpretationComputer:
    """
    Вычислитель интерпретации. Переводит сырой/структурированный цифровой
    след в элементы цифрового профиля
    """
    def __init__(self, config:Dict):
        self.config = config
        self.processors = []
        self.aggregator = None

    @classmethod
    def get_config_args(cls) -> Dict[str, str]:
        """
        Возвращает словарь используемых ключей в config
        с пояснением их типа и значения
        """
        raise NotImplemented

    @classmethod
    def get_name_descr(cls):
        """
        Дескриптор вычислителя - строка, по которой
        его можно зарегистрировать.
        """
        return NotImplemented

    def compute(self, **kwargs) -> Multiscale:
        """
        Вычисляет цифровой профиль в виде Multiscale.
        Вычисление состоит из этапов:
        1. Получение сырого цифрового следа: подтягивание извне/парсинг kwargs
        2. Перевод цифрового следа обработчиками
        3. Агрегация результатов обработки
        Если обработка выполняется на стороне образовательной активности, то
        выполняется только 3 этап
        """
        raise NotImplemented
