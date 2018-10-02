from django.test import TestCase
from .multiscale import create_multiscale
from .scorer import IntTypedScorer

class MultiscaleTestCase(TestCase):

    def test_creation(self):
        name = "SchemeTest"
        keys = ["alpha", "beta", "gamma"]

        ms_cls = create_multiscale(name=name, keys=keys)
        ms = ms_cls(alpha=2)
        self.assertTrue(all([
            getattr(ms, 'alpha') == 2,
            getattr(ms, 'beta') == 0,
            getattr(ms, 'gamma') == 0
        ]))

    def test_summation(self):
        name = "SchemeTest"
        keys = ["alpha", "beta", "gamma"]

        ms_cls = create_multiscale(name=name, keys=keys)
        ms1 = ms_cls(alpha=2)
        ms2 = ms_cls(alpha=1, gamma=2)
        ms = ms1 + ms2

        self.assertTrue(all([
            getattr(ms, 'alpha') == 3,
            getattr(ms, 'beta') == 0,
            getattr(ms, 'gamma') == 2
        ]))


class ScoringTestCase(TestCase):
    def setUp(self):
        self.Scale = create_multiscale(name="MH", keys=["math", "humanities"])

    def test_int_scorer(self):
        prize1 = self.Scale(math=3)
        scorer1 = IntTypedScorer.check_equals(9, prize1, 42)

        prize2 = self.Scale(math=-5, humanities=5)
        scorer2 = IntTypedScorer.check_greater(10, prize2, 42)
        ple_api_content = [
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
        total = scorer1.apply(ple_api_content) + scorer2.apply(ple_api_content)
        self.assertTrue(
            total.math == -5 and total.humanities==5
        )
