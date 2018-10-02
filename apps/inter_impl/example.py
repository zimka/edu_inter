import numpy as np
from apps.inter_tools import InterpretationComputer, Processor, Aggregator
from apps.scoring.scorer import IntTypedScorer
from apps.scoring import create_multiscale

ExampleResultScale = create_multiscale(name="Example", keys=["data_analytic", "community_leader"])
MathHumanityScale = create_multiscale(name="MathHumanity", keys=["math", "humanity"])
ArchetypesScale = create_multiscale(name="Archetype", keys=["fighter", "visionary", "chaser"])


class ExampleAgregator(Aggregator):
    """
    Пример агрегатора, собирающего из оценки по математике и значений архетипов
    значения цифрового профиля по ключам "Дата-аналитик" и "Лидер сообществ"
    """
    DP_FORMAT = ExampleResultScale

    @classmethod
    def get_config_args(cls):
        return {
            "weight_math_question": "вес вопроса по математике",
            "weight_arch_questions": "вес теста про архетипы",
        }

    def get_dp(self, math_ms, arch_ms):
        math_weight = self.config.get("weight_math_question", 1)
        arch_weight = self.config.get("weight_arch_questions", 1)
        arch_matrix = np.array(
            [[1, 1, 1],
             [1, 1, 1]])
        return ExampleResultScale.from_numeric(
            math_ms.numeric * math_weight + np.dot(arch_matrix, arch_ms.numeric * arch_weight)
        )


class ExampleInterpretationComputer(InterpretationComputer):
    """
    Пример вычислителя интерпретации
    """
    def __init__(self, config):
        super().__init__(config)
        self.aggregator = ExampleAgregator(config=config)
        self.processors = [
            Processor([
                IntTypedScorer.check_equals(9,   MathHumanityScale(math=3),              42),
                IntTypedScorer.check_greater(10, MathHumanityScale(math=-5, humanity=5), 42)
            ], scale=MathHumanityScale)
        ]

    @classmethod
    def get_config_args(cls):
        # TODO: аргументы лучше вытягивать без указания элементов явно
        args = {
            "id_math_question": "uuid вопроса по математике",
            "source_math_question": "url откуда брать ответы на вопрос по математике",
        }
        args.update(ExampleAgregator.get_config_args())
        return args

    @classmethod
    def get_name_descr(cls):
        return "example_ic"

    def load(self, **kwargs):
        "Подгрузка данных для интерпретации. В данном случае - фальшивая"

        math_raw_content = [
            {
                "question": {
                    "title": "Чему равно: 5 + 2 * 2",
                    "uuid": "42"
                },
                "answers": [
                    "14"
                ]
            },
            {
                "question": {
                    "title": "Ответ на этот вопрос не будет оцениваться, т.е. uuid не указан в оценщиках",
                    "uuid": "0"
                },
                "answers": [
                    ""
                ]
            }
        ]
        arch_structured_content = {
            "visionary": 3,
            "fighter": -1,
            "chaser": 1
        }
        return {
            "math": math_raw_content,
            "arch": arch_structured_content
        }

    def compute(self, user_uid=None, **kwargs):
        content = self.load(user_uid=user_uid)
        math_ms = self.processors[0].get_structured(content['math'])
        arch_ms = ArchetypesScale(**content["arch"])
        return self.aggregator.get_dp(math_ms=math_ms, arch_ms=arch_ms)
