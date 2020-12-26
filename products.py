import var, conexion

class Products():
    '''
    Eventos asociados a los artículos
    '''
    def limpiarPro(self):
        '''
        limpia los datos del formulario cliente
        :return: none
        '''
        try:
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in range(len(product)):
                product[i].setText('')
            var.ui.lblCodPro.setText('')
        except Exception as error:
            print('Error limpiar widgets: %s ' % str(error))

    def altaProducto(self):  #SE EJECUTA CON EL BOTÓN ACEPTAR
        '''
        cargará los proudctos en la tabla y en la base de datos
        en las búsquedas mostrará los datos del cliente
        :return: none
        '''
        #preparamos el registro
        try:
            newpro = []
            #protab = []  #será lo que carguemos en la tablas
            producto = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock ]
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
        except Exception as error:
            print('Error cargar producto : %s ' % str(error))


    def modifPro(self):
        """Módulos para modificar datos de un produd con determinado código

        :return: None
        """
        try:
            newdata = []
            product = [var.ui.editArtic, var.ui.editPrec, var.ui.editStock]
            for i in product:
                newdata.append(i.text())  # cargamos los valores que hay en los editline
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.modificarPro(cod, newdata)
            conexion.Conexion.mostrarProducts()

        except Exception as error:
            print('Error modificar producto: %s ' % str(error))

    def cargarProd():
        '''
        carga en widgets formulario cliente los datos
        elegidos en la tabla
        :return: none
        '''
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
            print('Error cargar clientes: %s ' % str(error))

    def bajaProd(self):
        """
        módulos para dar de baja un producto
        :return:
        """
        try:
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.bajaPro(cod)
            Products.limpiarPro(self)
            var.dlgaviso.hide()
            conexion.Conexion.mostrarProducts()
        except Exception as error:
            print('Error ventana baja producto: %s ' % str(error))