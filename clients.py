import conexion, clients
from venavisos import *
import var

class Clientes():
    def validarDni(dni):
        """

        Móudulo que valida la letra de un dni según sea nacional o extranjerao

        :param a: dni
        :type: string
        :return: None
        :rtype: bool

        Pone la letra en mayúsculas, comprueba que son nueve caracteres. Toma los 8 primeros, si extranjero
        cambia la letra por el número, y aplica el algoritmo de comprobación de la letra basado en la normativa
        Si es correcto devuelve True, si es falso devuelva False

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

        Modulo que según sea correcto el dni o no, muestra una imagen distinta

        :return: none

        Si es falso escribe en el label una cruz roja si es true devuelve una V verda

        """
        try:
            dni = var.ui.editDni.text()
            if Clientes.validarDni:
                var.ui.lblValidar.setStyleSheet('QLabel {color: green;}')
                var.ui.lblValidar.setText('V')
                var.ui.editDni.setText(dni.upper())
            else:
                var.ui.lblValidar.setStyleSheet('QLabel {color: red;}')
                var.ui.lblValidar.setText('X')
                var.ui.editDni.setText(dni.upper())
                message = 'DNI INCORRECTO   '
                #events.Eventos.AbrirAviso(message)
                clients.Clientes.limpiarCli()
        except Exception as error:
            print('Error: %s' % str(error))
            print('Error módulo escribir valido DNI')
            return None


    def selSexo(self):
        '''

        Modulo que según checkemos el rbtbutton Fem o Masc carga el texto correspondiente de Mujer o Hombre a la
        variable var.sex que luego se añade a la lista de los datos del cliente a incluir en la BBDD

        :return: None
        :rtype: None

        '''
        try:
            if var.ui.rbtFem.isChecked():
                var.sex = 'Mujer'
                var.ui.rbtMasc.setChecked(False)
            if var.ui.rbtMasc.isChecked():
                var.sex = 'Hombre'
                var.ui.rbtFem.setChecked(False)
        except Exception as error:
            print('Error: %s' % str(error))

    def selPago():
        '''

        Cheque que valores de paga seleccion en el checkbos y los añade a una variable lista var.py

        :return: None

        En QtDesigner se debe agrupar los checkbox en un ButtonGroup

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
        '''

        Al seleccion una provincia en el combo de provincias llama al evento cmbProv.activated que devuelve
        la provincia selecccionada

        :param a: provincia seleccionada
        :type a: string
        :return: None
        :rtype: None

        '''
        try:
            global vpro
            vpro = prov
        except Exception as error:
            print('Error: %s' % str(error))

    def abrirCalendar(self):
        '''

        Modulo que abre la ventana calendario

        '''
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def cargarFecha(qDate):
        """

        Módulo que carga la fecha marcada en el widget Calendar

        :parama a: librería python para formateo de fehcas
        :return: None
        :rtype: formato de fechas python

        A partir de los eventos Calendar.clicked.connect al clickear en una fecha, captura y la carga el widget edit
        que almacena la fecha

        """
        try:
            if var.ui.tabWidget.currentIndex() == 0:
                data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
                var.ui.editClialta.setText(str(data))
                var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altaCliente(self):
        """

        Módulo que carga los datos del cliente

        :param a: None
        :param b: None
        :return: None

        Se crea una lista newcli que contendrá todos los datos del cliente que se introduzcan en los widgets,
        esta lista se pasa como argumento al módulo altaCli del módulo Conexión.
        El módulo llama a la función mostrarClientes que recarga la tabla con todos los clientes además del nuevo
        El módulo llama a la función limpiarCli que vacía el contenido de los widgets.

        """
        try:
            newcli = []
            clitab = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            k = 0
            for i in client:
                newcli.append(i.text())
                if k < 3:
                    clitab.append(i.text())
                    k += 1
            newcli.append(vpro)
            newcli.append(var.sex)
            var.pay2 = Clientes.selPago
            newcli.append(var.pay2)
            edad = var.ui.spinEdad.value()
            newcli.append(edad)
            if client:
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
            print('Error cargar cliente : %s ' % str(error))

    def limpiarCli():
        '''

        Modulo que vacía o limpia los datos del formulario cliente

        :return: None

        En los checkbox y radiobutton los pone a False.

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

    def cargarCli(self):
        '''

        Modulo que se activa con el evento clicked.connec y setSelectionBehavior del widget TtableCli

        :return: None
        :rtype: None

        Al generarse el evento se llama al módulo de Conexion cargarCliente que devuelve los datos del cliente
        seleccionado haciendo una llamada a la BBDD

        '''
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
                if i == 0:
                    var.ui.editDniclifac.setText(fila[0])
                if i == 1:
                    var.ui.editApelclifac.setText(fila[1])
            conexion.Conexion.cargarCliente(self)
        except Exception as error:
            print('Error cargar clientes: %s ' % str(error))

    def bajaCliente():
        """

        Módulo que da de baja un cliente a partir del dni. Además recarga el widget tablaCli con los datos actualizados
        desde la BBDD

        :return: None
        :rtype: None

        Toma el dni cargado en el widget editDni se lo pasa al módulo bajaCli de la clase Conexión y da de bja el cliente.
        Limpia los datos del formulario y recarga tablaCli

        """
        try:
            print('Baja cliente')
            dni = var.ui.editDni.text()
            conexion.Conexion.bajaCli(dni)
            Clientes.limpiarCli()
            var.dlgaviso.hide()
            conexion.Conexion.mostrarClientes(None)
        except Exception as error:
            print('Error ventana baja cliente: %s ' % str(error))

    def modifCliente(self):
        """

        Módulos para modificar datos de un cliente con determinado código

        :return: None
        :rtype: None

        A partir del código del cliente, lee los nuevos datos de los widgets que se han cargado y modificado,
        llama al módulo modifCli de la clase Conexión para actualizar los datos en la BBDD pasándole una lista con
        los nuevos datos.
        Vuelve a mostrar la tablaCli actualizada pero no limpia datos de los widgets.

        """
        try:
            newdata = []
            client = [var.ui.editDni, var.ui.editApel, var.ui.editNome, var.ui.editClialta, var.ui.editDir]
            for i in client:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            newdata.append(var.ui.cmbProv.currentText())
            newdata.append(var.sex)
            var.pay = Clientes.selPago
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

        Limpia datos formulario y recarga la tabla de clientes llamando al módulo mostrarClientes de la clase
        Conexion

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

        Busca un Cliente a partir de un dni que introduce el usuario

        :return: None
        :rtype: None

        Toma el dni del widget editDni y llama a la función buscaCli de la clase Conexión a la que le pasa el dni.

        """
        try:
            dni = var.ui.editDni.text()
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error buscar clientes: %s ' % str(error))


    def valoresSpin():
        '''

        Módulo que se lanza con el programa cargando por defecto el valor 16 en el spinEdad

        :return: None
        :rtype: None

        '''

        try:
            var.ui.spinEdad.setValue(16)
        except Exception as error:
            print('Error valores spin: %s ' % str(error))