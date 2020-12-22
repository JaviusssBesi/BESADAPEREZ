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
