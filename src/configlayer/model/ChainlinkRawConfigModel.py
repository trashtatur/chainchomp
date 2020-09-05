class ChainlinkConfigModel:

    def __init__(self, raw_config: dict):
        self.raw_config = raw_config

    def get_project_name(self) -> str:
        return self.raw_config['project']

    def get_start(self) -> str:
        return self.raw_config['start']

    def get_stop(self) -> str:
        return self.raw_config['stop']

    def get_is_master_link(self) -> bool:
        if self.raw_config['masterLink'] == 'True':
            return True
        return False

    def get_master_link_location(self) -> str:
        return self.raw_config['masterLocation']

    def get_mq_type(self) -> str:
        return self.raw_config['chainlink']['type']

    def get_chainlink_name(self) -> str:
        return self.raw_config['chainlink']['name']

    def get_next_chainlink(self) -> str:
        return self.raw_config['chainlink']['next']

    def get_profile(self) -> dict:
        return self.raw_config[self.get_mq_type()]['profile']
