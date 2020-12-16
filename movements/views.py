# En el fichero views estaran todos los puntos de entrada, las rutas (@*.route)
from movements import app
from flask import render_template, request, url_for, redirect # se importa la función render_template de Flask
import sqlite3
import csv

DBFILE ='movements/Data/basededatos.db'

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE) # establece la conexión
    c = conn.cursor() # c se guarda el cursor que permite crear instancias y relacionarlas

    c.execute(query, params) # execute "darle al play" lee la base de datos
    conn.commit()
    filas = c.fetchall() # guarda en filas una lista con todos los registros de basededatos
    conn.close() # cierra la conexión

    
    if len(filas) == 0: # si la lista está vacia no devuelve nada.
        return None
    # si la condición anterior no se cumple es que la lista tiene algo y devuelve un diccionario
    
    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []
    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/') # se encarga de decirle a Flask que url ('/') debe ejecutar su correspondiente función.
def listaIngresos():
    
    ingreso = consulta ('SELECT fecha, concepto, cantidad, id FROM movimientos;') # guarda la muestra de los campos desde movimientos en la variable ingreso.

    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2]) # acumula en una variable el elemento 2 que corresponde a la cantidad en €
    
    conn.close() # cierra la conexión
    
    return render_template("movementsList.html", datos=ingresos, total=sumador) # La función render_template le pasa las variables clave valor al fichero movementsList.html
    # le pasa la variable ingresos (una lista de lista) y se lo pasa a jinja y este al servidor

@app.route('/creaalta', methods=["GET", "POST"]) # methods una lista con los metodos que vamos a permitir con el nombre de estos en mayuscula, sino se especifica el metodo por defecto siempre es GET
def nuevoIngreso():
    if request.method == "POST": #El objeto request nos servirá para acceder a la información que nos envíe el cliente, que son los parámetros, GET o POST
        
        consulta('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?,?,?);', # consulta ??? es similar a {}.format. inserta datos en los campos de la basededatos
                (
                    float(request.form.get('cantidad')), request.form.get('concepto'), request.form.get('fecha') # tupla introduce en ?
                ))

        return redirect(url_for('listaIngresos')) # url_for: redierecciona a la función listaIgresos de la ruta @
    
    return render_template("alta.html")

@app.route('/modifica/<id>', methods=['GET', 'POST']) # <id> es una variable que se le pasa como parametro a la función
def modificaIngreso(id):
    conn = squlite3.connect(DBFILE)
    c = conn.cursor()
    
    if request.method == 'GET':
        registro = consulta('SELECT fecha, concepto, cantidad, id FROM movimientos where id=?', (id,)) # (id,)) la coma es para indicar que es una dupla 
        
        return render_template("modifica.html", registro=registro)
    else:
        consulta('UPDATE movimientos SET fecha=?, concepto=?, cantidad=? WHERE id = ?',
                    (request.form.get('fecha'), request.form.get('concepto'), float(request.form.get('cantidad')), (id,)) # request : cuando llega una petición flask crea una objeto(instancia) 
                    # que se llama request en la que vienen todos los datos de la petición. Los formularios vienen siempre en request.form que son un diccionario y se obtiene por clave 
                    # y dicha clave está en el name del formulario en modifica_html 
    
        return redirect(url_for('listaIngresos'))


    '''
    fIngresos = open("movements/Data/basededatos.csv", 'r') # se abre el fichero basededatos.cvs en modo "r"-lectura y se guarda en la variable fIngreso
    csvReader = csv.reader(fIngresos, delimiter=",", quotechar='"') # usa el metodo reader para delimitar los datos del fichero csv por "," y omite los que vayan entre ' " ' y lo guarda la variable csvReader
    ingresos = list(csvReader) # transforma un fichero .csv en una lista para que jinja lo reconozca. sino se guradase en una lista se guardaria en un objeto y Jinja no lo reconocería.
    
    
    fIngresos = open("movements/Data/basededatos.csv", 'a', newline="") # abrimos el fichero en modo escritura 'a'
    csvWriter = csv.writer(fIngresoso, delimiter=',', quotechar='"') # escritor
    csvWriter.writerow([request.form.get('fecha'), request.form.get('concepto'), request.form.get('cantidad')]) # escribo una fila
        
    DIFERENTES TIPOS DE CONSULTAS QUE SE PUEDEN REALIZAR A UN BASE DE DATOS

    SELECT * FROM TABLA -> [(), (),()] devuelve unas listas vacías de dupla
    SELECT * FROM TABLA -> []
    INSERT ... -> []
    UPDATE ... -> []
    DELETE ... -> []
    
    '''