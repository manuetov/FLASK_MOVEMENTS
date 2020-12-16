# Este fichero se crea para que movements actue como un módulo.
from flask import Flask # Se importa la clase Flask, del un modulo flask

app = Flask(__name__)# se crea una instancia y como parametro se pone el nombre de nuestra aplicación 
# que es el nombre de nuestro fichero para que se identifique como tal. Resultaría indispensable en el 
# caso de tener un servidor con varias aplicaciones Flask. Esto es similar a: if name ==' main '

from movements import views
