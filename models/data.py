from dbconnect import db

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Call_Logs(db.Model, JsonModel):
    __tablename__ = 'calllog'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    POI = db.Column(db.String(200), nullable=False)
    Contact = db.Column(db.String(500), nullable=False)
    Time_of_Contact = db.Column(db.DateTime, nullable=False)
    Duration = db.Column(db.Integer, nullable=False)

    def __init__(self, POI, Contact, Time_of_Contact, Duration):
        self.POI = POI
        self.Contact = Contact
        self.Time_of_Contact = Time_of_Contact
        self.Duration = Duration

class Proximity_Logs(db.Model, JsonModel):
    __tablename__ = 'proximity'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    POI = db.Column(db.String(200), nullable=False)
    ShadowID = db.Column(db.String(500), nullable=False)
    Location = db.Column(db.String(100),nullable=False)
    Latitude = db.Column(db.String(100), nullable=False)
    Longitude = db.Column(db.String(100), nullable=False)
    Time_of_Observation = db.Column(db.DateTime, nullable=False)
    Date_of_Observation = db.Column(db.DateTime, nullable=False)

    def __init__(self, POI, ShadowID, Time_of_Contact,Location, Latitude, Longitude, Date_of_Observation):
        self.POI = POI
        self.ShadowID = ShadowID
        self.Location = Location
        self.Latitude=Latitude
        self.Longitude=Longitude
        self.Time_of_Contact = Time_of_Contact
        self.Date_of_Observation = Date_of_Observation
