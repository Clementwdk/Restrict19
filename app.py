from flask import Flask, g,render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from api import InfoC
from OpenSSL import SSL


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.secret_key = 'super secret key 2 '

db = SQLAlchemy(app)
apiData = InfoC()


class Usercon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    countryFav = [db.Column('CRestrict')]

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


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


users = Usercon.query.all()
country = CRestrict.query.all()


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/test', methods=['POST', 'GET'])
def test():
    apiData.reqApi('Ireland')

    return apiData.death

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        userChoice = request.form.get("ct")
        if request.form.get("subButton") == "Search":
            return redirect(url_for('res', country=userChoice))
    return render_template('Index.html', country=country)


@app.route('/res', methods=['POST', 'GET'])
def res():
    sCountry = request.args.get('country')
    actionFavButton = request.form.get("FavButton")
    listInfo = apiData.reqApilIST(sCountry)
    if sCountry:
        try:
            for x in country:
                if x.country == sCountry:
                    print('Country Find')
                    sCountry = x
        except:
            return 'INVALID DATA'
        print("Ok")
    if request.method == "POST":
        if actionFavButton:
            try:
                id = session['user_id']
            except:
                return 'You are not connected'
            for x in users:
                if x.id == id:
                    print("count exists")
                    userLog =  Usercon.query.filter_by(id=x.id).first()
                    userLog.countryFav.append(actionFavButton)
                    db.session.commit()
                    flash("Country add to your favorites")
    return render_template('res.html', infoC = sCountry, apiData= listInfo)

@app.route('/countryList', methods=['POST', 'GET'])
def countryList():
    sCountry = country
    actionFavButton = request.form.get("FavButton")

    if request.method == "POST":
        if actionFavButton:
            try:
                id = session['user_id']
            except:
                return 'You are not connected'
            for x in users:
                if x.id == id:
                    print("count exists")
                    userLog =  Usercon.query.filter_by(id=x.id).first()
                    userLog.countryFav.append(actionFavButton)
                    db.session.commit()
                    flash("Country add to your favorites")
    return render_template('countryList.html', infoC=sCountry, apiData= apiData)




@app.route('/login', methods=['POST', 'GET'])
def logIn():
    if request.method == 'POST':
            session.pop('user_id', None)

            login = request.form.get("log")
            pwd = request.form.get("pwd")

            for user in users:
                if user.name == login:
                    if user.password == pwd:
                        session['user_id'] = user.id
                        flash('Success')
                    else:
                        flash('Incorrect Password or Id')
    return render_template('logIn.html')

@app.route('/favorites', methods=['POST', 'GET'])
def favorites():
    listc = []
    try:
        id = session['user_id']
    except:
        return 'You are not connected'

    content = Usercon.query.filter_by(id=id).first()

    for fav in content.countryFav:
       queryC = CRestrict.query.filter_by(country=fav).first()
       if queryC not in listc and queryC:
        listc.append(queryC)
    return render_template('favorites.html', id=content, listc=listc)

@app.route('/nwaccount', methods=['POST', 'GET'])
def nwaccount():
    if request.method == "POST":
        user = request.form.get("nlog")
        pwd = request.form.get("npwd")
        if not user:
            flash("Username empty")
        elif not pwd:
            flash("Password empty")
        else:
            try:
                db.session.add(Usercon(user,pwd))
                db.session.commit()
            except:
                return 'Impossible to creat a new account'
            flash("Create Succesful")

    return render_template('nwaccount.html')

@app.route('/logout')
def logout():
        session.pop('user_id', None)
        return render_template('disconnected.html')


if __name__ == "__main__":
    app.run(debug=True)
    app.config['SESSION_TYPE'] = 'filesystem'
    db.create_all()






