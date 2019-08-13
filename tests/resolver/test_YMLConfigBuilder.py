import os
import unittest

from src.configs.MQs import MQTypes
from src.resolver.YMLConfigBuilder import YMLConfigBuilder


class YMLConfigLoaderTest(unittest.TestCase):
    RABBITMQ_CONFIGSTUB = os.getcwd() + "/configstubs/rabbitmq/default.yml"
    KAFKA_CONFIGSTUB = os.getcwd() + "/configstubs/kafka/default.yml"

    def setUp(self) -> None:
        self.YMLConfigLoaderRabbit = YMLConfigBuilder(MQTypes.RABBITMQ, os.getcwd() + '/profilestubs/')
        self.rabbitMQdefaultAssert = {
            'rabbitmq': {'hostname': 'testrabbit', 'name': 'myrabbit', 'erlangcookie': 'super secret cookie magic',
                         'profile': {'name': 'test', 'test': 'testvalue', 'some': {'other': {'test': 'testvalue2'}}}}}
        self.YMLConfigLoaderKafka = YMLConfigBuilder(MQTypes.KAFKA, os.getcwd() + '/profilestubs/')

    def test_load(self):
        pass
        # TODO Write more testcases for this


if __name__ == '__main__':
    unittest.main()
