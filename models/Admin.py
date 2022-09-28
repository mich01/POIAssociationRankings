from dbconnect import db

class JsonModel(object):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Admin(db.Model,JsonModel):
    __tablename__ = 'tbl_Admin'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserName = db.Column(db.String(100), nullable=False)
    Pass_word = db.Column(db.String(500), nullable=False)
    Sur_Name = db.Column(db.String(100), nullable=False)
    Other_Names = db.Column(db.String(100), nullable=False)
    GenderID = db.Column(db.Integer, nullable=False)
    Role_ID = db.Column(db.Integer, nullable=False)

    def __init__(self, UserName, Pass_word, Sur_Name,OtherNames,GenderID,Role_ID):
        self.UserName = UserName
        self.Pass_word = Pass_word
        self.Sur_Name = Sur_Name
        self.Other_Names = Other_Names
        self.GenderID = GenderID
        self.Role_ID = Role_ID

