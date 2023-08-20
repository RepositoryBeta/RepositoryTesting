from flask import Flask, session, render_template, request, redirect, url_for, flash
import models.conexion as conexion
from werkzeug.utils import secure_filename
from datetime import datetime
import os
app = Flask(__name__)
conn = conexion.DB()

def select(tabla):
        cur = conn.cursor()
        cur.execute('SELECT * FROM '+tabla)
        data = cur.fetchall()
        return data

def selectQuery(query):
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

def loginAdmin():
    if request.method == 'POST':
        cur = conn.cursor()
        Email = request.form['Email']
        Password = request.form['Password']
        query = ("SELECT IdUsuario,Nombres FROM usuarios WHERE Email = %s AND Password = %s AND IdEstado =1")
        valores = (Email,Password)
        cur.execute(query, valores)
        cur.connection.commit()
        result = cur.fetchall()
        cur.close()
        return result

app.config['UPLOAD_FOLDER'] = 'static/files/'
def publicarDocumento(iduser):
    idu = iduser
    if request.method == 'POST':
        cur = conn.cursor()
        Fecha = request.form['Fecha']
        Autor = request.form['Autor']
        Proyecto = request.form['Proyecto']
        Documento = request.files['Documento']
        filename = secure_filename(Documento.filename)
        Documento.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        query = ("INSERT INTO publicaciones (IdUsuario,Fecha,Autor,Proyecto,Ruta)VALUE(%s,%s,%s,%s,%s)")
        valores = (idu,Fecha,Autor,Proyecto,Ruta)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def listarPublicacionesAdmin():
    cur = conn.cursor()
    query = ("SELECT IdPublicacion,Fecha,Autor,Proyecto,Ruta FROM publicaciones ORDER BY IdPublicacion DESC")
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result

def getModificarPublicacionId():
    if request.method == 'POST':
        cur = conn.cursor()
        IdPublicacion = request.form['IdPublicacion']
        query = ("SELECT IdPublicacion,Fecha,Autor,Proyecto FROM publicaciones WHERE IdPublicacion = %s")
        cur.execute(query,IdPublicacion)
        result = cur.fetchall()
        cur.close()
        return result

app.config['UPLOAD_FOLDER'] = 'static/files/'
def getModificarPublicacion(muser):
    musr = muser
    if request.method == 'POST':
        cur = conn.cursor()
        IdPublicacion = request.form['IdPublicacion']
        Fecha = request.form['Fecha']
        Autor = request.form['Autor']
        Proyecto = request.form['Proyecto']
        Documento = request.files['Documento']
        filename = secure_filename(Documento.filename)
        Documento.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Ruta = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        query = """UPDATE publicaciones SET IdUsuario = %s,Fecha = %s,Autor = %s,Proyecto = %s,Ruta = %s WHERE IdPublicacion = %s"""
        valores = (musr,Fecha,Autor,Proyecto,Ruta,IdPublicacion)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def listarEstudiantesAdmin():
    cur = conn.cursor()
    query = """SELECT U.IdUsuario,R.Rol,CONCAT(U.Nombres,' ',U.Apellidos) AS 'Estudiantes',
    U.Nombres,U.Apellidos,TI.Tipo,U.Identificacion,U.Direccion,U.Telefono,U.Email,E.Estado 
    FROM usuarios U
    INNER JOIN roles R ON (U.IdRol=R.IdRol)
    INNER JOIN tipo_identificacion TI ON (U.IdTipo=TI.IdTipo)
    INNER JOIN estados E ON (U.IdEstado=E.IdEstado) ORDER BY U.IdUsuario DESC"""
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result

def getTipoTdentificacion():
    cur = conn.cursor()
    query = """SELECT IdTipo,Tipo 
    FROM tipo_identificacion"""
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result

def getActivarUsuario():
    if request.method == 'POST':
        cur = conn.cursor()
        IdUsuario = request.form['IdUsuario']
        query = """UPDATE usuarios SET IdEstado=1 
        WHERE IdUsuario = %s"""
        valores = IdUsuario
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def getMUsuario():
    if request.method == 'POST':
        cur = conn.cursor()
        IdUsuario = request.form['IdUsuario']
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        Identificacion = request.form['Identificacion']
        Direccion = request.form['Direccion']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        query = """UPDATE usuarios SET Nombres = %s,Apellidos = %s,Identificacion = %s,
        Direccion = %s,Telefono = %s,Email = %s WHERE IdUsuario = %s"""
        valores = (Nombres,Apellidos,Identificacion,Direccion,Telefono,Email,IdUsuario)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def getEliminarUsuario():
    if request.method == 'POST':
        cur = conn.cursor()
        IdUsuario = request.form['IdUsuario']
        query = """UPDATE usuarios SET IdEstado=2 
        WHERE IdUsuario = %s"""
        valores = IdUsuario
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def getEliminarChat():
    if request.method == 'POST':
        cur = conn.cursor()
        IdChat = request.form['IdChat']
        query = """UPDATE chat SET IdEstado=2
        WHERE IdChat = %s"""
        valores = IdChat
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def listarConsultas(iduser):
    IdUsuario = 2
    cur = conn.cursor()
    query = """SELECT C.IdConsulta,CONCAT(U.Nombres,' ',U.Apellidos) AS 'Estudiantes',C.Texto,E.Estado 
    FROM consultas C
    INNER JOIN usuarios U ON (C.IdUsuario=U.IdUsuario)
    INNER JOIN estados E ON (C.IdEstado=E.IdEstado) WHERE C.IdUsuario = %s ORDER BY C.IdConsulta DESC"""
    cur.execute(query,IdUsuario)
    result = cur.fetchall()
    cur.close()
    return result

def TConsulta():
    IdConsulta = request.form['IdConsulta']
    cur = conn.cursor()
    query = """SELECT Texto
    FROM consultas
    WHERE IdConsulta = %s"""
    cur.execute(query,IdConsulta)
    result = cur.fetchall()
    cur.close()
    return result
    #for row in result:
        

def registrarChat():
    if request.method == 'POST':
        cur = conn.cursor()
        Preguntas = request.form['Preguntas']
        Respuestas = request.form['Respuestas']
        query = "INSERT INTO chat (Preguntas,Respuestas)VALUE(%s,%s)"
        valores = (Preguntas,Respuestas)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def getModificarChatId():
    if request.method == 'POST':
        cur = conn.cursor()
        IdChat = request.form['IdChat']
        query = ("SELECT IdChat,Preguntas,Respuestas FROM chat WHERE IdChat = %s")
        cur.execute(query,IdChat)
        result = cur.fetchall()
        cur.close()
        return result

def getModificarChat():
    if request.method == 'POST':
        cur = conn.cursor()
        IdChat = request.form['IdChat']
        Preguntas = request.form['Preguntas']
        Respuestas = request.form['Respuestas']
        query = """UPDATE chat SET Preguntas = %s,Respuestas = %s WHERE IdChat = %s"""
        valores = (Preguntas,Respuestas,IdChat)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            return True
        else:
            return False

def listarChats():
    cur = conn.cursor()
    IdC = 1
    query = """SELECT IdChat,Preguntas,Respuestas FROM chat WHERE IdEstado = %s"""
    cur.execute(query,IdC)
    result = cur.fetchall()
    cur.close()
    return result