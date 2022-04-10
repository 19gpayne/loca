from api.model.shared_models import db

class Monument(db.Model):
    __table__ = db.Model.metadata.tables['monument']

class Description(db.Model):
    __table__ = db.Model.metadata.tables['descript']

class MonumentPicture(db.Model):
    __table__ = db.Model.metadata.tables['monument_picture']