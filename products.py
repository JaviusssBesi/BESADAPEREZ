import var, conexion

class Products():
    def limpiarPro(self):
        """

        Modulo que limpia el formulario producto

        :return: none
        :rtype: none

        """
        try:
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblCodPro.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def altaProducto(self):
        """

        Modulo que isertara los datos del producto en la tabla y BBDD

        :return: none
        :rtype: none

        """
        try:
            newpro = []
            producto = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock ]
            k = 0
            for i in producto:
                newpro.append(i.text())
            if producto:
                conexion.Conexion.altaProducto(newpro)
            else:
                print('Faltan Datos')
            Products.limpiarPro(producto)
            conexion.Conexion.cargarCmbventa(var.cmbventa)
        except Exception as error:
            print('Error cargar producto : %s ' % str(error))


    def modifPro(self):
        """

        Modulo para modificar los datos de un producto con un determinado codigo

        :return: none
        :rtype: none

        Tambien recarga la tabla productos con los nuevo valores

        """
        try:
            newdata = []
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in product:
                newdata.append(i.text())
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.modificarPro(cod, newdata)
            conexion.Conexion.mostrarProducts()
            conexion.Conexion.cargarCmbventa()

        except Exception as error:
            print('Error modificar producto: %s ' % str(error))

    def cargarProd():
        """

        Modulo que carga los datos de los productos de la fila clicada
        en sus widgets

        :return: none
        :rtype: none

        """
        try:
            fila = var.ui.tableProd.selectedItems()
            prod = [ var.ui.editArtic, var.ui.editPrec, var.ui.editStock ]
            if fila:
                fila = [dato.text() for dato in fila]
            i = 1
            cod = fila[0]
            for i, dato in enumerate(prod):
                dato.setText(fila[i])
            conexion.Conexion.cargarProd(cod)
        except Exception as error:
            print('Error cargar productos en productos: %s ' % str(error))

    def bajaProd(self):
        """

        Modul que da de baja un producto y recarga la tabla productos
        y limpia el formulario

        :return: none
        :rtype: none

        """
        try:
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.bajaPro(cod)
            Products.limpiarPro(self)
            var.dlgaviso.hide()
            conexion.Conexion.mostrarProducts()
            conexion.Conexion.cargarCmbventa()
        except Exception as error:
            print('Error ventana baja producto: %s ' % str(error))