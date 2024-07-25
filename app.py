from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL 
from flask_wtf import FlaskForm,CSRFProtect 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

mysql = MySQL(app)


# Habilita CSRF Protection
csrf = CSRFProtect(app)

@app.route('/')
def index():                    
    form = LoginForm()                              
    return render_template('login.html',form=form)


class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login',methods = ['GET','POST'])
def login ():
    form=LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s ', (email,))
        account = cursor.fetchone()

        if account and check_password_hash(account['password'],password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            return redirect(url_for('inicio'))
        
        else:
            flash('Email ou senha incorretos','danger')

    return render_template('login.html',form=form)


class RegistrationForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')
    
@app.route("/registro",methods=['GET','POST'])
def registro():
    form = RegistrationForm()
    print(form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash('Senha está errada', 'danger')
            return redirect(url_for('registro'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s' , (email,))
        account = cursor.fetchone()

        if account:
            flash ('A conta já existe', 'danger')
        
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Email invalido','danger')
        elif not re.match(r'[A-Za-z0-9]+', password):
            flash('Sua senha deve conter apenas caracters e numeros','danger')
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute('INSERT INTO users (email,password) VALUES (%s,%s)', (email,hashed_password,))
            mysql.connection.commit()
            flash('Você foi registrado','success')
            print('registrado')
            return redirect(url_for('login'))
        
    return render_template('registro.html', form=form)



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    flash('Você saiu da sua conta', 'success')
    return redirect(url_for('login'))

@app.route('/inicio')
def inicio():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id,name,description,price,image_url FROM products')
        products = cursor.fetchall()
        print(products)
        return render_template('inicio.html',products=products)

    return render_template('login.html')

@app.route('/product/<int:product_id>')
def detalhes_produto(product_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT name,description,price,stock_quantity,category_id,image_url FROM products WHERE id = %s',(product_id,))
    product = cursor.fetchone()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id,name,description,price,image_url FROM products')
    produtos_geral = cursor.fetchall()

    if product:
        return render_template('detalhes_produto.html',product=product,produtos_geral=produtos_geral)
    else:
        return redirect(url_for('inicio'))
    
    


if __name__ == '__main__':
    app.run(debug=True)



####################################     OLHAR A QUESTAO DOS HTTPS DAS ROTAS ##########################