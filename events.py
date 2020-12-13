import sys, var, clients
from datetime import datetime
import zipfile, os
class Eventos():


    def Salir(event):
        '''
        Módulo para cerrar el programa
        :return:
        '''
        try:
            #var.lblMensalir.setText('Desea Salir de Xestión')
            var.dlgsalir.show()
            if var.dlgsalir.exec_():
                #print(event)
                sys.exit()
            else:
                var.dlgsalir.hide()
                #event.ignore()

        except Exception as error:
            print('Error %s' % str(error))

    def closeSalir(event):
        try:
            if var.dlgsalir.exec_():
                var.dlgsalir.hide()
               #necesario para que ignore X de la ventana
        except Exception as error:
            print('Error %s' % str(error))

    def cargarProv(self):
        """
        carga las provincias al iniciar el programa
        :return:
        """
        try:
            prov = ['','A Coruña', 'Lugo', 'Ourense', 'Pontevedra', 'Vigo']
            for i in prov:
                var.ui.cmbProv.addItem(i)

        except Exception as error:
            print('Error: %s' % str(error))

    def Backup(self):
        try:
            fecha = datetime.now()
            fichzip = zipfile.ZipFile('_backup.zip','w')
            fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
        except Exception as error:
            print('Error: %s' % str(error))

    def AbrirDir(self):
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s ' % str(error))

    def AbrirPrinter(self):
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    def AbrirAviso(men):
        try:
            var.lblMensaviso.setText(men)
            var.dlgaviso.show()
        except Exception as error:
            print('Error abrir ventana aviso: %s ' % str(error))

    def Confirmar(self):
        try:
            if var.cliente:
                clients.Clientes.bajaCliente()
                var.dlgaviso.hide()
                var.cliente = False
                print(var.cliente)
        except Exception as error:
            print('Error botón confirma: %s ' % str(error))

    def Anular(self):
        try:
            var.dlgaviso.hide()
        except Exception as error:
            print('Error botón anula: %s ' % str(error))

    def mostrarAvisocli(self):
        try:
            var.cliente = True
            var.lblMensaviso.setText('¿Desea eliminar el cliente?')
            var.dlgaviso.show()
        except Exception as error:
            print('Error mostrar aviso: %s ' % str(error))