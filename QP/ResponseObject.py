class ResponseObject:
    def __init__(self, obj, status):
        self.object = obj
        self.status = status

    def serialize(self):
        if self.object is None:
            return{
                'object': '',
                'status': self.status
            }
        else:
            if isinstance(self.object, list):
                x = []
                for y in self.object:
                    x.append(y.serialize())
                return {
                    'object': x,
                    'status': self.status
                }
            return {
                'object': self.object.serialize(),
                'status': self.status
            }
