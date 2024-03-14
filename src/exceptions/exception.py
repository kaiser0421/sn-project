class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, reason, status_code=None, payload=None):
        super().__init__()
        self.reason = reason
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['reason'] = self.reason
        return rv
    
class DatabaseError(Exception):
    status_code = 400

    def __init__(self, reason, status_code=None, payload=None):
        super().__init__()
        self.reason = reason
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['reason'] = self.reason
        return rv
    
class ServerError(Exception):
    status_code = 400

    def __init__(self, reason, status_code=None, payload=None):
        super().__init__()
        self.reason = reason
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['success'] = False
        rv['reason'] = self.reason
        return rv