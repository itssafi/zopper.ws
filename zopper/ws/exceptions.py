class InvalidFilterFoundException(Exception):

    def __init__(self, message=(400, 'Invalid filter found.')):
        self.status_code = message[0]
        self.value = message[1]

    def __str__(self):
        return repr(self.value)


class NoFilterPassed(Exception):

    def __init__(self, message=(404, 'No filter is passed')):
        self.status_code = message[0]
        self.value = message[1]

    def __str__(self):
        return repr(self.value)


class InvadilDataException(Exception):

    def __init__(self, message=(400, 'Unhandled exceptions')):
        self.status_code = message[0]
        self.value = message[1]

    def __str__(self):
        return repr(self.value)
