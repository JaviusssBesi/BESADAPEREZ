import var, conexion

class Products():
    def limpiarPro(self):
        '''

        Módulo que limpia los datos del formulario producto

        :return: None
        :rtype: None
        '''
        try:
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblCodPro.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def altaProducto(self):
        '''

        Módulo que insertar los proudctos en la tabla y en la base de datos
        en las búsquedas mostrará los datos del producto
        :return: None
        :rtype: None
        '''

        #preparamos el registro
        try:
            newpro = []
            #protab = []  #será lo que carguemos en la tablas
            producto = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            k = 0
            for i in producto:
                newpro.append(i.text())  #cargamos los valores que hay en los editline
                # if k < 3:
                #     protab.append(i.text())
                #     k += 1
            if producto:
            #comprobarmos que no esté vacío lo principal
            #aquí empieza como trabajar con la TableWidget
                conexion.Conexion.altaProducto(newpro)
            else:
                print('Faltan Datos')
            #conexion.Conexion.mostrarClientes(None)
            Products.limpiarPro(producto)
            conexion.Conexion.cargarCmbventa(var.cmbventa)
        except Exception as error:
            print('Error cargar producto en alta : %s ' % str(error))


    def modifPro(self):
        """

        Módulo para modificar datos de un producto con determinado código

        :return: None
        :rtype: None

        Además recarga la tabla de productos con los valores actualizados

        """
        try:
            newdata = []
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in product:
                newdata.append(i.text())
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.modificarPro(cod, newdata)
            conexion.Conexion.mostrarProducts(self)
            conexion.Conexion.cargarCmbventa()

        except Exception as error:
            print('Error modificar producto: %s ' % str(error))

    def cargarProd():
        '''

        Módulo que carga en widgets formulario productos la fila que se clickea en la tablaPro

        :return: None
        :type: None

        '''
        try:
            fila = var.ui.tableProd.selectedItems()
            prod = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
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

        Módulo para dar de baja un producto y recarga la tabla productos y limpia el formulario productos

        :return: None
        :type: None

        """
        try:
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.bajaPro(cod)
            Products.limpiarPro(self)
            var.dlgaviso.hide()
            conexion.Conexion.mostrarProducts(self)
            conexion.Conexion.cargarCmbventa()
        except Exception as error:
            print('Error ventana baja producto: %s ' % str(error))