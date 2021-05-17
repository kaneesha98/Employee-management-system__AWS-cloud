from flask import Flask, render_template, redirect, url_for, request, session, logging, flash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
import sqlite3, hashlib, os
import string


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

class LoginForm(Form):  # Create Login Form
    Id = IntegerField('Id', render_kw={'autofocus': True, 'placeholder': 'Id'})
    password = PasswordField('password', [validators.length(min=3)],
                             render_kw={'placeholder': 'password'})

@app.route('/hrfinance.html', methods=['GET', 'POST'])
def hrfinance():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        Id = form.Id.data
        password= form.password.data
        if request.form['password']!='admin123':
            error="Invalid credentials. Please try again."
            return render_template('hrfinance.html', error=error)
        else:
            with sqlite3.connect('main.db') as conn:
                cur = conn.cursor()
                cur.execute('SELECT Id, email, designation, firstName, lastName, address1, address2, bloodgroup, city, state, country, phone, start_date, dob FROM employee WHERE Id=?', [Id])
                data=cur.fetchall()
                if data!=None:
                    return redirect(url_for('details', data=data))
                else:
                    error="Employee not found"
                    cur.close()
                return render_template('hrfinance.html', form=form, error=error)
    return render_template('hrfinance.html', form=form)

@app.route('/details.html', methods=['GET', 'POST'])
def details():
    data=request.args.get('data', None)
    s=data[1]
    data=parse(data)
    return render_template('details.html', data=data, s=s)

@app.route("/new.html", methods = ['GET', 'POST'])
def new():
    msg=None
    if request.method == 'POST':
        #Parse form data    
        email = request.form['email']
        password = request.form['password']
        designation=request.form['designation']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        bloodgroup = request.form['bloodgroup']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone=request.form['phone']
        start_date=request.form['start_date']
        dob=request.form['dob']

        with sqlite3.connect('main.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO employee (email, password, designation, firstName, lastName, address1, address2, bloodgroup, city, state, country, phone, start_date, dob) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (email, password, designation, firstName, lastName, address1, address2, bloodgroup, city, state, country, phone, start_date, dob))
            con.commit()
            msg="REGISTERED!"
        con.close()
        return render_template("home.html", error=msg)
    return render_template("new.html")



@app.route("/existing_login.html", methods = ['GET', 'POST'])
def existing_login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        Id = form.Id.data
        password = form.password.data
        with sqlite3.connect('main.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM employee WHERE Id=?", [Id])
            data=cur.fetchall()
            if data!=None:
                cur.execute("SELECT password FROM employee WHERE Id=?", [Id])
                passw=cur.fetchone()
                if request.form['password'] != passw[0]:
                    error = 'Invalid Password. Please try again.'
                else:
                    return redirect(url_for('existing_details'))
            else:
                error="Employee not found"
                cur.close()
        return render_template('existing_login.html', form=form, error=error)
    return render_template('existing_login.html', form=form)


@app.route("/existing_details.html", methods=["GET", "POST"])
def existing_details():
    if request.method == 'POST':
        Id = request.form['Id']
        email = request.form['email']
        designation=request.form['designation']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        bloodgroup = request.form['bloodgroup']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        start_date=request.form['start_date']
        dob=request.form['dob']
        with sqlite3.connect('main.db') as con:
                cur = con.cursor()
                cur.execute('UPDATE employee SET email=?, designation=?, firstName = ?, lastName = ?, address1 = ?, address2 = ?, bloodgroup = ?, city = ?, state = ?, country = ?, phone = ?, start_date=?, dob=? WHERE Id=?', (email, designation, firstName, lastName, address1, address2, bloodgroup, city, state, country, phone, start_date, dob, Id))
                con.commit()
                msg = "Saved Successfully"
        con.close()
        return render_template('home.html', error=msg)
    return render_template('existing_details.html')

def parse(data):
    i = 2
    ans=[]
    while i < len(data)-1:
        if data[i]!="'" and data[i] not in string.whitespace:
            if data[i]==',':
                i+=2
                string1=""
                while data[i]!=',' and i<len(data)-1:
                    string1+=data[i]
                    i+=1
                ans.append(string1)
    return ans

if __name__ == '__main__':
    app.run(debug=True)
