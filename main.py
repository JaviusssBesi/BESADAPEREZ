from PyQt5 import QtPrintSupport, QtCore
from ventana import *
from vensalir import *
from venavisos import *
from vencalendar import *
from ventabout import *
from datetime import datetime, date
import sys, var, events, clients, conexion, printer, products, ventas
import locale

# Idioma "es-ES" (código para el español de España)
locale.setlocale(locale.LC_ALL, 'es-ES')


class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana about

        '''
        super(DialogAbout, self).__init__()
        var.dlgabout = Ui_dlgAbout()
        var.dlgabout.setupUi(self)
        var.dlgabout.btnCerrar.clicked.connect(events.Eventos.CerrarAbout)


class DialogAvisos(QtWidgets.QDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana avisos

        '''
        super(DialogAvisos, self).__init__()
        var.dlgaviso = Ui_dlgAvisos()
        var.dlgaviso.setupUi(self)
        var.dlgaviso.btnAceptaviso.clicked.connect(clients.Clientes.bajaCliente)
        var.dlgaviso.btnCancelaviso.clicked.connect(events.Eventos.Anular)


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana de aviso salir

        '''
        super(DialogSalir, self).__init__()
        var.dlgsalir = Ui_dlgSalir()
        var.dlgsalir.setupUi(self)
        var.dlgsalir.btnAceptar.clicked.connect(events.Eventos.Salir)
        var.dlgsalir.btnCancelar.clicked.connect(events.Eventos.closeSalir)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana de calendario

        '''
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_dlgCalendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.Calendar.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.Calendar.clicked.connect(clients.Clientes.cargarFecha)
        var.dlgcalendar.Calendar.clicked.connect(ventas.Ventas.cargarFechafac)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana de direcotrio

        '''
        super(FileDialogAbrir, self).__init__()
        self.setWindowTitle('Archivos')
        self.setModal(True)


class PrintDialogAbrir(QtPrintSupport.QPrintDialog):
    def __init__(self):
        '''

        Clase que instancia la ventana de impresión

        '''
        super(PrintDialogAbrir, self).__init__()


class CmbVenta(QtWidgets.QComboBox):
    def __init__(self):
        '''

        Clase que instancia el combo de artículos

        '''
        super(CmbVenta, self).__init__()
        var.cmbventa = QtWidgets.QComboBox()


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        '''

        Clase main. Instancia todas las ventanas del programa.
        Genera y conecta todos los eventos de los botones, tablas y otros widgtes.
        Cuando se lanza se conecta con la BBDD
        Cuando se lanza el programa carga todos los artículos, factura y clientes de la BBDD en las
        ventanas correspondiente.

        '''
        super(Main, self).__init__()

        '''

        Instancia de ventanas auxiliares

        '''

        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.dlgsalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()
        var.dlgImprimir = PrintDialogAbrir()
        var.dlgaviso = DialogAvisos()
        var.dlgabout = DialogAbout()
        var.cmbventa = QtWidgets.QComboBox()
        events.Eventos()

        '''
        listas que contiene los valores de checkbox y radiobutton
        '''

        var.rbtsex = (var.ui.rbtFem, var.ui.rbtMasc)
        var.chkpago = (var.ui.chkEfec, var.ui.chkTar, var.ui.chkTrans)

        '''

        conexion de eventos con los objetos
        estamos conectando el código con la interfaz gráfico
        botones formulario cliente

        '''
        var.ui.btnSalir.clicked.connect(events.Eventos.Salir)
        var.ui.btnSalirpro.clicked.connect(events.Eventos.Salir)
        var.ui.menubarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.toolbarSalir.triggered.connect(events.Eventos.Salir)
        var.ui.toolbarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.toolbarAbrirDir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.toolbarPrinter.triggered.connect(events.Eventos.AbrirPrinter)
        var.ui.toolbarRestaurarBBDD.triggered.connect(events.Eventos.restaurarBD)
        var.ui.actionImportar_datos.triggered.connect(events.Eventos.importar_MercaEstadisticas)
        var.ui.editDni.editingFinished.connect(clients.Clientes.validoDni)
        # var.ui.editDni.editingFinished.connect(lambda: clients.Clientes.validoDni)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAltaCli.clicked.connect(clients.Clientes.altaCliente)
        var.ui.btnAltaPro.clicked.connect(products.Products.altaProducto)
        var.ui.btnLimpiarCli.clicked.connect(clients.Clientes.limpiarCli)
        var.ui.btnLimpiarPro.clicked.connect(products.Products.limpiarPro)
        var.ui.btnModifPro.clicked.connect(products.Products.modifPro)
        var.ui.btnBajaCli.clicked.connect(events.Eventos.mostrarAvisocli)
        var.ui.btnModifCli.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnBajaPro.clicked.connect(products.Products.bajaProd)
        var.ui.btnReloadCli.clicked.connect(clients.Clientes.reloadCli)
        var.ui.btnBuscarCli.clicked.connect(clients.Clientes.buscarCli)
        var.ui.btnFac.clicked.connect(ventas.Ventas.altaFactura)
        var.ui.btnBuscafac.clicked.connect(conexion.Conexion.mostrarFacturascli)
        var.ui.btnReloadfac.clicked.connect(conexion.Conexion.mostrarFacturas)
        var.ui.btnCalendarfac.clicked.connect(ventas.Ventas.abrirCalendar)
        var.ui.btnFacdel.clicked.connect(ventas.Ventas.borrarFactura)
        var.ui.btnAceptarventa.clicked.connect(ventas.Ventas.procesoVenta)
        var.ui.btnAnularventa.clicked.connect(ventas.Ventas.anularVenta)

        clients.Clientes.valoresSpin()

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)

        '''

        Conexión de eventos de las ventas de clientes, productos y facturas

        '''

        var.ui.cmbProv.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCli)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tableProd.clicked.connect(products.Products.cargarProd)
        var.ui.tableProd.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabFac.clicked.connect(ventas.Ventas.cargarFact)
        var.ui.tabFac.clicked.connect(ventas.Ventas.mostrarVentasfac)
        var.ui.tabFac.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tabVenta.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        events.Eventos.cargarProv(self)
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 1)
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatusdate, 2)
        var.ui.lblstatus.setStyleSheet('QLabel {color: red; font: bold;}')
        var.ui.lblstatus.setText('Bienvenido a 2º DAM')
        fecha = date.today()
        var.ui.lblstatusdate.setStyleSheet('QLabel {color: black; font: bold;}')
        var.ui.lblstatusdate.setText(fecha.strftime('%A %d de %B del %Y'))
        var.ui.actionAbout.triggered.connect(events.Eventos.abrirAbout)

        '''

        módulos de impresión

        '''
        var.ui.menubarReportCli.triggered.connect(printer.Printer.reportCli)
        var.ui.menubarReportPro.triggered.connect(printer.Printer.reportPro)
        var.ui.menubarReportFac.triggered.connect(printer.Printer.reportFact)
        var.ui.menubarFacxCli.triggered.connect(printer.Printer.facporCli)

        '''

        módulos conexion base datos

        '''

        conexion.Conexion.db_connect(var.filebd)
        # conexion.Conexion()  el del mongodb
        conexion.Conexion.mostrarClientes(self)
        conexion.Conexion.mostrarProducts(self)
        conexion.Conexion.mostrarFacturas(self)
        var.cmbventa = QtWidgets.QComboBox()
        var.ui.tabWidget.setCurrentIndex(0)

    def closeEvent(self, event):
        if event:
            events.Eventos.Salir(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
