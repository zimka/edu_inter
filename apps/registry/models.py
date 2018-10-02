from django.db import models
from apps.inter_impl import AVAILABLE_INTERPRETER_DESCR_CHOICES, AVAILABLE_INTERPRETER_IMPLEMENTAIONS
from jsonfield import JSONField


class ContextTemp(models.Model):
    # Должно быть в edu_coresys
    pass


class MetamodelTemp(models.Model):
    # Должно быть в edu_coresys
    pass


class InterpreterRegistry(models.Model):
    """
    Объекты модели создаются в админке с указанием конфига.
    Вычислитель выбирается из числа доступных.
    """
    metamodel = models.ForeignKey(MetamodelTemp, on_delete=models.CASCADE)
    context = models.ForeignKey(ContextTemp, on_delete=models.CASCADE)
    compute_descr = models.CharField(choices=AVAILABLE_INTERPRETER_DESCR_CHOICES, max_length=32)
    config = JSONField(default={})
    is_valid = models.BooleanField(default=False)

    def compute(self, **kwargs):
        inter_computer_cls = AVAILABLE_INTERPRETER_IMPLEMENTAIONS.get(self.compute_descr, None)
        if inter_computer_cls is None:
            self.is_valid = False
            self.save()
            return
        ic = inter_computer_cls(self.config)
        result = ic.compute(**kwargs)
        self.handle_ic_result(result)

    def handle_ic_result(self, result):
        """
        Сохраняем результат интерпретации в dp / куда-то еще
        """
        pass