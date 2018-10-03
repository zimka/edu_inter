from typing import Dict
from apps.scoring import Multiscale


class InterpretationComputer:
    """
    Вычислитель интерпретации. Переводит сырой/структурированный цифровой
    след в элементы цифрового профиля.
    Обработка сырого цифрового следа происходит в списке processors, аггрегация
    в методе .aggregate
    """
    DP_FORMAT = None

    def __init__(self, config:Dict):
        self.config = config
        self.processors = []

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

    def aggregate(self, **kwargs: Multiscale) -> DP_FORMAT:
        """
        Возвращает результат интерпретации в формате метамодели.
        Получает результаты обработки в виде различных подклассов
        Multiscale и компилирует в одну Multiscale, соответствующую
        метамодели интерпретации
        """
        raise NotImplemented

    def process(self, content) -> Dict[str, Multiscale]:
        """
        Применяет все обработчики к соответствующему разделу контента.
        """
        results = {}
        for proc in self.processors:
            selector_key = proc.get_selector_name()
            related_content = content.get(selector_key)
            results[selector_key] = proc.apply(related_content)
        return results