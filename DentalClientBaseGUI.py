"""
# Client Databse app for managing contacts and dental acts
"""
# *** general
import sys
import os

# *** qt specific
from PySide import QtGui, QtCore
from PySide.QtGui import QColor
from PySide.QtGui import QMessageBox
# from matplotlib import rc
# rc('backend', qt4="PySide")

# pyside-uic compiled files resulting from *.ui files
import ui_windowmain
import ui_windowsettings
from DentalClientBaseStructs import *
from DentalClientBaseToolkit import *
from DentalClientBaseSettings import *

import time
import numpy as np
import cPickle as pickle


 ### ***********  OPTIONS  ***********
verbose     = False
# =======================================================================

class GeneralSettings(QtGui.QMainWindow):
    """ Open Qt window containing all the acts for a given client """

    def __init__(self, parent=None):
    	super(GeneralSettings, self).__init__(parent)

    	self.ui = ui_windowsettings.Ui_AppCentralWidget()
    	self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('res/logo.ico'))
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
                    db = line.strip().split("=")
                    print db
                    if db[0].strip() == "Database_DefaultActs":
                        self.DefaultActsDatabasePath = db[1].strip() 
                    elif db[0].strip() == "Database_DoctorsActs":    
                        self.DoctorsActsDatabasePath = db[1].strip()
        else:
            with open(APP_SETTINGS, 'w') as fo:
                fo.write("Database_DoctorsActs = {0}\n".format(self.DoctorsActsDatabasePath))
                fo.write("Database_DefaultActs = {0}\n".format(self.DefaultActsDatabasePath))

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
        
        print "filename = ", filename
        if(self.sender() == self.ui.PB_LoadDatabaseDefaultActs):
            self.DefaultActsDatabasePath = filename
            self.ui.mLE_DatabaseDefaultActs.setText(self.DefaultActsDatabasePath)
            DefaultActs = pkl_load(filename) # returns a dict object
            if(DefaultActs == None): return
            self.DefaultActs = DefaultActs
   
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

        toolkit_populate_table_from_dict(self.ui.m_tabledefaultacts, self.DefaultActs)
        self.bUpToDate = False

        return 0

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

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
            self.DefaultActs[sName] = float(sPrice)
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
        self.setWindowIcon(QtGui.QIcon('res/logo.ico'))
        self.setWindowTitle(APP_NAME+" "+APP_LICENSE)
        
        # Background Color hotfix for central UI widget 
        # (coz not responding to stylesheet in UI)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(255,255,255))
        self.setPalette(p)

        # Increase the priority for the UI thread to ensure responsiveness
        QtCore.QThread.currentThread().Priority(QtCore.QThread.HighPriority)
       
        # Enable/Disable options
        self.ui.PB_AddDoctor.setEnabled(1)
        self.ui.PB_RemoveDoctor.setEnabled(1)

        # SLOTS
        self.ui.PB_Close.clicked.connect(self.OnClose)
        self.ui.PB_Settings.clicked.connect(self.OnOpenSettings)
        self.ui.PB_AddDoctor.clicked.connect(self.OnAddDoctor)
        self.ui.PB_RemoveDoctor.clicked.connect(self.OnRemoveDoctor)
        self.ui.PB_AddAct.clicked.connect(self.OnAddAct)
        self.ui.PB_RemoveAct.clicked.connect(self.OnRemoveAct)
        self.ui.m_tableclients.doubleClicked.connect(self.OnDoubleClickClient)

        date = time.strftime("%d/%m/%Y")
        stime = time.strftime("%H:%M")
        self.ui.LE_date.setText(date)
        self.ui.LE_time.setText(stime)

        self.winsettings = GeneralSettings(self)

        list_doctors = []
        list_acts_first_doctor = []
        self.ParsedDentalDatabase = self.winsettings.GetDoctorsActs() 
        if type(self.ParsedDentalDatabase) == TYPE_DENTAL_DATABASE:
            if(self.ParsedDentalDatabase.GetNbDoctors() > 0):
                list_doctors = self.ParsedDentalDatabase.GetListDoctors()
                first_doctor = list_doctors[0]
                list_acts_first_doctor = self.ParsedDentalDatabase.GetListActsByDoctorID(first_doctor.id())

        self.TableModelDoctors = DoctorTableModel(self, list_doctors)
        # self.TableModelActs = ActTableModel(self, [])
        self.TableModelActs = ActTableModelNew(self, self.ParsedDentalDatabase)

        # TABLE VIEW : DOCTORS
        table_view = self.ui.m_tableclients
        table_view.setModel(self.TableModelDoctors)
        table_view.setShowGrid(False)
        table_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # table_view.setEditTriggers( QtGui.QAbstractItemView.DoubleClicked
        #                           | QtGui.QAbstractItemView.SelectedClicked)

        sFont = APP_SETTINGS_TABLE_DOCTORS_FONT
        iFontSize = APP_SETTINGS_TABLE_DOCTORS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        # enable sorting
        table_view.setSortingEnabled(True)
        
        # TABLE VIEW : ACTS
        table_view = self.ui.m_tableacts
        table_view.setModel(self.TableModelActs)
        table_view.setShowGrid(False)
        sFont = APP_SETTINGS_TABLE_ACTS_FONT
        iFontSize = APP_SETTINGS_TABLE_ACTS_FONTSIZE
        font = QtGui.QFont(sFont, iFontSize) #, QtGui.QFont.Bold
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        hh = table_view.horizontalHeader()
        hh.setStretchLastSection(True)
        # enable sorting
        table_view.setSortingEnabled(True)
        qSpinBoxDeleg = SpinBoxDelegate()
        table_view.setItemDelegate(qSpinBoxDeleg)
        # table_view.setItemDelegateForColumn(3, qSpinBoxDeleg)
# 
    # ********************************************************************************

    ###### Member functions related to Qt

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        if event.key() == QtCore.Qt.Key_F4:
            self.OpenActWindow("XXX")

        # if event.key() == QtCore.Qt.Key_F10:
        # 	red alert 2 taunts !! EASTER EGG

    def OnClose(self):
        if(not self.TableModelActs.IsUpToDate()):
            sDatabasePath = self.winsettings.GetPath_DoctorActsDatabase()
            pkl_save(self.ParsedDentalDatabase, sDatabasePath)
        self.close()
        return 0

    def OpenActWindow(self, client):
    	win = ClientActsGUI(self)
    	win.show()
    	return 0

    def OnOpenSettings(self):
        # avoid multiple open
        if(not self.winsettings.isVisible()):
            self.winsettings.show()
            # disables also all child windows including settings windows 
            # self.setEnabled(0)
        return 0

    # **********  TABLE ACTS EVENTS ***********************

    def OnTableComboChangeValue(self, iNumber):
        table = self.ui.m_tableacts
        # http://stackoverflow.com/questions/1332110/selecting-qcombobox-in-qtablewidget
        iRow = self.sender().property("row")
        qItemUnitPrice = table.item(iRow, COL_ACTUNITPRICE) 
        if(qItemUnitPrice is None):
            qItemUnitPrice = QtGui.QTableWidgetItem()
            table.setItem(iRow, COL_ACTUNITPRICE, qItemUnitPrice)
        
        qComboActs = table.cellWidget(iRow, COL_ACTTYPE)
        sActType = qComboActs.currentText()
        DefaultActsDict = self.winsettings.GetDefaultActs() # returns act names vs price
        sUnitPrice = str(DefaultActsDict[sActType])
        qItemUnitPrice.setText(sUnitPrice)

    def OnAddAct__DEPRECATED(self):
        table = self.ui.m_tableacts
        iNbRow = table.rowCount()
        table.setRowCount(iNbRow+1)
        iRow = table.currentRow()
        
        # Column date
        toolkit_new_item(table, iRow, COL_ACTDATE, self.ui.LE_date.text())

        # Column type
        # TODO: fill combo with values coming database saved in settings
        # create combo from default acts defined in settings
        ComboItemsDict = self.winsettings.GetDefaultActs() # returns act names vs price
        ComboItems = ComboItemsDict.keys() # keep only act names
        qComboActs = QtGui.QComboBox()
        qComboActs.addItems(ComboItems)
        # http://stackoverflow.com/questions/1332110/selecting-qcombobox-in-qtablewidget
        qComboActs.setProperty("row", iRow)
        qComboActs.currentIndexChanged.connect(self.OnTableComboChangeValue)
        table.setCellWidget(iRow, COL_ACTTYPE, qComboActs)
        # Column unit price
        # Done using slot OnTableComboChangeValue
        # Column quantity
        qSpinQty = QtGui.QComboBox()
        return 0

    def OnAddAct(self):
        self.TableModelActs.addAct()
    
    def OnRemoveAct(self):
        table = self.ui.m_tableacts
        iRowToDel = table.currentRow()
        rowCount = table.rowCount()
        if rowCount == 0:
         return 0
        print "iRowToDel", iRowToDel
        print "rowCount (before)", rowCount
        table.removeRow(iRowToDel)
        rowCount = table.rowCount()
        print "rowCount (after)", rowCount
        # table.setRowCount(iRow-1)
        return 0 

    # **********  TABLE CLIENTS EVENTS ***********************
    def OnAddDoctor(self):
        table = self.ui.m_tableclients
        iRow = table.rowCount()
        table.setRowCount(iRow+1)
        return 0 

    def OnRemoveDoctor(self):
        table = self.ui.m_tableclients
        rowCount = table.rowCount()
        if rowCount == 0: return 0
        
        iRowToDel = table.currentRow()
        qItem = self.ui.m_tableclients.item(iRowToDel,0)
        qItem2 = self.ui.m_tableclients.item(iRowToDel,1)
        if qItem is None or qItem2 is None : return 0
        sName = self.ui.m_tableclients.item(iRowToDel,0).text()
        sSurname = self.ui.m_tableclients.item(iRowToDel,1).text()
        if sName == "" or sSurname == "" : return 0

        sMsg = "Are you sure to delete a doctor entry and all related dental acts ?"
        toolkit_ShowDeleteMessage(sMsg)
        if ret == QMessageBox.Cancel: return 0

        table.removeRow(iRowToDel)
        # table.setRowCount(rowCount-1)
        return 0 

    def OnDoubleClickClient__DEPRECATED(self, iRow, iCol):
        """ 
            Visualise/edit database of acts for the selected doctor
            Used with a "cellDoubleClicked" signal fired QTableWidget
        """
        qItem = self.ui.m_tableclients.item(iRow,0)
        qItem2 = self.ui.m_tableclients.item(iRow,1)
        if qItem is None or qItem2 is None : 
            return 0

        sName = self.ui.m_tableclients.item(iRow,0).text()
        sSurname = self.ui.m_tableclients.item(iRow,1).text()
        if sName == "" or sSurname == "" : return 0
        else:
           print "Selected doctor: ", sName, sSurname

        return 0

    def OnDoubleClickClient(self, qIndex):
        """ Visualise/edit database of acts for the selected doctor
            Used with a "doubleClicked" signal fired from QTableView
        """
        # qIndex is an instance of QModelIndex 
        # print "Test selection on clients table", qIndex.row(), qIndex.column()
        
        table_view = self.ui.m_tableacts
        table_model_doctors = self.TableModelDoctors
        table_model_acts = self.TableModelActs
        # iRow =  table_view.selectionModel().currentIndex().row()
        iRow = qIndex.row()
        sFirstname = table_model_doctors.index(iRow, COL_DRFIRSTNAME).data()
        sLastname = table_model_doctors.index(iRow, COL_DRLASTNAME).data()
        sPhone = table_model_doctors.index(iRow, COL_DRPHONE).data()
        hash_id = HashClientID(sFirstname,sLastname,sPhone)
        
        # Obsolete if using ActTableModelNew
        # ListActs = self.ParsedDentalDatabase.GetListActsByDoctorID(hash_id)
        # table_model_acts.load_from_list(ListActs)
        table_model_acts.SetModelForDoctorByID(hash_id)
        table_view.setModel(table_model_acts)

        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()

        # for iCol in range(table_model_doctors.columnCount(None)):
        #     itemToChange = table_model_doctors.index(iRow, iCol)
        #     brush = QtGui.QBrush(QtCore.Qt.darkBlue)
        #     itemToChange.data(brush, QtCore.Qt.ForegroundRole)

        return 0


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    window = DentalClientBaseGUI()
    window.show()
    sys.exit(app.exec_())