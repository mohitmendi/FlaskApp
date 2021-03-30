from flask import Flask, render_template, request, redirect 
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

#Config
db=yaml.load(open('db.yaml'))

app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
    #fetch form data
         userDetails = request.form
         student_id=userDetails['student_id']
         first_name=userDetails['first_name']
         last_name=userDetails['last_name']
         dob=userDetails['dob']
         amount_due=userDetails['amount_due']
         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO students(student_id,first_name,last_name,dob,amount_due) VALUES(%s, %s, %s, %s, %s)",(student_id,first_name,last_name,dob,amount_due))
         mysql.connection.commit()
         cur.close()
         return redirect('/students')
    return render_template('index.html')
@app.route('/students')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM students")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__=='__main__':
    app.run(debug=True)