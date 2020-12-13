class Connection:
    def __init__(self, sid, is_active, adapter_name):
        self.sid = sid
        self.is_active = is_active
        self.adapter_name = adapter_name
