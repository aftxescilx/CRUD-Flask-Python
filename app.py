from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL

app= Flask(__name__)

mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='institutojeffersonian'
mysql.init_app(app)

@app.route('/')
def index():
    
    sql="SELECT * FROM beneficiario WHERE estatus=1;"
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    beneficiario=cursor.fetchall()
    # print(beneficiario)
  
    conn.commit()
    return render_template('beneficiario/index.html', beneficiario=beneficiario)

@app.route('/destroy/<int:idBeneficiario>')
def destroy(idBeneficiario):
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("UPDATE beneficiario SET estatus=0 WHERE idBeneficiario=%s",(idBeneficiario))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:idBeneficiario>')
def edit(idBeneficiario):
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM beneficiario WHERE idBeneficiario=%s", (idBeneficiario))
    beneficiario=cursor.fetchall()
  
    conn.commit()
    return render_template('beneficiario/edit.html', beneficiario=beneficiario)

@app.route('/update', methods=['POST'])
def update():
    
    _nombre=request.form['txtNombre']
    _rfc=request.form['txtRfc']

    id=request.form['txtId']
    sql="UPDATE beneficiario SET nombre=%s, rfc=%s WHERE idBeneficiario=%s;"

    datos=(_nombre,_rfc,id)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

@app.route('/create')
def create():
    return render_template('beneficiario/create.html')

@app.route('/store', methods=['POST'])
def storage():
 
    _nombre=request.form['txtNombre']
    _rfc=request.form['txtRfc']
   
    sql="INSERT INTO beneficiario (idBeneficiario, nombre, rfc, idUsuarioCrea) VALUES (NULL, %s, %s, 1);"
    datos=(_nombre,_rfc)

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

if __name__== '__main__':
    app.run(debug=True)