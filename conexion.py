from PyQt5 import QtSql
import pymongo, var
from ventana import *

class Conexion():
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(filename))
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos','No se puede establecer conexion.\n'
                                            'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    def altaCli(cliente):
        query = QtSql.QSqlQuery()
        query.prepare('insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago)'
                    'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        # pagos = ' '.join(cliente[7]) si quiesesemos un texto, pero nos viene mejor meterlo como una lista
        query.bindValue(':formaspago', str(cliente[7]))
        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Alta Cliente con dni ' + str(cliente[0]))
            Conexion.mostrarClientes()
        else:
            print("Error: ", query.lastError().text())

    def cargarCliente():
        '''
        Módulo que carga el resto de widgets con los datos del cliente dni
        :return: None
        '''
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editClialta.setText( query.value(4))
                var.ui.editDir.setText(query.value(5))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

    def mostrarClientes(self):
        '''
        Carga los datos principales del cliente en la tabla
        se ejecuta cuando lanzamos el programa, actualizamos, insertamos y borramos un cliente
        :return: None
        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                #cojo los valores
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                # crea la fila
                var.ui.tableCli.setRowCount(index+1)
                #voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index,0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def bajaCli(dni):
        ''''
        modulo para eliminar cliente. se llama desde fichero clientes.py
        :return None
        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni '+ dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())


    def modifCli(codigo, newdata):
           ''''
           modulo para modificar cliente. se llama desde fichero clientes.py
           :return None
           '''
           query = QtSql.QSqlQuery()
           codigo = int(codigo)
           query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                         'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago where codigo=:codigo')
           query.bindValue(':codigo', int(codigo))
           query.bindValue(':dni', str(newdata[0]))
           query.bindValue(':apellidos', str(newdata[1]))
           query.bindValue(':nombre', str(newdata[2]))
           query.bindValue(':fechalta', str(newdata[3]))
           query.bindValue(':direccion', str(newdata[4]))
           query.bindValue(':provincia', str(newdata[5]))
           query.bindValue(':sexo', str(newdata[6]))
           query.bindValue(':formaspago', str(newdata[7]))

           if query.exec_():
               print('Cliente modificado')
               var.ui.lblstatus.setText('Cliente con dni '+ str(newdata[0]) + ' modificado')
           else:
               print("Error modificar cliente: ", query.lastError().text())

    def buscaCli(dni):
        """
        select un cliente a partir de su dni.
        :return:
        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.editApel.setText(str(query.value(1)))
                var.ui.editNome.setText(str(query.value(2)))
                var.ui.editClialta.setText(query.value(4))
                var.ui.editDir.setText(query.value(5))
                var.ui.cmbProv.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFem.setChecked(True)
                    var.ui.rbtMasc.setChecked(False)
                else:
                    var.ui.rbtMasc.setChecked(True)
                    var.ui.rbtFem.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)

                var.ui.tableCli.setRowCount(index + 1)
                    # voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

# class Conexion():
#     HOST = 'localhost'
#     PORT = '27017'
#     URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'
#     var.DATABASE = 'empresa'
#     try:
#         var.client = pymongo.MongoClient(URI_CONNECTION)
#         var.client.server_info()
#         print('Conexión realizada al servidor %s'  %HOST)
#     except:
#         print('Error conexion')