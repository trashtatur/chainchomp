class ChainlinkConfigModel:

    def __init__(
            self,
            project_name: str,
            chainlink_name: str,
            next_link='',
            previous_link='',
            start='echo "No start script provided"',
            stop='echo "No stop script provided"',
            is_master_link=False,
            master_location='localhost',
            mq_type='rabbitmq',
            profile='default'

    ):
        self.is_master_link = is_master_link
        self.stop = stop
        self.start = start
        self.previous_link = previous_link
        self.next_link = next_link
        self.chainlink_name = chainlink_name
        self.project_name = project_name
        self.master_location = master_location
        self.mq_type = mq_type
        self.profile = profile
