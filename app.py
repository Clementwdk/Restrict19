from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
#from covapp.models import db, Content

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"

db = SQLAlchemy(app)

class CRestrict(db.Model):
    country = db.Column(db.String(200), primary_key=True)
    authorization_status = db.Column(db.String(200))
    details = db.Column(db.Text(), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    infoRequirement = db.Column(db.Text(), nullable=False)
    vaccination = db.Column(db.Boolean(), nullable=False)
    test_medical_certificate = db.Column(db.Text(), nullable=False)
    other_medical_measures = db.Column(db.Text(), nullable=False)
    temparature_check = db.Column(db.Boolean(), nullable=False)
    use_of_mask = db.Column(db.Boolean(), nullable=False)
    public_transport = db.Column(db.Boolean(), nullable=False)
    nightclubs = db.Column(db.Boolean(), nullable=False)
    shops = db.Column(db.Boolean(), nullable=False)
    restaurants = db.Column(db.Boolean(), nullable=False)

    def __init__(self, country, authorization_status, details, severity, infoRequirement, vaccination,
                 test_medical_certificate, other_medical_measures, temparature_check, use_of_mask,
                 public_transport, nightclubs, shops, restaurants):
        self.restaurants = restaurants
        self.authorization_status = authorization_status
        self.details = details
        self.severity = severity
        self.country = country
        self.infoRequirement = infoRequirement
        self.vaccination = vaccination
        self.test_medical_certificate = test_medical_certificate
        self.other_medical_measures = other_medical_measures
        self.temparature_check = temparature_check
        self.use_of_mask = use_of_mask
        self.public_transport = public_transport
        self.nightclubs = nightclubs
        self.shops = shops

    def __repr__(self):
        return '<Country %r>' % self.country




@app.route('/', methods=['POST', 'GET'])
def home():
    country = CRestrict.query.all()
    return render_template('Index.html', country=country)

@app.route('/res', methods=['POST', 'GET'])
def res():
    country = CRestrict.query.all()
    return "coucou"




if __name__ == "__main__":
    app.run(debug=True)



