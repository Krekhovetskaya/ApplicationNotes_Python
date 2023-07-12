import json


class Note:

    def __init__(self, ident, header, message, version_date) -> None:
        self.ident = ident
        self.header = header
        self.message = message
        self.version_date = version_date

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Note):
            return False
        return self.ident == o.ident

    def __hash__(self):
        return hash(self.ident)


class NoteEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Note):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)
