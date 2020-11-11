import var, conexion
from ventana import *

class Clientes():
    '''
    eventos clientes
    '''
    def validarDni(dni):
        '''
        Código que controla si el dni o nie es correcto
        :return:
        '''
        try:
            tabla = 'TRWAGMYFPDXBNJZSQVHLCKE'
            dig_ext = 'XYZ'
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = '0123456789'
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni  = dni.replace(dni[0],reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23 ] == dig_control

        except:
            print('Error módulo validar DNI')
            return None

    def validoDni():
        '''
        muestra mensaje de dni válido
        :return: none
        '''
        try:
            dni = var.ui.editDni.text()
            if Clientes.validarDni(dni):
                var.ui.lblValidar.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())

        except:
            print('Error módulo escribir valido DNI')
            return None

    def selSexo():
        try:
            if var.ui.rbtFem.isChecked():
                var.sex =  'Mujer'
            if var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error: %s' % str(error))

    def selPago():
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                #agrupamos en QtDesigner los checkbox en un ButtonGroup
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')
            #var.pay = set(var.pay)
            #print (var.pay)
            return var.pay
        except Exception as error:
            print('Error: %s' % str(error))

    def selProv(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error: %s' % str(error))

    '''
    Abrir la ventana calendario
    '''
    def abrirCalendar():
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    '''
    Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
    '''

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editClialta.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def showClientes():  #SE EJECUTA CON EL BOTÓN ACEPTAR
        '''
        cargará los clientes en la tabla
        :return: none
        '''
        #preparamos el registro
        try:
            newcli = []
            clitab = []  #será lo que carguemos en la tablas
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir ]
            k = 0
            for i in client:
                newcli.append(i.text())  #cargamos los valores que hay en los editline
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            newcli.append(var.sex)
            var.pay2 = Clientes.selPago()
            newcli.append(var.pay2)
            print(newcli)
            if client:
            #comprobarmos que no esté vacío lo principal
            #aquí empieza como trabajar con la TableWidget
                row = 0
                column = 0
                var.ui.tableCli.insertRow(row)
                for registro in clitab:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tableCli.setItem(row, column, cell)
                    column +=1
                conexion.Conexion.cargarCli(newcli)
            else:
                print('Faltan Datos')
            Clientes.limpiarCli(client, var.rbtsex, var.chkpago)
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def limpiarCli(listaeditCli, listaRbtsex, listaChkpay):
        '''
        limpia los datos del formulario cliente
        :param listaRbtsex:
        :param listaChkpay:
        :return: none
        '''
        try:
            for i in range(len(listaeditCli)):
                listaeditCli[i].setText('')
            var.ui.grpbtnSex.setExclusive(False)  #necesario para los radiobutton
            for dato in listaRbtsex:
                dato.setChecked(False)
            for data in listaChkpay:
                data.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def cargarCli(self):
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [ var.ui.editDni, var.ui.editApel, var.ui.editNome ]
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])

        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

























