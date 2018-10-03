from django.test import TestCase
from .example import ExampleInterpretationComputer


class ExampleInterTestCase(TestCase):

    def test_default(self):
        ic = ExampleInterpretationComputer({})
        res = ic.compute()
        # (-5, +5) за неправильный ответ по математике и (+3, +3) за архетипы
        self.assertTrue(res.data_analytic == -2)
        self.assertTrue(res.community_leader == 8)

    def test_weight_zero(self):
        ic = ExampleInterpretationComputer({
            "weight_math_question": 0
        })
        # вес вопроса по математике обнулен -> остается (+3, +3) за архетипы
        res = ic.compute()
        self.assertTrue(res.data_analytic == 3)
        self.assertTrue(res.community_leader == 3)
