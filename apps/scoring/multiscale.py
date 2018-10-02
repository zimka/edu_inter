import numbers
import numpy as np


class Multiscale:
    """
    Мультишкала - контейнер для именованных числовых значений с
    поддержкой математических операций.
    Разрешенные ключи определяются в __slots__.
    """
    __slots__ = tuple()
    _base_type = float

    def __init__(self, **kwargs: numbers.Number):
        for k in self.__slots__:
            setattr(self, k, kwargs.pop(k, 0))
        if len(kwargs):
            raise KeyError("Unknown keys: {}".format(kwargs))

    def items(self):
        """
        Аналогичный методу dict метод
        """
        return ((k, getattr(self, k)) for k in self.__slots__)

    @property
    def numeric(self) -> np.ndarray:
        """
        Численное представление для векторных операций
        """
        return np.array([getattr(self, k) for k in self.__slots__], dtype=self._base_type)

    @classmethod
    def from_numeric(cls, numeric):
        """
        Построение мультишкалы по ее численному представлению
        """
        if isinstance(numeric, numbers.Number):
            numeric = np.zeros(len(cls.__slots__), dtype=cls._base_type) + numeric

        if not isinstance(numeric, np.ndarray) or len(cls.__slots__) != len(numeric):
            raise TypeError("Wrong numeric representation")
        return cls(
            **dict((cls.__slots__[n], numeric[n]) for n in range(len(numeric)))
        )

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Can add only schemes")
        return self.from_numeric(self.numeric + other.numeric)

    def __str__(self):
        return "Multiscale<{name}>({items})".format(
            name=self.__class__.__name__,
            items=str(dict(self.items()))
        )

    def __bool__(self):
        """
        Возвращает False, если все значения - нули
        """
        return self.numeric.sum() != 0

    def __call__(self, value):
        return self.from_numeric(value)

def create_multiscale(name, keys):
    """
    Ручка для быстрого построения мультишкал
    """

    class current_multiscale(Multiscale):
        __slots__ = keys
    current_multiscale.__name__ = name

    return current_multiscale
