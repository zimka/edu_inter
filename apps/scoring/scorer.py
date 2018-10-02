from .multiscale import Multiscale


class Scorer:
    """
    Оценщик цифрового следа. Принимает контент и возвращает оценку
    в формате Multiscale, применяя какую-то внутреннюю логику по ее
    выставлению
    """
    def apply(self, content)-> Multiscale:
        raise NotImplemented


class TypedScorer(Scorer):
    """
    Типизированный оценщик - оценивает цифровой след определенного типа.
    "Тип" относится не к content, а к ._select_related(content).
    Используется следующая логика оценивания: если check_function возвращает True
    на _select_related(content), то apply возвращает prize, иначе возвращается zero.
    """
    SCORE_TYPE = None

    def __init__(self, check_function, prize: Multiscale, **kwargs):
        self.check_function = check_function
        self.prize = prize

    def apply(self, content) -> Multiscale:
        related_content = self._select_related(content)
        zero = self.prize(0)
        if not related_content:
            return zero
        if not isinstance(related_content, self.SCORE_TYPE):
            # TODO: сделать что-нибудь
            return zero
        if not self.check_function(related_content):
            return zero
        return self.prize

    def _select_related(self, content) -> SCORE_TYPE:
        """
        Выбирает из всего цифрового следа определенную часть, относящуюся
        к логике оценивания. Например, выбирает один ответ на один вопрос
        теста из всех ответов за тест.
        """
        raise NotImplemented


class IntTypedScorer(TypedScorer):
    """
    Пример типизированного оценщика для вопроса со вводом числа.
    """
    SCORE_TYPE = int

    def __init__(self, check_function, prize: Multiscale, *, question_id=None):
        super().__init__(check_function, prize)
        self.question_id = question_id

    def _select_related(self, content):
        try:
            for item in content:
                question = item.get("question", {})
                if question.get("uuid") == str(self.question_id):
                    return int(item['answers'][0])
        except (ValueError, TypeError, KeyError):
            # TODO: несоответствие типов должно логироваться
            return None

    @classmethod
    def check_greater(cls, threshold_value, prize, question_id):
        return cls(lambda x: x > threshold_value, prize, question_id=question_id)

    @classmethod
    def check_equals(cls, target_value, prize, question_id):
        return cls(lambda x: x == target_value, prize, question_id=question_id)
