class ResponseObject(object):

    def __init__(self, message = 200, data = 'success'):
        self.message = message
        self.data = data

    def __repr__(self):
        return u'<ResponseObject {} {}>' .format(self.message, self.data)


    def set_fail(self, data = 'fail'):
        self.data = data
        self.message = 500