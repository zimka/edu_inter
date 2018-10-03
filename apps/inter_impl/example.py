import numpy as np
from apps.inter_tools import InterpretationComputer, Processor
from apps.scoring.scorer import IntTypedScorer
from apps.scoring import create_multiscale

ExampleResultScale = create_multiscale(name="Example", keys=["data_analytic", "community_leader"])
MathHumanityScale = create_multiscale(name="MathHumanity", keys=["math", "humanity"])
ArchetypesScale = create_multiscale(name="Archetype", keys=["fighter", "visionary", "chaser"])

EXAMPLE_MATH_CONTENT = [
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
EXAMPLE_ARCHETYPES_CONTENT = {
    "visionary": 3,
    "fighter": -1,
    "chaser": 1
}


class ExampleInterpretationComputer(InterpretationComputer):
    """
    Пример вычислителя интерпретации.
    Вычисляет ExampleResultScale на основе вопроса по математике и результатов архетипов.
    Обработка вопроса по математике - внутренняя, а архетипов - внешняя, поэтому
    Processor только один.
    """
    def __init__(self, config):
        super().__init__(config)
        self.processors = [
            Processor([
                IntTypedScorer.check_equals(9,   MathHumanityScale(math=3),              42),
                IntTypedScorer.check_greater(10, MathHumanityScale(math=-5, humanity=5), 42)
            ], scale=MathHumanityScale, selector_name="math")
        ]

    @classmethod
    def get_config_args(cls):
        args = {
            "id_math_question": "uuid вопроса по математике",
            "source_math_question": "url откуда брать ответы на вопрос по математике",
            "weight_math_question": "вес вопроса по математике",
            "weight_arch_questions": "вес теста про архетипы",
        }
        return args

    @classmethod
    def get_name_descr(cls):
        return "example_ic"

    def load(self, **kwargs):
        "Подгрузка данных для интерпретации. В данном случае - фальшивая"
        return {
            "math": EXAMPLE_MATH_CONTENT,
            "arch": EXAMPLE_ARCHETYPES_CONTENT
        }

    def compute(self, user_uid=None, **kwargs):
        content = self.load(user_uid=user_uid)
        structured = self.process(content)
        # строим Multiscale из content напрямую - они уже обработаны
        structured['arch'] = ArchetypesScale(**content["arch"])
        return self.aggregate(**structured)

    def aggregate(self, *, math, arch):
        """
        Шкала (math, humanity) напрямую добавляется в (data_analytic, community_leader)
        Шкала ArchetypesScale суммируется и поровну прибавляется к (data_analytic, community_leader)
        """
        math_weight = self.config.get("weight_math_question", 1)
        arch_weight = self.config.get("weight_arch_questions", 1)
        arch_matrix = np.array(
            [[1, 1, 1],
             [1, 1, 1]])
        return ExampleResultScale.from_numeric(
            math.numeric * math_weight + np.dot(arch_matrix, arch.numeric * arch_weight)
        )
