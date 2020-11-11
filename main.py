from ventana import *
from vensalir import *
from vencalendar import *
from datetime import datetime
import sys, var, events, clients, conexion

class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.dlgsalir = Ui_dlgSalir()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.Salir)
        #var.dlgsalir.btnBoxSalir.button(QtWidgets.QDialogButtonBox.No).clicked.connect(events.Eventos.closeSalir)
        #no es neceasario no quiero que haga nada

class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual,mesactual,diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()

        '''
        colección de datos
        '''
        var.rbtsex = (var.ui.rbtFem, var.ui.rbtMasc)
        var.chkpago = (var.ui.chkEfec, var.ui.chkTar, var.ui.chkTrans)

        '''
        conexion de eventos con los objetos
        estamos conectando el código con la interfaz gráfico
        '''

        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.actionSalir.triggered.connect(events.Eventos.Salir)
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAceptar.clicked.connect(clients.Clientes.showClientes)
        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
             i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        '''
        Llamada a módulos iniciales
        '''
        events.Eventos.cargarProv()

        '''
        módulos del principal
        '''
        conexion.Conexion.db_connect(var.filebd)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())