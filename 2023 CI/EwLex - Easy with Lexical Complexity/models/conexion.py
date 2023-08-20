from flask import Flask, session, render_template, request, redirect, url_for, flash
import pymysql as bd
def DB():
        try:
           conn =bd.connect(host='localhost',user='root',password='',db='ewlex_bd',charset="utf8mb4") 
           print("OK! conexión exitosa")
           return conn
        except Exception as e:
            print("Ocurrió un error al conectar a BD: ", e)
            return e