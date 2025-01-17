from app import db

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), unique=True, nullable=False)
    flight = db.Column(db.Float, nullable=False)
    accommodation = db.Column(db.Float, nullable=False)
    food = db.Column(db.Float, nullable=False)
    transport = db.Column(db.Float, nullable=False)

class SeasonFactor(db.Model):
    __tablename__ = 'season_factors'

    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(20), unique=True, nullable=False)
    factor = db.Column(db.Float, nullable=False)
