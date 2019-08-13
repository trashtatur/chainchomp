import os
import socket

import definitions
from resolver.jinja.helper.Helper import Helper


class RabbitMQDefault(Helper):

    def gethostname(self):
        return socket.gethostname()
    
    def getCookieInfo(self, path=os.path.join(definitions.CONFIG_FOLDER,'rabbitmq/erlangcookie')):
        file = open(path)
        content = file.readline()
        file.close()

        return content.rstrip()