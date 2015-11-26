from unittest import TestCase
from app.database import stub


class TestCase(TestCase):
    def setUp(self):
        stub()

