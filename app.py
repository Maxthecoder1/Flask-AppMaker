from flask import Flask, render_template, request, session, send_file
import os
import random
import shutil

from distutils.dir_util import copy_tree
app = Flask(__name__)
app.secret_key = 'MaxavierJeanphilippe'
#file = open('app.py', mode='w')
newappfilename = None
newapp = None


def import_creator(file, options):
    if options == 'userauth':
        file.write("from flask import Flask, render_template, request, session, flash, redirect, g, url_for\n")
        file.write("from flask_login import LoginManager, login_user, logout_user, current_user, login_required\n")
        file.write("from flask_sqlalchemy import SQLAlchemy\n")
        file.write("from datetime import datetime\n\n")
        file.write("app = Flask(__name__)\napp.config['SQLALCHEMY_DATABASE_URI'] = None # Enter the database connection string here\ndb = SQLAlchemy(app)\nlogin_manager = LoginManager()\nlogin_manager.init_app(app)\nlogin_manager.login_view = 'login'\n\n")
    else:
        file.write("from flask import Flask, render_template, request, session, flash, redirect, g, url_for\n")
        file.write("from flask_sqlalchemy import SQLAlchemy\n")
        file.write("from datetime import datetime\n\n")
        file.write("app = Flask(__name__)\napp.config['SQLALCHEMY_DATABASE_URI'] = None # Enter the database connection string here\ndb = SQLAlchemy(app)\n\n")


def express_model_creator(file, extras, models):
    if extras == 'none':
        for m in range(models):
            file.write("class Table{0}(db.Model):\n".format(m))
            file.write('\t__tablename__ = "table{0}"\n'.format(m))
            file.write("\tid = db.Column('id', db.Integer, primary_key=True)\n\n")
            file.write("\tdef init(self):\n")
            file.write("\t```initialize column variables```\n\n\n")
    elif extras == 'user':
        file.write("class User(db.Model):\n")
        file.write('\t__tablename__ = "users"\n')
        file.write("\tid = db.Column('id', db.Integer, primary_key=True)\n\n")
        file.write("\tdef init(self):\n")
        file.write("\t```initialize column variables```\n\n")
        for m in range(models):
            file.write("class Table{0}(db.Model):\n".format(m))
            file.write("\tid = db.Column('id', db.Integer, primary_key=True)\n\n")
            file.write("\tdef init(self):\n")
            file.write("\t```initialize column variables```\n\n\n")
    else:
        file.write("class User(db.Model):\n")
        file.write('\t__tablename__ = "users"\n')
        file.write("\tid = db.Column('id', db.Integer, primary_key=True)\n\n")
        file.write('\t@login_manager.user_loader\n\tdef user_load(id):\n\t\treturn User.query.get(id)\n\n\tdef is_active(self):\n\t\t"""True, as all users are active."""\n\t\treturn True\n\n\tdef get_id(self):\n\t\treturn self.id\n\n\tdef is_authenticated(self):\n\t\t"""Return True if the user is authenticated."""\n\t\treturn True\n\n\tdef is_anonymous(self):\n\t\t"""False, as anonymous users are not supported."""\n\t\treturn True\n\n')
        file.write("\tdef init(self):\n")
        file.write("\t```initialize column variables```\n\n\n")
        for m in range(models):
            file.write("class Table{0}(db.Model):\n".format(m))
            file.write('\t__tablename__ = "table{0}"\n'.format(m))
            file.write("\tid = db.Column('id', db.Integer, primary_key=True)\n\n")
            file.write("\tdef init(self):\n")
            file.write("\t```initialize column variables```\n\n\n")


def express_route_creator(file, rnumber, extras):
    if extras == 'userauth':
        file.write("@app.before_request\ndef _before_request():\n\tg.user = current_user\n\n\n")
    for number in range(0, rnumber):
        file.write("@app.route('/{0}', ".format(number))
        file.write("methods = ['GET', 'POST'])\n")
        file.write("def endpoint{0}():\n\t".format(number))
        file.write("if request.method == 'GET':\n\t")
        file.write("```do stuff```\n\t")
        file.write("elif request.method == 'POST'\n\t")
        file.write("```do stuff```\n\t")
        file.write('return render_template("endpoint{0}.html") #redirect_for_url("otherendpoint)\n\n\n'.format(number))


@app.route('/', methods=['GET'])
def home():
    return render_template('landingpage.html')

@app.route('/custom', methods=['GET'])
def custom():
    global newappfilename
    newappfilename = "flaskwebapp{0}".format(random.randint(0, 100000))
    return render_template('comingsoon.html')


@app.route('/express', methods=['GET'])
def express():
    global newappfilename
    newappfilename = "flaskwebapp{0}".format(random.randint(0, 100000))
    return render_template('startdesign.html')


@app.route('/customroutes', methods=['POST'])
def customroutes():
    return render_template('customroutes.html')

@app.route('/numberofcolumns', methods=['POST'])
def routes():
    return render_template('howmanycolumns.html')


@app.route('/edownload', methods=['POST', 'GET'])
def edownload():
    if request.method == 'POST':
        copy_tree("static\\flask_web_app", "static\\{0}".format(newappfilename))
        with open('static\\{0}\\app.py'.format(newappfilename), mode='w') as file:
            if len(request.form) == 4:
                import_creator(file, request.form['extras'])
                express_model_creator(file, request.form['extras'], int(request.form['models']))
                express_route_creator(file, int(request.form['routes']), request.form['extras'])
                file.write("if __name__ == '__main__':\n\tdb.engine.echo = True\n\tdb.metadata.bind = db.engine\n\tdb.metadata.create_all(checkfirst=True)\n\tapp.run()")
                shutil.make_archive(newappfilename, 'zip', root_dir="static/")

        return render_template("edownload.html", zipf="{0}.zip".format(newappfilename))
    if request.method == 'GET':
        return render_template("edownload.html", zipf="{0}.zip".format(newappfilename))

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        newapp['extras'] = request.form['extras']
        print(request.form)
        for num in range(int(request.form['models'])):
            newapp['models'][str(num)]['name'] = "Table{0}".format(num)
        if request.form['extras'] == "user" or request.form['extras'] == "userauth":
            newapp['models']['0']['name'] = "User"
        for r in range(int('routes')):
            newapp['routes'][str(r)] = "endpoint{0}".format(r)
        return render_template("download.html")


@app.route('/static/<filename>', methods=['GET'])
def downlo(filename):
    return send_file(filename_or_fp="{0}".format(filename))


@app.errorhandler(code_or_exception=404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(threaded=True)
