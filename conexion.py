from PyQt5 import QtSql, QtCore
import var, ventas
from ventana import *



class Conexion():
    def db_connect(filename):
        '''

        Módulo que realiza la conexión de la aplicación con la BBDD

        :param filename: nombre de la BBDD
        :type: string
        :return: True o False
        :rtype: bool

        Utiliza la librería de QtSql y el gestor de la BBDD es QSQlite. En caso de error muestra pantalla
        de aviso.

        '''
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(str(filename))
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la base de datos',
                                           'No se puede establecer conexion.\n'
                                           'Haz Click para Cancelar.', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexión Establecida')
        return True

    def altaCli(cliente):
        '''

        Da de alta un cliente cuyos datos se pasan por una lista.
        Muestra mensaje de resultado en el barra de estado.
        Recarga la tabla actualizada de clientes

        :param: cliente
        :type: lista
        :return: None
        :rtype: None

        '''
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre, fechalta, direccion, provincia, sexo, formaspago, edad)'
            'VALUES (:dni, :apellidos, :nombre, :fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        # pagos = ' '.join(cliente[7]) si quiesesemos un texto, pero nos viene mejor meterlo como una lista
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', int(cliente[8]))
        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Alta Cliente con dni ' + str(cliente[0]))
            Conexion.mostrarClientes(None)
        else:
            print("Error: ", query.lastError().text())

    def cargarCliente(self):
        '''

        Muestra los datos por pantalla de un cliente cuando se clickea sobre el mismo en la tabla.

        :return: None
        :rtype: None

        '''
        dni = var.ui.editDni.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
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
                var.ui.spinEdad.setValue(int(query.value(9)))

    def mostrarClientes(self):
        '''

        Módulo que carga los datos del cliente por orden alfabético en la tabla Clientes

        :return: None
        :rtype: None

        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes order by apellidos, nombre')
        if query.exec_():
            while query.next():
                # cojo los valores
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                # crea la fila
                var.ui.tableCli.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def bajaCli(dni):
        ''''

        Módulo para eliminar cliente.

        :param dni
        :type: string
        :return None
        :rtype None

        Se pasa como argumento el dni del cliente a eliminar.
        A continuación recarga la tablaCli actualizada
        Muestra mensje resultado en la barra de estado

        '''
        print('Baja cliente')
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():

            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print("Error mostrar clientes: ", query.lastError().text())
            var.ui.lblstatus.setText('Error baja cliente con dni ' + dni + ' ')
        Conexion.mostrarClientes(None)

    def modifCli(codigo, newdata):
        '''

        Módulo que actualiza datos de clinte

        :param codigo: código cliente
        :type codigo: int
        :param newdata: datos cliente
        :type newdata: lista
        :return: None
        :rtype: None

        Recibe como parámetros el código del cliente a modificar así como los datos que deseamos modificar.
        En realidad toma todos los datos que hay en los widgets de la pantalla clientes.

        '''
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre, fechalta=:fechalta, '
                      'direccion=:direccion, provincia=:provincia, sexo=:sexo, formaspago=:formaspago, edad=:edad where codigo=:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', int(newdata[8]))

        if query.exec_():
            print('Cliente modificado')
            var.ui.lblstatus.setText('Cliente con dni ' + str(newdata[0]) + ' modificado')
        else:
            print("Error modificar cliente: ", query.lastError().text())

    def buscaCli(dni):
        '''

        Módulos que busca un cliente y carga sus datos en la pantalla cliente

        :param dni: dni cliente a buscar
        :type dni: string
        :return: None
        :rtype: None

        '''

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
                var.ui.spinEdad.setValue(query.value(9))

                var.ui.tableCli.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(1))))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(2))))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(str(query.value(3))))

    '''
    Xestión Productos
    '''

    def altaProducto(producto):
        """

        Da de alta a un producto cuyos datos se pasan por una lista. Muestra mensaje de resultado en la barra de estado
        Recarga la tabla de productos actualizada

        :param : producto a cargar
        :type: lista
        :return: none
        :rtype: none

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into productos (producto, precio, stock)'
            'VALUES (:producto, :precio, :stock)')
        query.bindValue(':producto', str(producto[0]))
        producto[1] = producto[1].replace(',', '.')
        query.bindValue(':precio', round(float(producto[1]), 2))
        query.bindValue(':stock', int(producto[2]))
        if query.exec_():
            var.ui.lblstatus.setText('Alta Producto ' + str(producto[0]))
        Conexion.mostrarProducts()

    def mostrarProducts(self):
        """

        Modulo que carga los datos del producto por orden alfabetico en
        la tabla productos

        :type: lista
        :return: none
        :rtype: none

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, producto, precio from productos order by producto')
        if query.exec_():
            while query.next():
                codigo = query.value(0)
                producto = query.value(1)
                precio = query.value(2)
                var.ui.tableProd.setRowCount(index + 1)
                var.ui.tableProd.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tableProd.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                var.ui.tableProd.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                var.ui.tableProd.item(index, 0).setTextAlignment(QtCore.Qt.AlignCenter)
                var.ui.tableProd.item(index, 1).setTextAlignment(QtCore.Qt.AlignCenter)
                var.ui.tableProd.item(index, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                index += 1
        else:
            print("Error mostrar clientes: ", query.lastError().text())

    def cargarProd(cod):
        """

        Carga los datos de un producto cuando se cliquea sobre el en la
        tabla

        :param cod: codigo del producto
        :type cod: entero
        :return: none
        :rtype: none

        """
        query = QtSql.QSqlQuery()
        query.prepare('select producto, precio, stock from productos where codigo = :cod')
        query.bindValue(':cod', cod)
        if query.exec_():
            while query.next():
                var.ui.lblCodPro.setText(str(cod))
                var.ui.editArtic.setText(str(query.value(0)))
                var.ui.editPrec.setText(str(query.value(1)))
                var.ui.editStock.setText(str(query.value(2)))

    def bajaPro(cod):
        """

        Modulo para eliminar productos del inventario

        :param cod: codigo del producto
        :type cod: int
        :return: none
        :rtype: none

        Se pasa como argumento el codigo del producto a eliminar, recarga la
        tabla productos actualizada, muestra el mensaje de resultado en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from productos where codigo = :cod')
        query.bindValue(':cod', cod)
        if query.exec_():
            var.ui.lblstatus.setText('Producto de còdigo ' + cod + ' dado de baja')
        else:
            print("Error baja producto: ", query.lastError().text())
        Conexion.mostrarProducts()

    def modificarPro(cod, newdata):
        """

        Modulo que actualiza los datos del producto

        :param cod: codigo del producto
        :type cod: int
        :param newdata: datos producto
        :type newdata: lista
        :return: none
        :rtype: none

        Recibe el codigo del producto a modificar y sus datos.
        Tambien coge los datos de los widgets de la pantalla productos

        """
        cod = int(cod)
        query = QtSql.QSqlQuery()
        query.prepare('update productos set producto=:producto, precio=:precio, stock=:stock where codigo=:cod')
        query.bindValue(':cod', int(cod))
        query.bindValue(':producto', str(newdata[0]))
        newdata[1] = newdata[1].replace(',', '.')
        query.bindValue(':precio', round(float(newdata[1]), 2))
        query.bindValue(':stock', int(newdata[2]))

        if query.exec_():
            var.ui.lblstatus.setText('Producto con código ' + str(cod) + ' modificado')
        else:
            print("Error modificar producto: ", query.lastError().text())

    '''
    Facturación
    '''

    def altaFac(dni, fecha, apel):

        '''

        Módulo que da de alta una factura previa al proceso de venta

        :param dni: dni cliente
        :type dni: string
        :param fecha: fecha de alta de la factura
        :type fecha: formato fecha en string
        :param apel: apellidos del ciente
        :type apel: string
        :return: None
        :rtype: None

        Recibe datos para carga la factura en la BBDD y en la tabla Factura. Además obtiene el código de la
        factura dada de alta para cargarla en el label lblNumFac ya que al ser autonumérico no se obtiene hasta
        que previamente insertemos la factura.

        '''

        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos) VALUES (:dni, :fecha, :apellidos )')
        query.bindValue(':dni', str(dni))
        query.bindValue(':fecha', str(fecha))
        query.bindValue(':apellidos', str(apel))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Creada')
        else:
            print("Error alta factura: ", query.lastError().text())
        query1 = QtSql.QSqlQuery()
        query1.prepare('select max(codfac) from facturas')
        if query1.exec_():
            while query1.next():
                var.ui.lblNumFac.setText(str(query1.value(0)))

    def mostrarFacturas(self):
        '''

        Módulo que carga los datos de la factura por orden descendente numérico en la tabla Facturas

        :return: None
        :rtype: None

        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas order by codfac desc')
        if query.exec_():
            while query.next():
                # crea la fila
                var.ui.tabFac.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tabFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                var.ui.tabFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                index += 1
            Conexion.limpiarFac(self)
            var.ui.tabFac.selectRow(0)
            var.ui.tabFac.setFocus()
        else:
            print("Error mostrar facturas: ", query.lastError().text())
        if index == 0:
            var.ui.tabFac.clearContents()

    def mostrarFacturascli(self):
        '''

        Módulo que carga los datos de la factura de un cliente concreto en los widgets de gestión de factura

        :return: None
        :rtype: None

        Si no existen facturas de ese cliente entonces muestra un aviso

        '''

        index = 0
        cont = 0
        dni = var.ui.editDniclifac.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                # cojo los valores
                cont = cont + 1
                codfac = query.value(0)
                fecha = query.value(1)
                # crea la fila
                var.ui.tabFac.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tabFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tabFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.tabFac.setRowCount(0)
                var.ui.lblstatus.setText('Cliente sin Facturas')
        else:
            print("Error mostrar facturas cliente: ", query.lastError().text())

    def limpiarFac(self):
        '''

        Módulo que borra los datos contenidos en los widgets de gestión de facturas

        :return: None
        :rtype: None

        '''

        datosfac = [var.ui.editDniclifac, var.ui.editDatafac, var.ui.lblNumFac, var.ui.editApelclifac]
        for i, data in enumerate(datosfac):
            datosfac[i].setText('')

    def cargarFac(cod):
        '''

        Módulo que carga datos de un factura en los widgets al clickear sobre una fila de la tablaPro

        :param cod: código de la factura
        :type cod: int
        :return: None
        :rtype: None

        '''
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(cod))
        if query.exec_():
            while query.next():
                var.ui.editDniclifac.setText(str(query.value(0)))
                var.ui.editApelclifac.setText(str(query.value(1)))

    def cargarFac2(self):
        '''

        Módulo que carga datos de un factura en los widgets al clickear sobre una fila de la tablaPro

        :return: None
        :rtype: None

        '''
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, dni, fecha, apellidos from facturas ORDER BY codfac DESC LIMIT 1')
        if query.exec_():
            while query.next():
                var.ui.lblNumFac.setText(str(query.value(0)))
                var.ui.editDniclifac.setText(str(query.value(1)))
                var.ui.editDatafac.setText(str(query.value(2)))
                var.ui.editApelclifac.setText(str(query.value(3)))

    def cargarCmbventa(cmbventa):
        '''

        Módulo que carga los datos en el combobox provincias haciendo un llamada a la BBDD.

        :return: None
        :rtype: None

        '''
        var.cmbventa.clear()
        query = QtSql.QSqlQuery()
        var.cmbventa.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                var.cmbventa.addItem(str(query.value(1)))

    def obtenCodPrec(articulo):
        '''

        Módulo que devuelve el precio y código del producto que se pasa como parámetro

        :param: articulo
        :type: string
        :return: dato
        :rtype: lista que contiene código y precio del producto

        '''

        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio from productos where producto = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                dato = [str(query.value(0)), str(query.value(1))]
        return dato

    def altaVenta():
        '''

        Módulo que añade líneas de venta en una factura creada

        :return: None
        :rtype: None

        Inserta en la tabla ventas una línea de venta que se va mostrando cada vez que realizamos la transacción.
        Tras realizar la venta se crea una nueva factura incluyendo el combobox de selección de artículor

        '''

        query = QtSql.QSqlQuery()
        query.prepare('insert into ventas (codfacventa, codarticventa, cantidad, precio) VALUES (:codfacventa, :codarticventa,'
                      ' :cantidad, :precio )')
        query.bindValue(':codfacventa', int(var.venta[0]))
        query.bindValue(':codarticventa', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))
        row = var.ui.tabVenta.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tabVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tabVenta.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tabVenta.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tabVenta.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row = row + 1
            var.ui.tabVenta.insertRow(row)
            var.ui.tabVenta.setCellWidget(row, 1, var.cmbventa)
            var.ui.tabVenta.scrollToBottom()
            Conexion.cargarCmbventa(var.cmbventa)
        else:
            print("Error alta venta: ", query.lastError().text())

    def anulaVenta(codVenta):
        '''

        Módulo que anula una linea de venta de una factura

        :param: codVenta que es el código de la venta a anlar
        :return: None
        :rtype: None

        Muestra mensaje en la barra de estado

        '''
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codVenta')
        query.bindValue(':codVenta', codVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
        else:
            print("Error baja venta: ", query.lastError().text())

    def borraFac(self,codfac):
        '''

        Módulo que borra una factura y todas las ventas asociadas a esa factura

        :param: codfac o código de la factura
        :type: int
        :return: None
        :rtype: None

        En primer lugar borra la factura y luego vuelve a realizar una llamada a la base de datos para
        borrar todas aquellas ventas asociadas a esa factura.

        '''


        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(codfac))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Anulada')
            Conexion.mostrarFacturas(self)
        else:
            print("Error anular factura en borrafac: ", query.lastError().text())

        query1 = QtSql.QSqlQuery()
        query1.prepare('delete from ventas where codfacventa = :codfac')
        query1.bindValue(':codfac', int(codfac))
        if query1.exec_():
            var.ui.lblstatus.setText('Factura Anulada')
        else:
            print("Error anular factura en borrafac: ", query.lastError().text())
        var.ui.lblSubtotal.setText('0.00')
        var.ui.lblIva.setText('0.00')
        var.ui.lblTotal.setText('0.00')

    def listadoVentasfac(self, codfac):
        """

        Módulo que lista las ventas contenidaa en una factura

        :param codfac: valor factura a la que se incluirán las líneas de venta
        :type codfac: int
        :return: None
        :rtype: None

        Recibe el código de la factura para seleccionar los datos de las ventas cargadas a esta.
        De la BB.DD toma el nombre del producto y su precio para cada línea de venta. El precio lo multiplica
        por las unidades y se obtiene el subtotal de cada línea. Después en cada línea de la tabla irá
        el código de la venta, el nombre del producto, las unidades y el subtotal.
        Finalmente, va sumando el subfact, que es la suma de todas las ventas de esa factura, le aplica el IVA y
        el importe total de la factura. Los tres valores, subfact, iva y fac los muestra en los label asignados.

        En excepciones se recoge cualquier error que se produzca en la ejecución del módulo.

        """
        try:
            var.ui.tabVenta.clearContents()
            var.subfac = 0.00
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad, precio from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))
            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    precio = query.value(3)
                    var.ui.tabVenta.setRowCount(index + 1)
                    var.ui.tabVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select producto from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            var.ui.tabVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tabVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tabVenta.setItem(index, 3, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(precio)) + ' €'))
                            var.ui.tabVenta.setItem(index, 4, QtWidgets.QTableWidgetItem("{0:.2f}".format(float(subtotal))+ ' €'))
                            var.ui.tabVenta.item(index,0).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVenta.item(index, 2).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVenta.item(index, 3).setTextAlignment(QtCore.Qt.AlignCenter)
                            var.ui.tabVenta.item(index, 4).setTextAlignment(QtCore.Qt.AlignRight)

                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)
                #ventas.Ven tas.prepararTablaventas(index)
            if int(index) > 0:
                ventas.Ventas.prepararTablaventas(index)
            else:
                print(index)
                var.ui.tabVenta.setRowCount(0)
                ventas.Ventas.prepararTablaventas(0)
            var.ui.lblSubtotal.setText("{0:.2f}".format(float(var.subfac)))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblIva.setText("{0:.2f}".format(float(var.iva)))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblTotal.setText("{0:.2f}".format(float(var.fac)))

        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))


# class Conexion():
#     HOST = 'localhost'
#     PORT = '27017'
#     URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'#     var.DATABASE = 'empresa'
#     try:
#         var.client = pymongo.MongoClient(URI_CONNECTION)
#         var.client.server_info()
#         print('Conexión realizada al servidor %s'  %HOST)
#     except:
#         print('Error conexion')
