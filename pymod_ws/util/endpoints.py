import re

class EndpointHandler:
    def __init__(self, endpoint):
        endpoint_pattern = "[a-zA-Z0-9_-]+"
        try:
            self.endpoint = re.findall(endpoint_pattern, endpoint)[0]
        except:
            raise NameError("Endpoint definition must match the regex {}".format(endpoint_pattern))

    def on_open(self):
        pass

    def on_message(self):
        pass

    def on_close(self):
        pass