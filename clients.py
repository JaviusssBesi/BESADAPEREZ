import var, conexion, events, clients
from venavisos import *

class Clientes():
    """
    eventos necesarios formulario clientes
    """
    def validarDni(dni):
        """
        Código que controla si el dni o nie es correcto
        :return:
        """
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
                    dni  = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni)%23] == dig_control

        except Exception as error:
            print('Error módulo validar DNI %s' % str(error))
            return None

    def validoDni():
        """
        muestra mensaje de dni válido
        :return: none
        """
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
                men = 'DNI INCORRECTO   '
                events.Eventos.AbrirAviso(men)
                clients.Clientes.limpiarCli()
        except Exception as error:
            print('Error: %s' % str(error))
            print('Error módulo escribir valido DNI')
            return None

    def selSexo(self):
        try:
            if var.ui.rbtFem.isChecked():
                var.sex =  'Mujer'
            if var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error: %s' % str(error))

    def selPago():
        '''
        chequea que valores de pago han sido activados
        agrupamos en QtDesigner los checkbox en un ButtonGroup
        :return: devuelve una lista de valores
        '''
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                if data.isChecked() and i == 0:
                   var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                   var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                   var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error: %s' % str(error))

    def selProv(prov):
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error: %s' % str(error))

    def abrirCalendar(self):
        '''
        Abrir la ventana calendario
        '''
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def cargarFecha(qDate):
        ''''
        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
        '''
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.editClialta.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altaCliente(self):  #SE EJECUTA CON EL BOTÓN ACEPTAR
        '''
        cargará los clientes en la tabla y en la base de datos
        cargará datos cliente en el resto widgets
        en las búsquedas mostrará los datos del cliente
        :return: none
        '''
        #preparamos el registro
        try:
            newcli = [] #contiene todos los datos
            clitab = []  #será lo que carguemos en la tablas
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
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
            edad = var.ui.spinEdad.value()
            newcli.append(edad)
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
                conexion.Conexion.altaCli(newcli)
            else:
                print('Faltan Datos')
            conexion.Conexion.mostrarClientes(None)
            Clientes.limpiarCli()
        except Exception as error:
            print('Error cargar fecha lo : %s ' % str(error))

    def limpiarCli():
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in range(len(client)):
                client[i].setText('')
            var.ui.grpbtnSex.setExclusive(False)  #necesario para los radiobutton
            for dato in var.rbtsex:
                dato.setChecked(False)
            for data in var.chkpago:
                data.setChecked(False)
            var.ui.cmbProv.setCurrentIndex(0)
            var.ui.lblValidar.setText('')
            var.ui.lblCodcli.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def cargarCli():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [ var.ui.editDni, var.ui.editApel, var.ui.editNome ]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
            conexion.Conexion.cargarCliente()
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def bajaCliente():
        """
        módulos para dar de baja un cliente
        :return:
        """
        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.bajaCli(dni)
            Clientes.limpiarCli()
            var.dlgaviso.hide()
            conexion.Conexion.mostrarClientes(None)
        except Exception as error:
            print('Error ventana baja cliente: %s ' % str(error))

    def modifCliente(self):
        """Módulos para modificar datos de un cliente con determinado código

        :return: None
        """
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in client:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            newdata.append(var.ui.cmbProv.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.selPago()
            newdata.append(var.pay)
            edad = var.ui.spinEdad.value()
            newdata.append(edad)
            cod = var.ui.lblCodcli.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarClientes(self)

        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def reloadCli():
        '''
        Limpia datos formulario y recarga la tabla de clientes
        :return: None
        '''
        try:
            print(var.ui.spinEdad.value())
            Clientes.limpiarCli()
            conexion.Conexion.mostrarClientes(None)
        except Exception as error:
            print('Error recargar clientes: %s ' % str(error))

    def buscarCli(self):
        """
        Busca un Cliente a partir de un dni que escribe el usuario
        :return: mensaje
        """
        try:
            #Clientes.limpiarCli()
            dni = var.ui.editDni.text()
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error buscar clientes: %s ' % str(error))

    def valoresSpin():
        try:
            var.ui.spinEdad.setValue(16)
        except Exception as error:
            print('Error valores spin: %s ' % str(error))