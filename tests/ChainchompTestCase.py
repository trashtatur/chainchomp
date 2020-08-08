import os
import unittest
from abc import ABC


class ChainchompConfigTestCase(unittest.TestCase, ABC):

    def setUp(self) -> None:
        os.environ["testing"] = "true"

    def tearDown(self) -> None:
        os.environ["testing"] = "false"
