# Requerimientos
- mysql 8.0.33
- python 3.10.8
- Workbench 8.0
# Librerías utilizadas
- pymysql (Librería para la conexión a la base de datos)
- openai (Librería que permite utilizar el API de OpenAi)
- colorama (Librería pintar los mensaje por consola)
- dotenv (Librería que permite leer los archivos .env de configuración)
- pandas (Librería para la manipulación y tratamiento de datos)
- sys (Usado para terminar la ejecución en caso de problemas con el API)
- os (Usado para validar rutas)
- re (Permite el uso de expresiones regulares)
# Tablas usadas en la base de datos
- task2_test_small (Tabla que contiene el conjunto de datos a evaluar)
- result_task2_1 (Tabla que donde se guardara los resultados del task 2.1)
- result_task2_2 (Tabla que donde se guardara los resultados del task 2.2)
- task_exec (Tabla donde se guardara informacion sobre la ejecución)
# Conjunto de datos (directorios) proporcionados por los organizadores de la tarea.
- results: Contiene los datos resultantes de la experimentación en distintos formatos (xlsx, json y tsv).
- test: Contiene los conjuntos de datos usados para el testeo en formato json y tsv.
-	test_conv: Contiene los conjuntos de datos de testeo convertidos a xlsx para mejor visualización.
-	train: Conjunto de datos de entrenamiento en formato json y tsv. 
-	train_conv: Conjunto de datos de entrenamiento convertido a xlsx para mejor visualización.


Link al colab con una breve descripción del codigo (codigo no funcional ya que esta configurado para una base de datos local)
https://colab.research.google.com/drive/1io7GiE3hQD_2-pnAEcW0H5Q269uxZkZ5?usp=sharing