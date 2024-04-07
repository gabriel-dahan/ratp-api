from . import db

class RATP_Line(db.Model):
    __tablename__ = 'lines'

    id = db.Column(db.String(6), primary_key = True)
    type = db.Column(db.String(10), nullable = False)
    name = db.Column(db.String(255), nullable = False)
    groupname = db.Column(db.String(255))
    operatorname = db.Column(db.String(255), nullable = False)
    networkname = db.Column(db.String(255))

    @property
    def serialize(self) -> dict:
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'type': self.type,
           'name': self.name,
           'groupname': self.groupname,
           'operatorname': self.operatorname,
           'networkname': self.networkname
       }