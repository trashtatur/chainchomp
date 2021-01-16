class Connection:
    def __init__(self, sid, is_active, adapter_name):
        self.sid = sid
        self.is_active = is_active
        self.name = adapter_name
