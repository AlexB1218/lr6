from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bobrovitskiy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BackupData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backupdate = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<BackupData %r>' % self.id


class Inspection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(100), nullable=False)
    user_number = db.Column(db.Integer, nullable=False)
    owner_number = db.Column(db.Integer, nullable=False)
    auto_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Inspection %r>' % self.id


class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colour = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    engine = db.Column(db.Integer, nullable=False)
    technical_passport = db.Column(db.String(100), nullable=False)
    inspection_id = db.Column(db.Integer, nullable=False)
    owner_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Auto %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    officer_firstname = db.Column(db.String(100), nullable=False)
    officer_lastname = db.Column(db.String(100), nullable=False)
    officer_rank = db.Column(db.String(100), nullable=False)
    inspection_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Integer, nullable=False)
    license = db.Column(db.Integer, nullable=False)
    auto_number = db.Column(db.Integer, nullable=False)
    inspection_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Owner %r>' % self.id

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/backup')
def backup():
    backup = BackupData.query.order_by(BackupData.id.desc()).all()
    return render_template("backup.html", backup=backup)


@app.route('/backup/<int:id>/update', methods=['POST', 'GET'])
def backup_update(id):
    backup = BackupData.query.get(id)
    if request.method == "POST":
        backup.backupdate = request.form['backupdate']

        try:
            db.session.commit()
            return redirect('/backup')
        except:
            return "При радактировании резервных данных произошла ошибка"
    else:
        return render_template("update_backup.html", backup=backup)


@app.route('/create_backup', methods=['GET', 'POST'])
def backup_create():
    if request.method == "POST":
        backupdate = request.form['backupdate']

        backup = BackupData(backupdate=backupdate)

        try:
            db.session.add(backup)
            db.session.commit()
            return redirect('/backup')
        except:
            return "При добавлении резервных данных произошла ошибка"
    else:
        return render_template("create_backup.html")


@app.route('/backup/<int:id>/delete')
def backup_delete(id):
    backup = BackupData.query.get_or_404(id)

    try:
        db.session.delete(backup)
        db.session.commit()
        return redirect('/backup')
    except:
        return "При удалении резеврных данных произошла ошибка"


@app.route('/backup/<int:id>')
def backup_detail(id):
    backup = BackupData.query.get(id)
    return render_template("backup_detail.html", backup=backup)


@app.route('/owner')
def owner():
    owner = Owner.query.order_by(Owner.id.desc()).all()
    return render_template("owner.html", owner=owner)


@app.route('/owner/<int:id>/update', methods=['POST', 'GET'])
def owner_update(id):
    owner = Owner.query.get(id)
    if request.method == "POST":
        owner.firstname = request.form['firstname']
        owner.lastname = request.form['lastname']
        owner.gender = request.form['gender']
        owner.adress = request.form['adress']
        owner.birthday = request.form['birthday']
        owner.license = request.form['license']

        try:
            db.session.commit()
            return redirect('/owner')
        except:
            return "При радактировании владельца авто произошла ошибка"
    else:
        return render_template("update_owner.html", owner=owner)


@app.route('/create_owner', methods=['GET', 'POST'])
def owner_create():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        adress = request.form['adress']
        birthday = request.form['birthday']
        license = request.form['license']

        owner = Owner(firstname=firstname, lastname=lastname, gender=gender,
                      adress=adress, birthday=birthday, license=license)

        try:
            db.session.add(owner)
            db.session.commit()
            return redirect('/owner')
        except:
            return "При добавлении владельца авто произошла ошибка"
    else:
        return render_template("create_owner.html")


@app.route('/owner/<int:id>/delete')
def owner_delete(id):
    owner = Owner.query.get_or_404(id)

    try:
        db.session.delete(owner)
        db.session.commit()
        return redirect('/owner')
    except:
        return "При удалении владельца авто произошла ошибка"


@app.route('/owner/<int:id>')
def owner_detail(id):
    owner = Owner.query.get(id)
    return render_template("owner_detail.html", owner=owner)


@app.route('/auto')
def auto():
    auto = Auto.query.order_by(Auto.id.desc()).all()
    return render_template("auto.html", auto=auto)


@app.route('/auto/<int:id>/delete')
def auto_delete(id):
    auto = Auto.query.get_or_404(id)

    try:
        db.session.delete(auto)
        db.session.commit()
        return redirect('/position')
    except:
        return "При удалении авто произошла ошибка"


@app.route('/auto/<int:id>/update', methods=['POST', 'GET'])
def auto_update(id):
    auto = Auto.query.get(id)
    if request.method == "POST":
        auto.id = request.form['id']
        auto.colour = request.form['colour']
        auto.brand = request.form['brand']
        auto.technical_passport = request.form['technical_passport']
        auto.engine = request.form['engine']

        try:
            db.session.commit()
            return redirect('/auto')
        except:
            return "При радактировании должности произошла ошибка"
    else:
        return render_template("update_auto.html", auto=auto)


@app.route('/create_auto', methods=['POST', 'GET'])
def auto_create():
    if request.method == "POST":
        id = request.form['id']
        colour = request.form['colour']
        brand = request.form['brand']
        technical_passport = request.form['technical_passport']
        engine = request.form['engine']

        auto = Auto(id=id, colour=colour,
                    brand=brand, technical_passport=technical_passport, engine=engine)

        try:
            db.session.add(auto)
            db.session.commit()
            return redirect('/auto')
        except:
            return "При добавлении авто произошла ошибка"
    else:
        return render_template("create_auto.html")


@app.route('/auto/<int:id>')
def auto_detail(id):
    auto = Auto.query.get(id)
    return render_template("auto_detail.html", auto=auto)


@app.route('/inspection')
def inspection():
    inspection = Inspection.query.order_by(Inspection.id.desc()).all()
    return render_template("inspection.html", inspection=inspection)


@app.route('/inspection/<int:id>')
def inspection_detail(id):
    inspection = Inspection.query.get(id)
    return render_template("inspection_detail.html", inspection=inspection)


@app.route('/inspection/<int:id>/delete')
def inspection_delete(id):
    inspection = Inspection.query.get_or_404(id)

    try:
        db.session.delete(inspection)
        db.session.commit()
        return redirect('/inspection')
    except:
        return "При удалении информации об инспекции произошла ошибка"


@app.route('/inspection/<int:id>/update', methods=['POST', 'GET'])
def inspection_update(id):
    inspection = Inspection.query.get(id)
    if request.method == "POST":
        inspection.date = request.form['date']
        inspection.result = request.form['result']

        try:
            db.session.commit()
            return redirect('/inspection')
        except:
            return "При радактировании инспекции произошла ошибка"
    else:
        return render_template("update_inspection.html", inspection=inspection)


@app.route('/create_inspection', methods=['GET', 'POST'])
def inspection_create():
    if request.method == "POST":
        date = request.form['date']
        result = request.form['result']

        inspection = Inspection(date=date, result=result)

        try:
            db.session.add(inspection)
            db.session.commit()
            return redirect('/inspection')
        except:
            return "При добавлении инспекции произошла ошибка"
    else:
        return render_template("create_inspection.html")


@app.route('/user')
def user():
    user = User.query.order_by(User.id.desc()).all()
    return render_template("user.html", user=user)


@app.route('/user/<int:id>/update', methods=['POST', 'GET'])
def user_update(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.login = request.form['login']
        user.password = request.form['password']
        user.officer_firstname = request.form['officer_firstname']
        user.officer_lastname = request.form['officer_lastname']
        user.officer_rank = request.form['officer_rank']

        try:
            db.session.commit()
            return redirect('/user')
        except:
            return "При радактировании пользователя произошла ошибка"
    else:
        return render_template("update_user.html", user=user)


@app.route('/create_user', methods=['GET', 'POST'])
def user_create():
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        officer_firstname = request.form['officer_firstname']
        officer_lastname = request.form['officer_lastname']
        officer_rank = request.form['officer_rank']

        user = User(login=login, password=password, officer_firstname=officer_firstname,
                    officer_lastname=officer_lastname, officer_rank=officer_rank)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/user')
        except:
            return "При добавлении перемещения сотрудников произошла ошибка"
    else:
        return render_template("create_user.html")


@app.route('/user/<int:id>/delete')
def user_delete(id):
    user = User.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/user')
    except:
        return "При удалении пользователя произошла ошибка"


@app.route('/user/<int:id>')
def user_detail(id):
    user = User.query.get(id)
    return render_template("user_detail.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
