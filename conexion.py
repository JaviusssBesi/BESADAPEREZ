from PyQt5 import QtWidgets, QtSql
import pymongo, var

# class Conexion():
#     def db_connect(filename):
#         db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
#         db.setDatabaseName(filename)
#         if not db.open():
#             QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos','No se puede establecer conexion.\n'
#                                             'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
#             return False
#         else:
#             print('Conexión Establecida')
#         return True
#
#     def cargarCli(cliente):
#         query = QtSql.QSqlQuery()
#         query.prepare('insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago)'
#                     'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago)')
#         query.bindValue(':dni', str(cliente[0]))
#         query.bindValue(':apellidos', str(cliente[1]))
#         query.bindValue(':nombre', str(cliente[2]))
#         query.bindValue(':fechalta', str(cliente[3]))
#         query.bindValue(':direccion', str(cliente[4]))
#         query.bindValue(':provincia', str(cliente[5]))
#         query.bindValue(':sexo', str(cliente[6]))
#         # pagos = ' '.join(cliente[7]) si quiesesemos un texto, pero nos viene mejor meterlo como una lista
#         query.bindValue(':formaspago', str(cliente[7]))
#         #  print(pagos)
#         if query.exec_():
#             print("Inserción Correcta")
#         else:
#             print("Error: ", query.lastError().text())

class Conexion():
    HOST = 'localhost'
    PORT = '27017'
    URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'
    var.DATABASE = 'empresa'
    try:
        print('Conexión realizada al servidor %s'  %HOST)
    except:
        print('Error conexion')