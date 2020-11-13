 from PyQt5 import QtWidgets, QtSql
 import pymongo, var

 class Conexion():
     def db_connect(filename):
         db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
         db.setDatabaseName(filename)
         if not db.open():
             QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos','No se puede establecer conexion.\n'
                                            'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True


# class Conexion():
#     HOST = 'localhost'
#     PORT = '27017'
#     URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'
#     var.DATABASE = 'empresa'
#     try:
#         print('Conexión realizada al servidor %s'  %HOST)
#     except:
#         print('Error conexion')