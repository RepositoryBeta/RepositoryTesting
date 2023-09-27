from flask import Flask, session, jsonify, render_template, request, redirect, url_for, flash
import re
import models.usuarios as usuarios
import models.admin as admin

import json
from codecs import open
import base64

import models.conexion as conexion
#import index 
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


from PyMultiDictionary import MultiDictionary
dictionary = MultiDictionary()

conn = conexion.DB()
app = Flask(__name__)
app.secret_key = "SECRET_KEY"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regusuario_admin', methods=['GET', 'POST'])
def registrarUsuarioAdmin():
    user = usuarios.registraUsuarioAdmin()
    return jsonify(user)

@app.route('/regusuario', methods=['GET', 'POST'])
def registrarUsuario():
    user = usuarios.registraUsuario()
    print(user)
    return jsonify(user)

@app.route('/regchat', methods=['GET', 'POST'])
def registrarChat():
    rchat = admin.registrarChat()
    print(rchat)
    return jsonify(rchat)

@app.route('/get_modificar_usuario', methods=['GET', 'POST'])
def getModificarUsuarioId():
    user = usuarios.getModificarUsuarioId()
    return jsonify(user)

@app.route('/valida_respuesta', methods=['GET', 'POST'])
def valida_respuesta():
    mpass = usuarios.getValidaRespuesta()
    print(mpass)
    return jsonify(mpass)

@app.route('/nueva_password', methods=['GET', 'POST'])
def getmodificar_password():
    mpass = usuarios.getModificarPassword()
    print(mpass)
    return jsonify(mpass)

@app.route('/loginuser', methods=['GET', 'POST'])
def loginUsuario():
    usu = usuarios.loginUsuario()
    for usr in usu:
        session['idusuario'] = usr[0]
        print(session['idusuario'])
        session['usuario'] = usr[2]
    return jsonify(usu)

import unicodedata

def quitar_tildes(palabra):
    palabra_sin_tildes = ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))
    return palabra_sin_tildes

cur = conn.cursor()
@app.route('/buscar', methods=['POST'])
def palabrasComplejas():
    if request.method == "POST":
        cadena = request.form['cadena']
        query = ("INSERT INTO consultas (IdUsuario,Texto)VALUE(%s,%s)")
        valores = (session['idusuario'],cadena)
        cur = conn.cursor()
        cur.execute('SET NAMES utf8mb4')
        cur.execute("SET CHARACTER SET utf8mb4")
        cur.execute("SET character_set_connection=utf8mb4")
        cur.execute(query, valores)
        cur.connection.commit()
        cur.close()
        cur = conn.cursor()
        query = ("SELECT IdConsulta FROM consultas ORDER BY IdConsulta DESC")
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        stop_words = set(stopwords.words('spanish'))  # Utiliza 'spanish' para español
        palabras = word_tokenize(cadena)
        palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stop_words]
        palabras = tuple(palabras_filtradas)
        tupa2 = []
        for dato in palabras:
            query = ("SELECT Palabras FROM crea WHERE Palabras = %s AND FrecAbsoluta <1000")
            cur = conn.cursor()
            cur.execute('SET NAMES utf8mb4')
            cur.execute("SET CHARACTER SET utf8mb4")
            cur.execute("SET character_set_connection=utf8mb4")
            cur.execute(query,dato)
            result = cur.fetchall()
            cur.close()

            for registro in result:
                tupa2.append(registro)
            pl = set(tupa2)
            palabras_unicas = list(pl)
            i=0
            for elemento in palabras_unicas:
                i=i+1
        IdConsulta = 0
        for resu in res:
            IdConsulta = resu
        for element in palabras_unicas:
            for element_id in element:
                for rs in palabras_filtradas:
                    if rs == element_id:
                        plf = element_id
                        cur = conn.cursor()
                        query = ("INSERT INTO palabras_consulta (IdConsulta,Palabras)VALUE(%s,%s)")
                        valores = (IdConsulta,plf)
                        cur.execute(query, valores)
                        cur.connection.commit()
                        cur.close()
        query = ("SELECT IdPalabra,Palabras FROM palabras_consulta WHERE IdConsulta = %s")
        cur = conn.cursor()
        cur.execute(query,IdConsulta)
        rsl = cur.fetchall()
        cur.close()
        fr = list(rsl)
        return json.dumps(fr)

from nltk.corpus import wordnet
#from googletrans import Translator
from mtranslate import translate
# Descargar el recurso léxico de WordNet en español
nltk.download('omw')
nltk.download('wordnet')

def obtener_sinonimos(palabra):
    sinonimos = set()
    for synset in wordnet.synsets(palabra):
        for lemma in synset.lemmas():
            sinonimos.add(lemma.name())
    return sinonimos

def traducirT(texto):
    translator = Translator(from_lang='es', to_lang='en')
    traduccion = translator.translate(texto)
    return traduccion

def traducir(texto, idioma_origen, idioma_destino):
    translator = Translator()
    traduccion = translator.translate(texto, src=idioma_origen, dest=idioma_destino)
    return traduccion.text

@app.route('/get_sinonimos', methods=['POST'])
def getSinonimos():
    if request.method == "POST":
        IdPalabra = request.form['IdPalabra']
        query = ("SELECT Palabras FROM palabras_consulta WHERE IdPalabra = %s")
        cur = conn.cursor()
        cur.execute(query,IdPalabra)
        rsl = cur.fetchall()
        cur.close()
        sinonimos = [] #declarar lista para almacenar los sinonimos
        for row in rsl:
            for col in row:
                palabra = col
                traduccion = translate(palabra,"en")#traduce del español al ingles
                #print(traduccion)
                sinon = obtener_sinonimos(traduccion)
                if sinon:
                    #print(f"Sinónimos de {sinon}:")
                    for sinonimo in sinon:
                        traduccion = translate(sinonimo,"es")
                        #print(traduccion)
                        stop_words = set(stopwords.words('spanish'))  # Utiliza 'spanish' para español
                        palabras = word_tokenize(traduccion)
                        palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stop_words]
                        for pf in palabras_filtradas:
                            sinonimos.append(pf)
        lista_sin_repetidos = list(set(sinonimos))#pasar los sinonimos encontrados a la lista
        for sinonim in lista_sin_repetidos:#recorrer la lista de sinonimos para guardar en la base
            cur = conn.cursor()
            query = ("INSERT INTO sinonimos (IdPalabra,Palabras)VALUE(%s,%s)")#proceso de insercion en la base
            valores = (IdPalabra,sinonim)
            cur.execute(query, valores)
            cur.connection.commit()
        cur.close()
        return json.dumps(lista_sin_repetidos)#retorna al front la lista de sinonimos encontrados en formato json

@app.route('/get_palabra', methods=['POST'])
def getPalabra():
    if request.method == "POST":
        IdPalabra = request.form['IdPalabra']
        query = ("SELECT Palabras FROM palabras_consulta WHERE IdPalabra = %s")
        cur = conn.cursor()
        cur.execute(query,IdPalabra)
        rsl = cur.fetchall()
        cur.close()
        for row in rsl:
            pl = list(row)
        return json.dumps(pl)
        
def obtener_definiciones(palabra):
    # Obtiene los synsets (conjunto de palabras sinónimas) para la lista
    synsets = wordnet.synsets(palabra)
    definiciones = []
    for synset in synsets:
        # Obtiene las definiciones de los synsets
        definiciones.extend(synset.definitions())
    return definiciones
    
@app.route('/get_deficiciones', methods=['POST'])
def getDeficiciones():
    if request.method == "POST":
        IdPalabra = request.form['IdPalabra']
        query = ("SELECT Palabras FROM palabras_consulta WHERE IdPalabra = %s")
        cur = conn.cursor()
        cur.execute(query,IdPalabra)
        rsl = cur.fetchall()
        cur.close()
        definiciones = [] #declarar lista para almacenar las definiciones
        for row in rsl:
            for col in row:
                palabra = col
                traduccion = translate(palabra,"en")
                synsets = wordnet.synsets(traduccion)
                # Imprimir las definiciones
                if synsets:
                    for synset in synsets:
                        for definition in synset.definition().split(';'):
                            traduccion = translate(definition,"es")# traduce del ingles al español
                            print(traduccion)
                            definiciones.append(traduccion)# agrega la traducion a la lista
                else:
                    print("No se encontraron definiciones para la palabra.")
        lista_defini = list(definiciones)#pasar las definiciones encontrados a la lista
        for defini in lista_defini:#recorrer la lista de definiciones para guardar en la base
            cur = conn.cursor()
            query = ("INSERT INTO definiciones (IdPalabra,Definiciones)VALUE(%s,%s)")#proceso de insercion en la base
            valores = (IdPalabra,defini)
            cur.execute(query, valores)
            cur.connection.commit()
        cur.close()
        return json.dumps(lista_defini)#retorna al front la lista de definiciones encontrados en formato json

@app.route('/get_chat', methods=['POST'])
def getChat():
    if request.method == "POST":
        cadena = request.form['IdPregunta']#SELECT Respuestas FROM chat WHERE Respuestas LIKE '%Cuenta%';
        stop_words = set(stopwords.words('spanish'))  # Utiliza 'spanish' para español
        palabras = word_tokenize(cadena)
        palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stop_words]
        for row in palabras_filtradas:
            query = ("SELECT Respuestas FROM chat WHERE Preguntas LIKE %s")
            cur = conn.cursor()
            cur.execute(query,(f"%{row}%",))
            results = cur.fetchmany()
            cur.close()
        return json.dumps(results)
    
@app.route('/estudiantes')
def estudiantes():
    return render_template('secure/estudiantes.html')

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginAdmin():
    usu = admin.loginAdmin()
    for usr in usu:
        session['idusuario'] = usr[0]
        session['usuario'] = usr[1]
    return jsonify(usu)

@app.route('/administrador')
def administrador():
   return render_template('admin/administrador.html')

@app.route('/publicar')
def publicar():
    pub = admin.listarPublicados()
    return render_template('admin/publicar-proyectos.html', pub = pub)

@app.route('/get_mod_chat', methods=['GET', 'POST'])
def getModificarChatId():
    chatid = admin.getModificarChatId()
    return jsonify(chatid)

@app.route('/modchat', methods=['GET', 'POST'])
def getModificarChat():
    mchat = admin.getModificarChat()
    return jsonify(mchat)

@app.route('/chat')
def chat():
    ch = admin.listarChats()
    return render_template('admin/chat.html', ch = ch)

@app.route('/usuarios')
def usuario():
    users = admin.listarEstudiantesAdmin()
    return render_template('secure/usuarios.html', users = users)

@app.route('/get_correo', methods=['GET'])
def get_correo():
    cconf = admin.getCorreoConfigurado()
    return jsonify(cconf)
 
@app.route('/guardar_correo', methods=['POST'])
def guardar_correo():
    cc = admin.guardarCorreo()
    return jsonify(cc)

@app.route('/correo_configurado')
def correo():
    cc = admin.getCorreoConfigurado()
    return render_template('secure/correo.html', cc = cc)

@app.route('/publicados')
def publicadosPDF():
    pub = admin.listarPublicacionesAdmin()
    return render_template('admin/publicados.html', pub = pub)

@app.route('/articulos')
def articulos():
    pub = admin.listarArticulosAdmin()
    return render_template('documents/articulos.html', art = pub)

@app.route('/publicaciones')
def publicacionesPDF():
    pub = admin.listarPublicacionesAdmin()
    return render_template('documents/publicaciones.html', pub = pub)

@app.route('/get_mod_publicacion', methods=['GET', 'POST'])
def getModificarPublicacionId():
    mpubid = admin.getModificarPublicacionId()
    return jsonify(mpubid)

@app.route('/mod_publicacion', methods=['GET', 'POST'])
def getModificarPublicacion():
    muser = session['idusuario']
    mpub = admin.getModificarPublicacion(muser)
    return jsonify(mpub)#

@app.route('/tipo_identificacion', methods=['GET'])
def tipoidentificacion():
    tident = admin.getTipoTdentificacion()
    return jsonify(tident)

@app.route('/tipo_publicaion', methods=['GET'])
def tipo_publicaion():
    tident = admin.getTipoPublicacion()
    return jsonify(tident)

@app.route('/roles_usuario', methods=['GET'])
def roles_usuario():
    tident = admin.getRolesUsuario()
    return jsonify(tident)

@app.route('/preguntas_validacion', methods=['GET'])
def preguntasvalidacion():
    pval = admin.getPreguntasValidacion()
    return jsonify(pval)

@app.route('/activar_usuario', methods=['POST'])
def getActivarUsuario():
    usu = admin.getActivarUsuario()
    return jsonify(usu)

@app.route('/moduser', methods=['POST'])
def getModUsuario():
    usu = admin.getMUsuario()
    return jsonify(usu)

@app.route('/modroluser', methods=['POST'])
def modroluser():
    usu = admin.getMRolUsuario()
    return jsonify(usu)

@app.route('/eliminar_usuario', methods=['POST'])
def getEliminarUsuario():
    usu = admin.getEliminarUsuario()
    return jsonify(usu)

@app.route('/eliminar_chat', methods=['POST'])
def getEliminar_Chat():
    usu = admin.getEliminarChat()
    return jsonify(usu)

@app.route('/consultas')
def consultas():
    us = session['idusuario']
    csts = admin.listarConsultas(us)
    return render_template('secure/consultas.html', csts = csts)

@app.route('/texto_consulta', methods=['POST'])
def getTextoConsulta():
    if request.method == "POST":
        IdConsulta = request.form['IdConsulta']
        query = ("SELECT Texto FROM consultas WHERE IdConsulta = %s")
        cur = conn.cursor()
        cur.execute(query,IdConsulta)
        csl = cur.fetchall()
        cur.close()
        for row in csl:
            for column in row:
                base64_string = column.decode('utf-8')
        return jsonify(base64_string)

@app.route('/palabras_encontradas', methods=['POST'])
def getPalabrasConsulta():
    if request.method == "POST":
        IdConsulta = request.form['IdConsulta']
        query = ("SELECT IdPalabra,Palabras FROM palabras_consulta WHERE IdConsulta = %s")
        cur = conn.cursor()
        cur.execute(query,IdConsulta)
        pcsl = cur.fetchall()
        cur.close()
        return jsonify(pcsl)

@app.route('/get_sinonimos_consulta', methods=['POST'])
def get_sinonimos_consulta():
    if request.method == "POST":
        IdPalabra = request.form['IdPalabra']
        query = ("SELECT Palabras FROM sinonimos WHERE IdPalabra = %s")
        cur = conn.cursor()
        cur.execute(query,IdPalabra)
        snm = cur.fetchall()
        cur.close()
        return jsonify(snm)

@app.route('/get_deficiciones_consulta', methods=['POST'])
def get_deficiciones_consulta():
    if request.method == "POST":
        IdPalabra = request.form['IdPalabra']
        query = ("SELECT Definiciones FROM definiciones WHERE IdPalabra = %s")
        cur = conn.cursor()
        cur.execute(query,IdPalabra)
        defini = cur.fetchall()
        cur.close()
        return jsonify(defini)

@app.route('/get_consultas', methods=['POST'])
def get_consultas():
    if request.method == "POST":
        us = session['idusuario']
        query = """SELECT C.IdConsulta,CONCAT(U.Nombres,' ',U.Apellidos) AS 'Estudiantes',C.Texto,E.Estado
        FROM consultas C
        INNER JOIN usuarios U ON (C.IdUsuario=U.IdUsuario)
        INNER JOIN estados E ON (C.IdEstado=E.IdEstado) WHERE U.IdUsuario = %s ORDER BY C.IdConsulta DESC"""
        cur = conn.cursor()
        cur.execute(query,us)
        cstas = cur.fetchall()
        cur.close()
        for clt in cstas:
            for cl in clt:
                #name = "b'Cuando la vida se ensa\xc3\xb1a contigo y te apalea con fuerza no debes darte por vencido, debes ser m\xc3\xa1s fuerte que la vida misma y seguir adelante, si te tira una vez, lev\xc3\xa1ntate dos veces mas, g\xc3\xa1nale tiempo al tiempo, as\xc3\xad te har\xc3\xa1s m\xc3\xa1s fuerte y no habr\xc3\xa1 nada que te pueda derrotar.'"
                name = cl.encode('latin')
                name = name.decode()
        return jsonify(name)

@app.route('/UpDocumento', methods=['GET', 'POST'])
def UpDocumento():
    iduser = session['idusuario']
    up = admin.publicarDocumento(iduser)
    if up:
        flash('Publicado OK!.')
        return redirect(url_for('publicar'))
    else:
        flash('Error al publicar!.')
        return redirect(url_for('publicar'))
    return up

if __name__ == "__main__":
    #app.run(host="192.168.1.134", port=80, debug=True)
    app.run(port=3000, debug=True)