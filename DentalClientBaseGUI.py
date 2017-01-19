# VERSION=      MAJOR_VERSION . MINOR_VERSION  . IMPROVEMENT_FEATURE . BUG_CORRECTION
__version__ =  '      0       .       7       .           0         .         0      '

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
from PySide import QtGui, QtCore
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
        self.setWindowIcon(QtGui.QIcon(APP_LOGO_PATH))
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

    # ********************************************************************************

    def InitSettings(self):

        # Boolean to check wether settings need to be saved again
        self.bUpToDate = False

        bFoundSettings = False
        if os.path.isfile(APP_SETTINGS):
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
            with open(APP_SETTINGS, 'w') as fo:
                fo.write("Database_DoctorsActs = {0}\n".format(self.DoctorsActsDatabasePath))
                fo.write("Database_DefaultActs = {0}\n".format(self.DefaultActsDatabasePath))
                fo.write("LastInvoiceNo = {0}\n".format(self.LastInvoiceNo))

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
        
        # print "filename = ", filename
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
            self.close()

    # def focusOutEvent(self, event):
    #     self.setFocus(QtCore.Qt.StrongFocus)

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
        return 0 

    def OnRemoveAct(self):
        table = self.ui.m_tabledefaultacts
        iRow = table.rowCount()
        table.setRowCount(iRow-1)
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
        self.setWindowIcon(QtGui.QIcon(APP_LOGO_PATH))
        self.setWindowTitle(APP_NAME+" "+APP_LICENSE)
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

        # SLOTS
        self.ui.PB_OpenInvoiceFolder.clicked.connect(self.OnOpenInvoiceFolder)
        self.ui.PB_ExportInvoice.clicked.connect(self.OnExportInvoice)
        self.ui.PB_Calculator.clicked.connect(self.OnSpawnCalculator)
        self.ui.PB_Close.clicked.connect(self.OnClose)
        self.ui.PB_Settings.clicked.connect(self.OnOpenSettings)
        self.ui.PB_AddDoctor.clicked.connect(self.OnAddDoctor)
        self.ui.PB_RemoveDoctor.clicked.connect(self.OnRemoveDoctor)
        self.ui.PB_AddAct.clicked.connect(self.OnAddAct)
        self.ui.PB_RemoveAct.clicked.connect(self.OnRemoveAct)
        # self.ui.m_tableclients.doubleClicked.connect(self.OnActivateClient)
        self.ui.m_tableclients.clicked.connect(self.OnActivateClient)

        date = time.strftime("%d/%m/%Y")
        stime = time.strftime("%H:%M")
        self.ui.LE_date.setText(date)
        self.ui.LE_time.setText(stime)

        self.appsettings = GeneralSettings(self)
        self.NewDoctorDialog = QNewDoctorDialog(self)

        list_doctors = []
        self.DefaultActsDict = self.appsettings.GetDefaultActs()
        self.ParsedDentalDatabase = self.appsettings.GetDoctorsActs() 
        if type(self.ParsedDentalDatabase) == TYPE_DENTAL_DATABASE:
            if(self.ParsedDentalDatabase.GetNbDoctors() > 0):
                list_doctors = self.ParsedDentalDatabase.GetListDoctors()

        self.TableModelDoctors = DoctorTableModelNew(self)
        # self.TableModelDoctors = DoctorTableModel(self)
        self.TableModelActs = ActTableModelNew(self)

        # TABLE VIEW : DOCTORS
        table_view = self.ui.m_tableclients
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
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        
        # TABLE VIEW : ACTS
        table_view = self.ui.m_tableacts
        table_view.setWordWrap(True)
        table_view.setModel(self.TableModelActs)
        table_view.setEditTriggers( QtGui.QAbstractItemView.DoubleClicked ) # AllEditTriggers # NoEditTriggers 
        table_view.setDragDropOverwriteMode(False)
        table_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        # table_view.setTextElideMode(QtCore.Qt.ElideNone)
        table_view.setShowGrid(False)
        sFont = APP_SETTINGS_TABLE_ACTS_FONT
        iFontSize = APP_SETTINGS_TABLE_ACTS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)        
        # Set delegates
        qDelegateAct = DentalActDelegate(table_view, self.DefaultActsDict.keys())
        table_view.setItemDelegate(qDelegateAct)

        self.ActiveClientID = None
        self.LastKnownActType = ""

        self.InitStyle()
        
    # ********************************************************************************

    def InitStyle(self):
        self.ui.PB_ExportInvoice.setStyleSheet("Text-align:left")
        self.ui.PB_OpenInvoiceFolder.setStyleSheet("Text-align:left")
        self.ui.PB_Calculator.setStyleSheet("Text-align:left")
        self.ui.PB_Settings.setStyleSheet("Text-align:left")
        return 0

    ###### Member functions related to Qt

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        # if event.key() == QtCore.Qt.Key_F4:
        #     self.OpenActWindow("XXX")

        # if event.key() == QtCore.Qt.Key_F10:
        # 	red alert 2 taunts !! EASTER EGG

    def OnClose(self):
        bUTD1 = self.TableModelDoctors.IsUpToDate() 
        bUTD2 = self.TableModelActs.IsUpToDate()
        bExitWithoutSave = bUTD1 and bUTD2
        if(not bExitWithoutSave):
            sDatabasePath = self.appsettings.GetPath_DoctorActsDatabase()
            pkl_save(self.ParsedDentalDatabase, sDatabasePath)
        self.close()
        return 0

    def OnOpenSettings(self):
        # avoid multiple open
        self.appsettings.show()
        self.appsettings.activateWindow()
        return 0

    def OnSpawnCalculator(self):
        # os.system('calc.exe')
        subprocess.call("calc.exe")
        return 0

    def OnOpenInvoiceFolder(self):
        # print ">>> APP_INVOICE_EXPORT_DIR:" , APP_INVOICE_EXPORT_DIR
        # subprocess.Popen(r'explorer /select,"D:\LOCAL_DEV\_temp\DentalClientBase\invoice_exports\."')
        # subprocess.Popen(r'explorer /select' + APP_INVOICE_EXPORT_DIR)
        filename = ""
        filters = ["Dental Database Invoice (*.html)", "Any files (*)"]
        dialog = QtGui.QFileDialog(self, "Open Exported Invoice", directory = APP_INVOICE_EXPORT_DIR)
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
        iInvoiceID = self.appsettings.GetLastInvoiceNo() + 1
        dentalDoctor = self.ParsedDentalDatabase.GetDoctorFromID(doctorID)
        listDentalActs = self.ParsedDentalDatabase.GetListActsByDoctorIdByDate(doctorID, sCurrentMonth, sCurrentYear)
        if len(listDentalActs) == 0 : 
            sMsg = "No dental acts found for the current month while exporting invoice."
            sMsg += " No invoice exported."
            toolkit_ShowWarningMessage(sMsg)
            return 0
        
        # attempt to export an invoice
        sExportedInvoice = ExportInvoice(iInvoiceID, sCurrentMonth, sCurrentYear, dentalDoctor, listDentalActs)
        
        if sExportedInvoice is None:
            toolkit_ReportUndefinedBehavior()
            return 0

        # increment invoice counter after successful export 
        if sExportedInvoice != "" :
            self.appsettings.SetLastInvoiceNo(iInvoiceID)
            webbrowser.open_new_tab(sExportedInvoice)
        return 0

    # **********  TABLE ACTS EVENTS ***********************

    def OnAddAct(self):
        sCurrentDate = QtCore.QDate.currentDate().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
        newDentalAct = DentalAct(sCurrentDate, "", self.LastKnownActType) # remaining kept default
        self.TableModelActs.addDentalAct(self.ActiveClientID, newDentalAct)
        return 0
        
    def OnRemoveAct(self):
        table_view = self.ui.m_tableacts
        selectModel = table_view.selectionModel()
        selectedIndexes = selectModel.selectedIndexes()
        qIndex = selectedIndexes[0]
        if not qIndex.isValid(): return 0
        iRowToDel = selectedIndexes[0].row()
        self.TableModelActs.removeDentalAct(self.ActiveClientID, iRowToDel)
        return 0 

    # **********  TABLE CLIENTS EVENTS ***********************

    def OnAddDoctor(self):
        qDialog = self.NewDoctorDialog
        qDialog.cleanLineEdits()
        # qDialog.show()
        # qDialog.activateWindow()
        if qDialog.exec_() == QtGui.QDialog.Accepted:
            newDentalClient = qDialog.getNewDoctor()
            # self.ParsedDentalDatabase.AddDoctorByInstance(newDentalClient)
            self.TableModelDoctors.AddDoctorToDatabase(newDentalClient)      
        return 0 

    def OnRemoveDoctor(self):
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
        table_view = self.ui.m_tableacts
        table_model_doctors = self.TableModelDoctors
        table_model_acts = self.TableModelActs
        iRow = qIndex.row()
        self.ActiveClientID = table_model_doctors.getHashIDFromSelectedDoctor(qIndex)
        table_model_acts.SetModelForDoctorByID(self.ActiveClientID)
        table_view.setModel(table_model_acts)
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        hh = table_view.horizontalHeader()
        
        table_view.setColumnWidth(COL_ACTDATE,          ACT_TABLE_COLUMNSIZE_DATE)
        table_view.setColumnWidth(COL_ACTTYPE,          ACT_TABLE_COLUMNSIZE_TYPE)
        table_view.setColumnWidth(COL_ACTPATIENT,       ACT_TABLE_COLUMNSIZE_PATIENT)
        table_view.setColumnWidth(COL_ACTNOTES,         ACT_TABLE_COLUMNSIZE_NOTES)
        table_view.setColumnWidth(COL_ACTUNITPRICE,     ACT_TABLE_COLUMNSIZE_UNITPRICE)
        table_view.setColumnWidth(COL_ACTQTY,           ACT_TABLE_COLUMNSIZE_QTY)
        table_view.setColumnWidth(COL_ACTSUBTOTAL,      ACT_TABLE_COLUMNSIZE_TOTAL)
        # hh.setStretchLastSection(True)
        return 0


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
        return DentalClient(self.ui.firstName.text(),
                            self.ui.lastName.text(),
                            self.ui.phoneNumber.text(),
                            self.ui.email.text(),
                            self.ui.address.text())

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