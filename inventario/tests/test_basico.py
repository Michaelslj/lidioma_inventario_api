from django.test import TestCase

class PruebaBasica(TestCase):
    def test_siempre_pasa(self):
        self.assertEqual(1, 1)