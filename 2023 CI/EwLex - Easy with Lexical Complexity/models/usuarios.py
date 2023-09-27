from flask import Flask, session, jsonify, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import models.conexion as conexion
import re

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from werkzeug.security import generate_password_hash, check_password_hash

conn = conexion.DB()
app = Flask(__name__)

def loginUsuario():
    if request.method == 'POST':
        cur = conn.cursor()
        Usuario = request.form['Email']
        Password = request.form['Password']
        print(Password)
        query = ("SELECT IdUsuario,Password,Nombres FROM usuarios WHERE Usuario = %s AND Password = %s AND IdRol = 2 AND IdEstado =1")
        valores = (Usuario,Password)
        cur.execute(query, valores)
        cur.connection.commit()
        result = cur.fetchall()
        cur.close()
        return result
        """
        return result
        for ps in result:
            Ps = ps[1]
            Pass = check_password_hash(Ps,Password)
            if Pass ==True:
                
            else:
                return False
        """

def registraUsuarioAdmin():
    if request.method == 'POST':
        cur = conn.cursor()
        IdRol = 1
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        IdTipo = request.form['IdTipo']
        Identificacion = request.form['Identificacion']
        Direccion = request.form['Direccion']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        Password = request.form['Password']
        IdPregunta = request.form['IdPregunta']
        Respuesta = request.form['Respuesta']
        query = ("INSERT INTO usuarios (IdRol,Nombres,Apellidos,IdTipo,Identificacion,Direccion,Telefono,Usuario,Password,IdPregunta,Respuesta)VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        valores = (IdRol,Nombres,Apellidos,IdTipo,Identificacion,Direccion,Telefono,Email,Password,IdPregunta,Respuesta)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            cur = conn.cursor()
            query = """SELECT IdConfig,Servidor,Puerto,Remitente,Password,Asunto,Mensaje
            FROM config_correo"""
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            for re in result:
                servidor = re[1]
                puerto = re[2]
                remitente = re[3]
                password = re[4]
                asunto = re[5]
                mensaje = re[6]
                # Configuración del servidor SMTP y credenciales
                smtp_server = servidor
                smtp_port = puerto
                smtp_username = remitente
                smtp_password = password

                # Destinatario y remitente
                from_email = smtp_username
                to_email = Email
                # Crear objeto de mensaje
                subject = asunto
                body = ('Hola! ' + Nombres + ' ' + Apellidos + ', ' + mensaje +' Email: '+ Email + ' Password: ' + Password)
                msg = MIMEMultipart()
                msg["From"] = from_email
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                # Conectar al servidor SMTP
                try:
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_username, smtp_password)
    
                    # Enviar correo
                    server.sendmail(from_email, to_email, msg.as_string())
    
                    print("Correo enviado exitosamente")
                except Exception as e:
                    print("Error al enviar el correo:", e)
                finally:
                    # Cerrar la conexión al servidor SMTP
                    server.quit()
            return True
        else:
            return False

def registraUsuario():
    if request.method == 'POST':
        cur = conn.cursor()
        IdRol = 2
        Nombres = request.form['Nombres']
        Apellidos = request.form['Apellidos']
        IdTipo = request.form['IdTipo']
        Identificacion = request.form['Identificacion']
        Direccion = request.form['Direccion']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        Password = request.form['Password']
        #Pass = generate_password_hash(Password, 'sha256',30)
        IdPregunta = request.form['IdPregunta']
        Respuesta = request.form['Respuesta']
        query = ("INSERT INTO usuarios (IdRol,Nombres,Apellidos,IdTipo,Identificacion,Direccion,Telefono,Usuario,Password,IdPregunta,Respuesta)VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        valores = (IdRol,Nombres,Apellidos,IdTipo,Identificacion,Direccion,Telefono,Email,Password,IdPregunta,Respuesta)
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            cur = conn.cursor()
            query = """SELECT IdConfig,Servidor,Puerto,Remitente,Password,Asunto,Mensaje
            FROM config_correo"""
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            for re in result:
                servidor = re[1]
                puerto = re[2]
                remitente = re[3]
                password = re[4]
                asunto = re[5]
                mensaje = re[6]
                # Configuración del servidor SMTP y credenciales
                smtp_server = servidor
                smtp_port = puerto
                smtp_username = remitente
                smtp_password = password

                # Destinatario y remitente
                from_email = smtp_username
                to_email = Email
                # Crear objeto de mensaje
                subject = asunto
                body = ('Hola! ' + Nombres + ' ' + Apellidos + ', ' + mensaje +' Email: '+ Email + ' Password: ' + Password)
                msg = MIMEMultipart()
                msg["From"] = from_email
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                # Conectar al servidor SMTP
                try:
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    # Enviar correo
                    server.sendmail(from_email, to_email, msg.as_string())
                    print("Correo enviado exitosamente")
                except Exception as e:
                    print("Error al enviar el correo:", e)
                finally:
                    # Cerrar la conexión al servidor SMTP
                    server.quit()
            return True
        else:
            return False

def getModificarUsuarioId():
    if request.method == 'POST':
        cur = conn.cursor()
        IdUsuario = request.form['IdUsuario']
        query = ("SELECT IdUsuario,Nombres,Apellidos,Identificacion,Direccion,Telefono,Usuario FROM usuarios WHERE IdUsuario = %s")
        cur.execute(query,IdUsuario)
        result = cur.fetchall()
        cur.close()
        return result

def getValidaRespuesta():
    if request.method == 'POST':
        cur = conn.cursor()
        Usuario = request.form['Usuario']
        IdPregunta = request.form['IdPreguntas']
        Respuesta = request.form['Respuesta']
        valores = (Usuario,IdPregunta,Respuesta)
        query = ("SELECT Respuesta FROM usuarios WHERE Usuario = %s AND IdPregunta = %s AND Respuesta = %s")
        cur.execute(query,valores)
        result = cur.fetchone()
        return result

def getModificarPassword():
    if request.method == 'POST':
        cur = conn.cursor()
        Email = request.form['Usuario']
        Password = request.form['Password']
        query = """UPDATE usuarios SET Password = %s  WHERE Usuario = %s"""
        valores = (Password,Email,)
        cur.execute(query,valores)
        cur.connection.commit()
        cur.close()
        filas_afectadas = cur.rowcount
        if filas_afectadas > 0:
            cur = conn.cursor()
            query = """SELECT IdConfig,Servidor,Puerto,Remitente,Password,Asunto,Mensaje
            FROM config_correo"""
            cur.execute(query)
            result = cur.fetchall()
            cur.close()
            for re in result:
                servidor = re[1]
                puerto = re[2]
                remitente = re[3]
                password = re[4]
                asunto = re[5]
                mensaje = re[6]
                # Configuración del servidor SMTP y credenciales
                smtp_server = servidor
                smtp_port = puerto
                smtp_username = remitente
                smtp_password = password

                # Destinatario y remitente
                from_email = smtp_username
                to_email = Email
                # Crear objeto de mensaje
                subject = asunto
                body = ('Hola! hemos detectado modificacion de credenciales, ' + mensaje +' Email: '+ Email + ' Password: ' + Password)
                msg = MIMEMultipart()
                msg["From"] = from_email
                msg["To"] = to_email
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))

                # Conectar al servidor SMTP
                try:
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_username, smtp_password)
    
                    # Enviar correo
                    server.sendmail(from_email, to_email, msg.as_string())
    
                    print("Correo enviado exitosamente")
                except Exception as e:
                    print("Error al enviar el correo:", e)
                finally:
                    # Cerrar la conexión al servidor SMTP
                    server.quit()
            return True
        else:
            return False