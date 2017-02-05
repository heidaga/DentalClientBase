"""
# Client Databse app for managing contacts and dental acts
"""
# *** general
import sys
import os
import subprocess
import time
import cPickle as pickle

# *** qt specific
from PySide import QtGui, QtCore, QtWebKit
from PySide.QtGui import QColor
from PySide.QtGui import QMessageBox
# from matplotlib import rc
# rc('backend', qt4="PySide")

# pyside-uic compiled files resulting from *.ui files
import ui_windowmain
import ui_windowsettings
from ui_dialogNewDoctor import Ui_Form

from DentalClientBaseStructs import *
from DentalClientBaseToolkit import *
from DentalClientBaseSettings import *
from DentalClientBaseInvoice import *


"""
# TODOs

* initialise database from settings, then copy it to temporary folder
on leaving application, confirm if user wants to save work, if yes copy from temporary folder
this modified database ... ??
"""


 ### ***********  OPTIONS  ***********
verbose = False 
# =======================================================================


class GeneralSettings(QtGui.QMainWindow):
    """ Openv window containing all the acts for a given client """
    def __init__(self, parent=None):
    	super(GeneralSettings, self).__init__(parent)

    	self.ui = ui_windowsettings.Ui_AppCentralWidget()
    	self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(APP_LOGO_PNG_PATH))
        self.setWindowTitle("General Settings")
        
        # Background Color hotfix for central UI widget 
        # (coz not responding to stylesheet in UI)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(225,225,255))
        self.setPalette(p)

        # Increase the priority for the UI thread to ensure responsiveness
        # QtCore.QThread.currentThread().Priority(QtCore.QThread.HighPriority)
       
        # SLOTS
        self.ui.PB_Close.clicked.connect(self.OnClose)
        self.ui.PB_ActAdd.clicked.connect(self.OnAddAct)
        self.ui.PB_ActRemove.clicked.connect(self.OnRemoveAct)
        self.ui.PB_LoadDatabaseDefaultActs.clicked.connect(self.OnDatabaseLoad)
        self.ui.PB_LoadDatabaseDoctors.clicked.connect(self.OnDatabaseLoad)
        self.ui.m_tabledefaultacts.cellChanged.connect(self.OnDefaultsChange)

        # Initialize settings GUI
        self.ui.mLE_DatabaseDefaultActs.setText("")
        self.ui.mLE_DatabaseDoctorsActs.setText("")
        self.ui.m_tabledefaultacts.setEnabled(0)
        
        # Initialize member variables
        self.DoctorsActsDatabasePath = "res/database_clients_2017.dat"
        self.ClientDatabase = DentalDatabase()

        self.DefaultActsDatabasePath = "res/database_defaultprices.dat"
        self.DefaultActs = dict()
        self.LastInvoiceNo = -1

        self.InitSettings()

        self.MySignal = PriceChangeClass()

    # ********************************************************************************
    def WriteSettings(self):
        with open(APP_SETTINGS, 'w') as fo:
            fo.write("Database_DoctorsActs = {0}\n".format(self.DoctorsActsDatabasePath))
            fo.write("Database_DefaultActs = {0}\n".format(self.DefaultActsDatabasePath))
            fo.write("LastInvoiceNo = {0}\n".format(self.LastInvoiceNo))

    def InitSettings(self):

        # Boolean to check wether settings need to be saved again
        self.bUpToDate = False

        bFoundSettings = False
        if os.path.isfile(APP_SETTINGS):
            # print "os.path.isfile(APP_SETTINGS) is true so read mode"
            bFoundSettings = True
            with open(APP_SETTINGS, 'r') as fo:
                while True:
                    line = fo.readline()
                    if not line: break
                    splitLine = line.strip().split("=")
                    sSettingKey = splitLine[0].strip()
                    sSettingVal = splitLine[1].strip()
                    # if verbose: print ">>> database", splitLine
                    
                    if sSettingKey == "Database_DefaultActs":
                        self.DefaultActsDatabasePath = sSettingVal 
                    
                    elif sSettingKey == "Database_DoctorsActs":    
                        self.DoctorsActsDatabasePath = sSettingVal
                    
                    elif sSettingKey == "LastInvoiceNo":
                        self.LastInvoiceNo = int(sSettingVal)
                        if self.LastInvoiceNo < 0: self.LastInvoiceNo = 0 
        else:
            self.WriteSettings()

        # Load default acts
        bFoundDatabasePrices = False
        if os.path.isfile(self.DefaultActsDatabasePath):
            bFoundDatabasePrices = True
            DefaultActs = pkl_load(self.DefaultActsDatabasePath)
            if(DefaultActs == None): return
            self.DefaultActs = DefaultActs
        
        # Load dental database (acts, name, prices, ...)
        bFoundDatabaseDoctors = False
        if os.path.isfile(self.DoctorsActsDatabasePath):
            bFoundDatabaseDoctors = True
            Doctors_and_Acts = pkl_load(self.DoctorsActsDatabasePath)
            if(Doctors_and_Acts == None): return
            self.ClientDatabase = Doctors_and_Acts
        
        
        if bFoundSettings and bFoundDatabasePrices: 
            self.bUpToDate = True
        
        self.ui.mLE_DatabaseDefaultActs.setText(self.DefaultActsDatabasePath)
        self.ui.mLE_DatabaseDoctorsActs.setText(self.DoctorsActsDatabasePath)
        
        self.ui.m_tabledefaultacts.setEnabled(1)
        if bFoundDatabasePrices:
            toolkit_populate_table_from_dict(self.ui.m_tabledefaultacts, self.DefaultActs)
        else:
            self.ui.m_tabledefaultacts.setRowCount(0)

        return 0

    ###### Member functions related to Qt
    def OnDatabaseLoad(self):
        if(self.sender() == self.ui.PB_LoadDatabaseDefaultActs):
            sMsg = "Are you sure you want to change the default acts-prices database ?"
            reply = toolkit_ShowWarningMessage2(sMsg)
            if reply != QMessageBox.Ok: return 0

        if(self.sender() == self.ui.PB_LoadDatabaseDoctors):
            sMsg = "Are you sure you want to change the doctors database ?"
            reply = toolkit_ShowWarningMessage2(sMsg)
            if reply != QMessageBox.Ok: return 0

        # Get user-chosen file name
        filename = None
        filters = ["Dental Database files (*.dat *.pkl)", "Any files (*)"]
        dialog = QtGui.QFileDialog(self, "Open Dental Database", directory = APP_DIR)
        dialog.setNameFilters(filters)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
        if filename == None: return 0
        
        # Load new databases
        if(self.sender() == self.ui.PB_LoadDatabaseDefaultActs):
            self.DefaultActsDatabasePath = filename
            self.ui.mLE_DatabaseDefaultActs.setText(self.DefaultActsDatabasePath)
            DefaultActs = pkl_load(filename) # returns a dict object
            if(DefaultActs == None): return
            self.DefaultActs = DefaultActs
            sMsg = "The default acts-prices database has been modified. You should restart the application before changes take effect."
            toolkit_ShowWarningMessage(sMsg)
   
        if(self.sender() == self.ui.PB_LoadDatabaseDoctors):
            self.DoctorsActsDatabasePath = filename
            self.ui.mLE_DatabaseDoctorsActs.setText(self.DoctorsActsDatabasePath)
            Doctors_and_Acts = pkl_load(filename) # returns a dict object
            if(Doctors_and_Acts == None): return
            if type(Doctors_and_Acts) != TYPE_DENTAL_DATABASE:
                toolkit_ShowCriticalMessage("The loaded doctors database contains invalid data. Please load a valid database file.")
                return 0
            self.ClientDatabase = Doctors_and_Acts
            sMsg = "The doctors database has been modified. You should restart the application before changes take effect."
            toolkit_ShowWarningMessage(sMsg)

        with open(APP_SETTINGS, 'w') as fo:
            fo.write("Database_DoctorsActs = {0}\n".format(self.DoctorsActsDatabasePath))
            fo.write("Database_DefaultActs = {0}\n".format(self.DefaultActsDatabasePath))
            fo.write("LastInvoiceNo = {0}\n".format(self.LastInvoiceNo))

        toolkit_populate_table_from_dict(self.ui.m_tabledefaultacts, self.DefaultActs)
        self.bUpToDate = False

        return 0

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.OnClose()

    def GetLastInvoiceNo(self):
        return self.LastInvoiceNo

    def SetLastInvoiceNo(self, iVal):
        self.LastInvoiceNo = iVal
        return 0

    def OnClose(self):
        if self.bUpToDate:
            self.close()
        else:
            bStatus = self.CheckValidity()
            if bStatus:
                self.ParseUserActsFromTable()
                pkl_save(self.DefaultActs, self.DefaultActsDatabasePath)
                self.bUpToDate = True
                self.close()
            else:
                sMsg = "The default acts/price table contains empty or negative cells."
                sMsg += " Please check again before quitting settings."
                toolkit_ShowWarningMessage(sMsg)
        return 0

    def OnAddAct(self):
        table = self.ui.m_tabledefaultacts
        iRowCount = table.rowCount()
        table.setRowCount(iRowCount+1)
        # iRow = table.currentRow()
        self.bUpToDate = False
        return 0 

    def OnRemoveAct(self):
        table = self.ui.m_tabledefaultacts
        iRow = table.rowCount()
        table.setRowCount(iRow-1)
        self.bUpToDate = False
        return 0 

    def OnDefaultsChange(self, iRow, iCol):
        table = self.ui.m_tabledefaultacts
        toolkit_format_existing_cell(table, iRow, iCol)
        self.bUpToDate = False
        return 0

    # return a copy dict
    def GetDefaultActs(self):
        return dict(self.DefaultActs)

    # return a copy list
    def GetDoctorsActs(self):
        return self.ClientDatabase

    def CheckValidity(self):
        table = self.ui.m_tabledefaultacts
        if (table.rowCount() == 0): return True
        for iRow in xrange(table.rowCount()):
            qItemName = table.item(iRow, 0)
            if qItemName is None: return False
            qItemPrice = table.item(iRow, 1)
            if qItemPrice is None: return False
            if qItemName.text() == "": return False
            if qItemPrice.text() == "": return False
            fPrice = float(qItemPrice.text())
            if fPrice <= 0.0 : return False
        return True

    def ParseUserActsFromTable(self):
        table = self.ui.m_tabledefaultacts
        self.DefaultActs = dict()
        for iRow in xrange(table.rowCount()):
            sName = table.item(iRow, 0).text()
            sPrice = table.item(iRow, 1).text()
            self.DefaultActs[sName.upper()] = float(sPrice)

        self.MySignal.PricesChanged.emit()
        
        return 0

    def GetPath_DoctorActsDatabase(self):
        return str(self.DoctorsActsDatabasePath)

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************
# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalClientBaseGUI(QtGui.QMainWindow):
    """ Main window for all clients, allowing to add clients and manage existing clients """

    def __init__(self, parent=None):
    	super(DentalClientBaseGUI, self).__init__(parent)

    	self.ui = ui_windowmain.Ui_AppCentralWidget()
    	self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(APP_LOGO_PNG_PATH))
        self.setWindowTitle(APP_NAME+" "+APP_LICENSE)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.ui.banner.setIcon(QtGui.QIcon(APP_BANNER_PATH))
        
        # Background Color hotfix for central UI widget 
        # (coz not responding to stylesheet in UI)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255,255,255))
        self.setPalette(p)

        sFont = APP_SETTINGS_FONT
        iFontSize = APP_SETTINGS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(font)

        # Increase the priority for the UI thread to ensure responsiveness
        QtCore.QThread.currentThread().Priority(QtCore.QThread.HighPriority)
        
        # Enable/Disable options
        self.ui.PB_AddDoctor.setEnabled(1)
        self.ui.PB_RemoveDoctor.setEnabled(1)

        # CLASS INSTANCES
        self.AppSettings = GeneralSettings(self)
        self.NewDoctorDialog = QNewDoctorDialog(self)

        date = time.strftime("%d/%m/%Y")
        stime = time.strftime("%H:%M")
        self.ui.LE_date.setText(date)
        self.ui.LE_time.setText(stime)


        # ONLY FOR DEBUG *********************************
        # list_doctors = []
        # self.DefaultActsDict = self.AppSettings.GetDefaultActs()
        self.ParsedDentalDatabase = self.AppSettings.GetDoctorsActs()
        # if type(self.ParsedDentalDatabase) == TYPE_DENTAL_DATABASE:
        #     if(self.ParsedDentalDatabase.GetNbDoctors() > 0):
        #         list_doctors = self.ParsedDentalDatabase.GetListDoctors()

        # DECLARE MODELS *********************************
        self.TableModelDoctors = DoctorTableModel(self)
        self.TableModelActs = ActTableModel(self)
        self.TableModelPayments = PaymentTableModel(self)

        # CONNECT MODELS WITH MAN APP (IF NECESSCARY) *******
        self.TableModelActs.dataChanged.connect(self.OnTableDataChange)
        self.TableModelPayments.dataChanged.connect(self.OnTableDataChange)

        # TABLE VIEW : DOCTORS ******************************
        table_view = self.ui.m_TableViewClients
        # table_view.setWordWrap(True)
        table_view.setModel(self.TableModelDoctors)
        table_view.setShowGrid(False)
        table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        table_view.setEditTriggers( QtGui.QAbstractItemView.SelectedClicked ) # DoubleClicked
                                    
        sFont = APP_SETTINGS_TABLE_DOCTORS_FONT
        iFontSize = APP_SETTINGS_TABLE_DOCTORS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        vv = table_view.verticalHeader()
        vv.setVisible(True)
        vv.setStretchLastSection(False)
        table_view.resizeColumnsToContents()
        # table_view.resizeRowsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        
        # TABLE VIEW : ACTS *********************************
        table_view = self.ui.m_TableViewActs
        table_view.setWordWrap(True)
        table_view.setModel(self.TableModelActs)
        table_view.setEditTriggers( QtGui.QAbstractItemView.AllEditTriggers ) # AllEditTriggers # NoEditTriggers 
        table_view.setDragDropOverwriteMode(False)
        # table_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows) # SelectItems
        # table_view.setTextElideMode(QtCore.Qt.ElideNone)
        table_view.setShowGrid(False)
        sFont = APP_SETTINGS_TABLE_ACTS_FONT
        iFontSize = APP_SETTINGS_TABLE_ACTS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        vv = table_view.verticalHeader()
        vv.setVisible(True)
        vv.setStretchLastSection(False)
        table_view.resizeColumnsToContents()
        # table_view.resizeRowsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)        
        # Set delegates
        sActTypeDict = self.AppSettings.GetDefaultActs()
        self.qDelegateAct = DentalActDelegate(table_view, sActTypeDict.keys())
        table_view.setItemDelegate(self.qDelegateAct)
 
        # TABLE VIEW : PAYMENTS *********************************
        table_view = self.ui.m_TableViewPayments
        table_view.setWordWrap(True)
        table_view.setModel(self.TableModelPayments)
        table_view.setEditTriggers( QtGui.QAbstractItemView.AllEditTriggers ) # AllEditTriggers # NoEditTriggers 
        table_view.setDragDropOverwriteMode(False)
        # table_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # table_view.setTextElideMode(QtCore.Qt.ElideNone)
        table_view.setShowGrid(False)
        sFont = APP_SETTINGS_TABLE_PAYMENTS_FONT
        iFontSize = APP_SETTINGS_TABLE_PAYMENTS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        vv = table_view.verticalHeader()
        vv.setVisible(True)
        vv.setStretchLastSection(False)
        table_view.resizeColumnsToContents()
        # table_view.resizeRowsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)        
        # Set delegates
        self.qDelegatePayment = DentalPaymentDelegate(table_view)
        table_view.setItemDelegate(self.qDelegatePayment)


        self.ui.LE_TotalActs.setText("0.0")
        self.ui.LE_TotalPayments.setText("0.0")
        self.ui.GB_InvoiceViewer.setVisible(False)
        self.ui.TabInvoiceViewer.setCurrentIndex(0)
        # self.ui.webViewMesseger.load(QtCore.QUrl('https://web.whatsapp.com/'))
        
        self.ui.m_TableWidgetPrices.setEnabled(0)
        self.ActiveClientID = None
        self.LastKnownActType = ""

        self.InitStyle()
        self.InitSlots()
        
    # ********************************************************************************

    def InitStyle(self):
        self.ui.PB_ExportInvoice.setStyleSheet("Text-align:left")
        self.ui.PB_OpenInvoiceFolder.setStyleSheet("Text-align:left")
        self.ui.PB_Calculator.setStyleSheet("Text-align:left")
        self.ui.PB_Settings.setStyleSheet("Text-align:left")
        self.ui.PB_ToggleInvoiceViewer.setStyleSheet("Text-align:left")
        self.ui.PB_Reporting.setStyleSheet("Text-align:left")
        self.ui.LE_TotalActs.setStyleSheet("color: rgb(0, 0, 240)")
        self.ui.LE_TotalPayments.setStyleSheet("color: rgb(0, 0, 240)")

        # self.InitializeHorizontalHeaderSize(self.ui.m_TableViewClients)
        self.ui.m_TableViewClients.resizeColumnsToContents()
        return 0

    def InitSlots(self):
        self.ui.PB_Reporting.clicked.connect(self.OnReporting)
        self.ui.PB_OpenInvoiceFolder.clicked.connect(self.OnOpenInvoiceFolder)
        self.ui.PB_ExportInvoice.clicked.connect(self.OnExportInvoice)
        self.ui.PB_Calculator.clicked.connect(self.OnSpawnCalculator)
        self.ui.PB_Close.clicked.connect(self.OnClose)
        self.ui.PB_Settings.clicked.connect(self.OnOpenSettings)
        self.ui.PB_AddDoctor.clicked.connect(self.OnAddDoctor)
        self.ui.PB_RemoveDoctor.clicked.connect(self.OnRemoveDoctor)
        self.ui.PB_AddAct.clicked.connect(self.OnAddAct)
        self.ui.PB_RemoveAct.clicked.connect(self.OnRemoveAct)
        self.ui.PB_AddPayment.clicked.connect(self.OnAddPayment)
        self.ui.PB_RemovePayment.clicked.connect(self.OnRemovePayment)
        self.ui.PB_ToggleInvoiceViewer.clicked.connect(self.OnShowHideInvoiceViewer)
        self.ui.m_TableViewClients.clicked.connect(self.OnActivateClient)

        self.AppSettings.MySignal.PricesChanged.connect(self.OnPricesChanged)
        self.TableModelActs.MySignal.PricesChanged.connect(self.OnPricesChanged)

        self.ShortcutDelDoctor = QtGui.QShortcut(self)
        self.ShortcutDelDoctor.setKey(QtCore.Qt.CTRL + QtCore.Qt.Key_Delete)
        self.ShortcutDelDoctor.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.ShortcutDelDoctor.activated.connect(self.OnRemoveDoctor)

        self.ShortcutAddAct = QtGui.QShortcut(self)
        self.ShortcutAddAct.setKey(QtCore.Qt.CTRL + QtCore.Qt.Key_A)
        self.ShortcutAddAct.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.ShortcutAddAct.activated.connect(self.OnAddAct)

        self.ShortcutAddAct = QtGui.QShortcut(self)
        self.ShortcutAddAct.setKey(QtCore.Qt.CTRL + QtCore.Qt.Key_D)
        self.ShortcutAddAct.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.ShortcutAddAct.activated.connect(self.OnRemoveAct)

        self.ShortcutAddAct = QtGui.QShortcut(self)
        self.ShortcutAddAct.setKey(QtCore.Qt.CTRL + QtCore.Qt.Key_P)
        self.ShortcutAddAct.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.ShortcutAddAct.activated.connect(self.OnAddPayment)

        self.ShortcutAddAct = QtGui.QShortcut(self)
        self.ShortcutAddAct.setKey(QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.ShortcutAddAct.setContext(QtCore.Qt.WidgetWithChildrenShortcut)
        self.ShortcutAddAct.activated.connect(self.OnRemovePayment)


    @QtCore.Slot()
    def OnPricesChanged(self):
       if self.ActiveClientID is not None:
        self.UpdateDoctorDetailsByID()

    def SumAndWriteActs(self):
        listDentalActs = self.ParsedDentalDatabase.GetListActsByDoctorID(self.ActiveClientID)
        fGrandTotal = 0.0
        for jAct in listDentalActs: fGrandTotal += jAct.SubTotal
        self.ui.LE_TotalActs.setText(str(fGrandTotal))
        return 0

    def SumAndWritePayments(self):
        listDentalPayments = self.ParsedDentalDatabase.GetListPaymentsByDoctorID(self.ActiveClientID)
        fPaid = 0.0
        for jPayment in listDentalPayments: fPaid += jPayment.Sum
        self.ui.LE_TotalPayments.setText(str(fPaid))
        return 0

    ###### Member functions related to Qt

    def closeEvent(self, event):
        """ I had to use the prefix GtGui.QMessage and return make it work """
        bUTD1 = self.TableModelDoctors.IsUpToDate() 
        bUTD2 = self.TableModelActs.IsUpToDate()
        bUTD3 = self.TableModelPayments.IsUpToDate()
        bExitWithoutSave = bUTD1 and bUTD2 and bUTD3
        if(bExitWithoutSave): 
            event.accept()
            return

        if BOOLSETTING_Confirm_before_exit_application:
            sMsg = "You are about to quit Dental Client Base. "
            sMsg += "Do you want to SAVE your progress or IGNORE any changes before quitting ?" 
            reply = toolkit_ShowWarningMessage3(sMsg)
            if reply == QtGui.QMessageBox.Cancel: 
                event.ignore()
                return
            if reply == QtGui.QMessageBox.Ignore: 
                event.accept()
                return

        sDatabasePath = self.AppSettings.GetPath_DoctorActsDatabase()
        pkl_save(self.ParsedDentalDatabase, sDatabasePath)
        self.AppSettings.WriteSettings() # re-write settings.ini
        event.accept()
        return

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.OnClose()
        # if event.key() == QtCore.Qt.Key_F4:
        #     self.OpenActWindow("XXX")

        # if event.key() == QtCore.Qt.Key_F10:
        # 	red alert 2 taunts !! EASTER EGG

    def OnTableDataChange(self, topleft_index, bottom_right_index):
        if self.ActiveClientID is None: return 0
        if self.sender() == self.TableModelActs: self.SumAndWriteActs()
        elif self.sender() == self.TableModelPayments: self.SumAndWritePayments()
        else: return 0

    def OnClose(self):
        """ handled by close event """
        self.close()
        return 0

    def OnOpenSettings(self):
        # avoid multiple open
        self.AppSettings.show()
        self.AppSettings.activateWindow()
        return 0

    def OnShowHideInvoiceViewer(self):
        bSwitch = self.ui.GB_InvoiceViewer.isVisible() 
        self.ui.GB_InvoiceViewer.setVisible(not bSwitch)
        return 0

    def OnSpawnCalculator(self):
        subprocess.call("calc.exe")
        return 0

    def OnReporting(self):
        self.ReportingDiag = QtGui.QDialog(self)
        reportingWidg = self.ReportingDiag        
        reportingWidg.setWindowTitle("My Form")
        layout = QtGui.QVBoxLayout(reportingWidg)
        qTextEdit = QtGui.QTextEdit("Write your message here..", reportingWidg)
        PB_Ok = QtGui.QPushButton("Send", reportingWidg)
        PB_Cancel = QtGui.QPushButton("Cancel", reportingWidg)
        PB_Ok.clicked.connect(reportingWidg.accept)
        PB_Cancel.clicked.connect(reportingWidg.reject)
        layout.addWidget(qTextEdit)
        layout.addWidget(PB_Ok)
        layout.addWidget(PB_Cancel)
        # Set dialog layout
        reportingWidg.setLayout(layout)

        if self.ReportingDiag.exec_() == QtGui.QDialog.Accepted:
            sMsg = qTextEdit.toPlainText()
            toolkit_ErrorReport(sMsg)
        return 0

    def OnOpenInvoiceFolder(self):
        filename = ""
        sOpenDir = APP_INVOICE_EXPORT_DIR
        if self.ActiveClientID is not None:
            dentalDoctor = self.ParsedDentalDatabase.GetDoctorFromID(self.ActiveClientID)
            sOpenDir = os.path.join(APP_INVOICE_EXPORT_DIR,dentalDoctor.GetExportName())
            if not QtCore.QDir(sOpenDir).exists():
                sOpenDir = APP_INVOICE_EXPORT_DIR

        filters = ["HTML Invoice (*.html)", "PDF Invoice (*.pdf)", "Dental Database Invoice (*.html *.pdf)", "Any files (*)"]
        dialog = QtGui.QFileDialog(self, "Open Exported Invoice", directory = sOpenDir)
        dialog.setNameFilters(filters)
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
        
        if dialog.exec_():
            filename = dialog.selectedFiles()[0]
        
        if filename == "":
            sMsg = "No exported invoice selected for viewing."
            toolkit_ShowWarningMessage(sMsg)
            return 0
        
        webbrowser.open_new_tab(filename)
        return 0

    def OnExportInvoice(self):
        # TODO: set self.ActiveClientID to None when TableDoctors is deselected/out of focus
        doctorID = self.ActiveClientID
        if doctorID is None:
            sMsg = "Unable to export invoice before selecting a doctor."
            sMsg += " No invoice exported."
            toolkit_ShowWarningMessage(sMsg)
            return 0

        sCurrentDate = QtCore.QDate.currentDate().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
        sCurrentMonth = sCurrentDate.split("/")[1]
        sCurrentYear = sCurrentDate.split("/")[2]
        iInvoiceID = self.AppSettings.GetLastInvoiceNo() + 1
        dentalDoctor = self.ParsedDentalDatabase.GetDoctorFromID(doctorID)
        listDentalPayments = self.ParsedDentalDatabase.GetListPaymentsByDoctorIdByDate(doctorID, sCurrentMonth, sCurrentYear)
        listDentalActs = self.ParsedDentalDatabase.GetListActsByDoctorIdByDate(doctorID, sCurrentMonth, sCurrentYear)
        if len(listDentalActs) == 0 : 
            sMsg = "No dental acts found for the current month while exporting invoice. No invoice exported."
            toolkit_ShowWarningMessage(sMsg)
            return 0
        
        # create export folder if doesnt exist
        if not QtCore.QDir(APP_INVOICE_EXPORT_DIR).exists():
            QtCore.QDir().mkdir(APP_INVOICE_EXPORT_DIR)

        # create doctor sub folder if doesnt exist
        sDoctorExportName = dentalDoctor.GetExportName()
        sExportSubFolder = os.path.join(APP_INVOICE_EXPORT_DIR, sDoctorExportName)
        if not QtCore.QDir(sExportSubFolder).exists():
            QtCore.QDir().mkdir(sExportSubFolder)
        
        sExportedInvoice , sExportedInvoicePDF = ExportInvoice( iInvoiceID, 
                                                                sCurrentMonth, sCurrentYear, 
                                                                dentalDoctor, listDentalActs, listDentalPayments)
        
        if sExportedInvoice is None:
            toolkit_ReportUndefinedBehavior("OnExportInvoice: sExportedInvoice (#{0}) is None.".format(iInvoiceID))
            return 0

        # increment invoice counter after successful export 
        if sExportedInvoice != "" :
            self.AppSettings.SetLastInvoiceNo(iInvoiceID)

            if BOOLSETTING_Preview_exported_invoice_in_internet_browser:
                webbrowser.open_new_tab(sExportedInvoice)
            
            # Preview in Invoice viewer pre requisite for PDF ? 
            if BOOLSETTING_Preview_exported_invoice_in_Invoice_Viewer:
                self.ui.TabInvoiceViewer.setCurrentIndex(1)
                self.ui.TabInvoiceViewer.setTabText(1, "Invoice {0}: {1}".format(iInvoiceID, dentalDoctor.GetFullName()))
                
                # Show in second tab 
                # TODO: for each client open a new closable tab
                # self.webViewInvoiceViewer = QtWebKit.QWebView() # spawns a separate window
                self.ui.webViewInvoiceViewer.load(QtCore.QUrl.fromLocalFile(sExportedInvoice))
                self.ui.webViewInvoiceViewer.show()

            if BOOLSETTING_Convert_exported_invoice_to_pdf_without_preview:
                # Print a PDF
                qdoc = QtGui.QTextDocument(self)
                sContentHtml = open( sExportedInvoice , 'r').read()                
                qdoc.setHtml( sContentHtml.replace(" ", "") ) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                printer = QtGui.QPrinter() #QtGui.QPrinter(QtGui.QPrinter.HighResolution)
                printer.setOutputFileName(sExportedInvoicePDF)
                printer.setOutputFormat(QtGui.QPrinter.PdfFormat) # QPrinter.NativeFormat
                printer.setPageSize(QtGui.QPrinter.A4)
                # printer.setOrientation(QtGui.QPrinter.Portrait)    # QtGui.QPrinter.Portrait    
                # printer.setFullPage(True)
                qdoc.print_(printer)
                # printer.newPage()
                # printer.setColorMode(QtGui.QPrinter.Color) # QtGui.QPrinter.GrayScale
                # dlg = QtGui.QPrintDialog(printer, None)
                # if dlg.exec_() != QtGui.QDialog.Accepted:
                #     return
                self.ui.webViewInvoiceViewer.print_(printer)

        return 0

    def isDoctorSelected(self):
        return (self.ActiveClientID is not None)

    # **********  TABLE ACTS EVENTS ***********************

    def OnAddAct(self):
        if not self.isDoctorSelected():
            toolkit_ShowWarningMessage("Unable to complete operation: please select doctor first.")
        sCurrentDate = QtCore.QDate.currentDate().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
        newDentalAct = DentalAct(sCurrentDate, "", self.LastKnownActType, 1) # remaining kept default
        self.TableModelActs.addDentalAct(self.ActiveClientID, newDentalAct)
        return 0
        
    def OnRemoveAct(self):
        if not self.isDoctorSelected():
            toolkit_ShowWarningMessage("Unable to complete operation: please select doctor first.")
        table_view = self.ui.m_TableViewActs
        selectModel = table_view.selectionModel()
        selectedIndexes = selectModel.selectedIndexes()
        if len(selectedIndexes) == 0: return 0
        qIndex = selectedIndexes[0]
        if not qIndex.isValid(): return 0
        iRowToDel = selectedIndexes[0].row()
        if self.sender() == self.ui.PB_RemoveAct:
            if BOOLSETTING_Confirm_before_delete_act_via_remove_button:
                reply = toolkit_ShowDeleteMessage("Are you sure you want to\ndelete the selected ACT ?")
                if reply != QMessageBox.Ok: return 0
        self.TableModelActs.removeDentalAct(self.ActiveClientID, iRowToDel)
        return 0 

    # **********  TABLE PAYMENTS EVENTS ***********************

    def OnAddPayment(self):
        if not self.isDoctorSelected():
            toolkit_ShowWarningMessage("Unable to complete operation: please select doctor first.")
        sCurrentDate = QtCore.QDate.currentDate().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
        newDentalPayment = DentalPayment(sCurrentDate)
        self.TableModelPayments.addDentalPayment(self.ActiveClientID, newDentalPayment)
        return 0
        
    def OnRemovePayment(self):
        if not self.isDoctorSelected():
            toolkit_ShowWarningMessage("Unable to complete operation: please select doctor first.")
        table_view = self.ui.m_TableViewPayments
        selectModel = table_view.selectionModel()
        selectedIndexes = selectModel.selectedIndexes()
        if len(selectedIndexes) == 0: return 0
        qIndex = selectedIndexes[0]
        if not qIndex.isValid(): return 0
        iRowToDel = selectedIndexes[0].row()
        if self.sender() == self.ui.PB_RemovePayment:
            if BOOLSETTING_Confirm_before_delete_payment_via_remove_button:
                reply = toolkit_ShowDeleteMessage("Are you sure you want to\ndelete the selected PAYMENT ?")
                if reply != QMessageBox.Ok: return 0 
        self.TableModelPayments.removeDentalPayment(self.ActiveClientID, iRowToDel)
        return 0 

    # **********  TABLE CLIENTS EVENTS ***********************

    def OnAddDoctor(self):
        qDialog = self.NewDoctorDialog
        qDialog.cleanLineEdits()
        if qDialog.exec_() == QtGui.QDialog.Accepted:
            newDentalClient = qDialog.getNewDoctor()
            if newDentalClient is None:
                sMsg = "OnAddDoctor: newDentalClient is None."
                sMsg += "I couldn't create a DentalClient from the params given by the opened dialog" 
                toolkit_ReportUndefinedBehavior(sMsg)
                return 0
            dictActsPricesFromSettings = self.AppSettings.GetDefaultActs()
            newDentalClient.SetDoctorPrices(dictActsPricesFromSettings)
            self.TableModelDoctors.AddDoctorToDatabase(newDentalClient)      
        return 0 

    def OnRemoveDoctor(self):
        if self.sender() == self.ui.PB_RemoveDoctor:
            if BOOLSETTING_Confirm_before_delete_doctor_via_remove_button:
                sMsg = "Are you sure to delete a doctor entry and all related dental acts ?"
                ret = toolkit_ShowDeleteMessage(sMsg)
                if ret == QMessageBox.Cancel: return 0
        if self.ActiveClientID is None: return 0
        self.TableModelDoctors.RemoveDoctorFromDatabase(self.ActiveClientID)
        return 0 

    def OnActivateClient(self, qIndex):
        """ Visualise/edit database of acts for the selected doctor
            Used with a "doubleClicked" signal fired from QTableView
        """
        iRow = qIndex.row()
        self.ActiveClientID = self.TableModelDoctors.getHashIDFromSelectedDoctor(qIndex)
        self.UpdateDoctorDetailsByID()
        return 0

    def UpdateDoctorDetailsByID(self):
        
        # Make the acts of the clients match those in preferences
        # If not, add only the new acts with their prices
        sSettingsDefaultPricesDict = self.AppSettings.GetDefaultActs()
        sDoctorPricesDict = self.ParsedDentalDatabase.GetDoctorPricesByDoctorID(self.ActiveClientID)
        lAdded, lRemoved, lDiffs = toolkit_compare_dicts(sDoctorPricesDict, sSettingsDefaultPricesDict)
        
        # Doctor has more acts than settings, they should be removed
        for sTypeKey in lAdded: del sDoctorPricesDict[sTypeKey]
        # Doctor has less acts than settings, they should be added
        for sTypeKey in lRemoved: sDoctorPricesDict[sTypeKey] = sSettingsDefaultPricesDict[sTypeKey]

        # Cast changes to database
        self.ParsedDentalDatabase.SetDoctorPricesByDoctorID(self.ActiveClientID, sDoctorPricesDict)

        # Now doctor has all the Act Types as in settings, so we should update the delegate
        self.qDelegateAct.setActTypesStringList(sDoctorPricesDict.keys())

        # Visualise the doctor prices dict
        tableWidget = self.ui.m_TableWidgetPrices
        tableWidget.setEnabled(1)
        toolkit_populate_table_from_dict(tableWidget, sDoctorPricesDict, QtCore.Qt.ItemIsEnabled)
        
        # Refresh table AFTER doctor prices dict has been updated
        self.TableModelActs.SetModelForDoctorByID(self.ActiveClientID)
        self.TableModelPayments.SetModelForDoctorByID(self.ActiveClientID)

        if BOOLSETTING_Initialize_Columnsize_On_Client_Activation:
            self.InitializeHorizontalHeaderSize(self.ui.m_TableViewActs)
            self.InitializeHorizontalHeaderSize(self.ui.m_TableViewPayments)
        else:
            self.ui.m_TableViewActs.resizeColumnsToContents()
            self.ui.m_TableViewPayments.resizeColumnsToContents()

        # Update totals for newly selected doctor
        self.SumAndWriteActs()
        self.SumAndWritePayments()
        return 0


    def InitializeHorizontalHeaderSize(self, table_view):
        iWIDTH = table_view.width()

        if table_view is self.ui.m_TableViewClients:
            table_view.setColumnWidth(COL_DRFIRSTNAME,      iWIDTH*DOCTOR_TABLE_COLUMNSIZE_FIRSTNAME)
            table_view.setColumnWidth(COL_DRLASTNAME,       iWIDTH*DOCTOR_TABLE_COLUMNSIZE_LASTNAME)
            table_view.setColumnWidth(COL_DRPHONE,          iWIDTH*DOCTOR_TABLE_COLUMNSIZE_PHONE)

        if table_view is self.ui.m_TableViewActs:
            table_view.setColumnWidth(COL_ACTDATE,          iWIDTH*ACT_TABLE_COLUMNSIZE_DATE)
            table_view.setColumnWidth(COL_ACTTYPE,          iWIDTH*ACT_TABLE_COLUMNSIZE_TYPE)
            table_view.setColumnWidth(COL_ACTPATIENT,       iWIDTH*ACT_TABLE_COLUMNSIZE_PATIENT)
            table_view.setColumnWidth(COL_ACTNOTES,         iWIDTH*ACT_TABLE_COLUMNSIZE_NOTES)
            table_view.setColumnWidth(COL_ACTUNITPRICE,     iWIDTH*ACT_TABLE_COLUMNSIZE_UNITPRICE)
            table_view.setColumnWidth(COL_ACTQTY,           iWIDTH*ACT_TABLE_COLUMNSIZE_QTY)
            table_view.setColumnWidth(COL_ACTSUBTOTAL,      iWIDTH*ACT_TABLE_COLUMNSIZE_TOTAL)
            
        elif table_view is self.ui.m_TableViewPayments:
            table_view.setColumnWidth(COL_PAYMENTDATE,      iWIDTH*PAYMENT_TABLE_COLUMNSIZE_DATE)
            table_view.setColumnWidth(COL_PAYMENTSUM,       iWIDTH*PAYMENT_TABLE_COLUMNSIZE_SUM)

#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************


class QNewDoctorDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.PB_Ok.clicked.connect(self.accept)
        self.ui.PB_Cancel.clicked.connect(self.reject)
        self.cleanLineEdits()

    def validate(self):
        if self.ui.firstName.text() == "": return False
        if self.ui.lastName.text() == "": return False
        if self.ui.phoneNumber.text() == "": return False
        return True

    def cleanLineEdits(self):
        self.ui.firstName.setText("")
        self.ui.lastName.setText("")
        self.ui.phoneNumber.setText("")
        self.ui.address.setText("")
        self.ui.email.setText("")
    
    def getNewDoctor(self):
        """ Returns a DentalClient instance """
        fn = str(self.ui.firstName.text()).strip()
        ln = str(self.ui.lastName.text()).strip()
        pn = str(self.ui.phoneNumber.text()).strip()
        em = str(self.ui.email.text()).strip()
        ad = str(self.ui.address.text()).strip()
        return DentalClient(fn, ln, pn, em, ad)
                            
    def accept(self):
        if self.validate():
            return QtGui.QDialog.accept(self)
        else:
            toolkit_ShowCriticalMessage("Unable to add new doctor.\nPlease fill in the starred fields.")


#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************
#****************************************************************************************************


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    window = DentalClientBaseGUI()
    window.show()
    window.setStyleSheet(APP_SETTINGS_COLOR_TABLE)
    sys.exit(app.exec_())