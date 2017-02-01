"""
# USEFUL LINKS
http://www.informit.com/articles/article.aspx?p=1405547&seqNum=3

# Qt
http://doc.qt.io/qt-4.8/qabstractitemmodel.html#endResetModel
"""

# *** qt specific
from PySide import QtGui, QtCore
from PySide.QtGui import QMessageBox
from PySide.QtGui import QColor
# from PySide.QtCore import qDebug
from enum import Enum
from DentalClientBaseSettings import *
import operator

import hashlib
import sys
import webbrowser
import urllib
from urllib import quote

# Non open to user modification
APP_SETTINGS_ACTDATE_FORMAT_DATABASE = "dd/MM/yyyy"

HASH_ROLE = 1000

########################
# Qt dependent settings
########################

#Alignment
ACT_TABLE_ALIGNEMENT_DATE = QtCore.Qt.AlignCenter
ACT_TABLE_ALIGNEMENT_TYPE = QtCore.Qt.AlignLeft and QtCore.Qt.AlignVCenter
ACT_TABLE_ALIGNEMENT_PATIENT = QtCore.Qt.AlignLeft and QtCore.Qt.AlignVCenter
ACT_TABLE_ALIGNEMENT_NOTES = QtCore.Qt.AlignLeft and QtCore.Qt.AlignVCenter
ACT_TABLE_ALIGNEMENT_FLOATS = QtCore.Qt.AlignCenter #and QtCore.Qt.AlignVCenter

#Font: QFont(const QString & family, int pointSize = -1, int weight = -1, bool italic = false)
sFont = APP_SETTINGS_TABLE_ACTS_FONT
iFontSize = APP_SETTINGS_TABLE_ACTS_FONTSIZE
ACT_TABLE_FONT_DATE = QtGui.QFont(sFont, iFontSize, QtGui.QFont.Normal)
ACT_TABLE_FONT_TYPE = QtGui.QFont(sFont, iFontSize, QtGui.QFont.Bold)
ACT_TABLE_FONT_PATIENT = QtGui.QFont(sFont, iFontSize)
ACT_TABLE_FONT_NOTES = QtGui.QFont(sFont, iFontSize)
ACT_TABLE_FONT_FLOATS = QtGui.QFont(sFont, iFontSize, QtGui.QFont.Normal, True)

SETTINGS_ACTNAME_ALIGNEMENT = QtCore.Qt.AlignLeft and QtCore.Qt.AlignVCenter

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

def sha1(x):
    return hashlib.sha1(x.encode(sys.getfilesystemencoding())).hexdigest()

def HashClientID(sFirstname, sLastName, sPhone):
    if sFirstname == "": return None
    if sLastName == "": return None
    if sPhone == "": return None
    return sha1(sFirstname+sLastName+sPhone)

# i need this act hash to search for the act in the database and delete
# unless if passing the row index is sufficient !?
# def HashActID(self):
    # if self.Date="": return None
    # if self.Type="": return None
    # if self.PatientName="": return None
    # return sha1(self.Date+self.Type+str(self.UnitPrice)+str(self.Qty)


# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

def toolkit_populate_table_from_dict(table_widget, values_dict, qFlags = None ):
    if qFlags is None: 
        qFlags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
    table_widget.setRowCount(len(values_dict))
    # table_widget.setColumnCount(2)
    # table_widget.setHorizontalHeaderLabels(['name', 'value'])
    for iRow, field in enumerate(values_dict):
        dValue = values_dict[field]
        toolkit_create_formatted_cell(table_widget, iRow, 0, field.upper(), qFlags)        
        toolkit_create_formatted_cell(table_widget, iRow, 1, str(dValue), qFlags )

def toolkit_create_formatted_cell(table_widget, iRow, iCol, value, qFlags):
    qItem = QtGui.QTableWidgetItem(value)
    qItem.setTextAlignment( SETTINGS_ACTNAME_ALIGNEMENT )
    sFont = APP_SETTINGS_TABLE_DEFAULTACTS_FONT
    iFontSize = APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE
    qItem.setFont(QtGui.QFont(sFont, iFontSize, QtGui.QFont.Bold))
    qItem.setFlags(qFlags)
    if qFlags == QtCore.Qt.ItemIsEnabled:
        qItem.setBackground(QColor(240,240,255))
    table_widget.setItem(iRow, iCol, qItem)
    return 0

def toolkit_format_existing_cell(table_widget, iRow, iCol):
    qItem = table_widget.item(iRow, iCol)
    qItem.setText(qItem.text().upper())
    qItem.setTextAlignment( SETTINGS_ACTNAME_ALIGNEMENT )
    sFont = APP_SETTINGS_TABLE_DEFAULTACTS_FONT
    iFontSize = APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE
    qItem.setFont(QtGui.QFont(sFont, iFontSize, QtGui.QFont.Bold))
    return 0

def toolkit_ShowWarningMessage(msg):
    msgBox = QMessageBox()
    msgBox.setText("Warning")
    msgBox.setInformativeText(msg)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    # msgBox.setIcon(QMessageBox.Warning)
    res = APP_SETTINGS_SCALED_ICONS_RESOLUTION
    msgBox.setIconPixmap(QtGui.QPixmap('res/information.png').scaled(res,res))
    return msgBox.exec_()

def toolkit_ShowWarningMessage2(msg):
    msgBox = QMessageBox()
    msgBox.setText("Warning")
    msgBox.setInformativeText(msg)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Cancel)
    # msgBox.setIcon(QMessageBox.Warning)
    res = APP_SETTINGS_SCALED_ICONS_RESOLUTION
    msgBox.setIconPixmap(QtGui.QPixmap('res/information.png').scaled(res,res))
    return msgBox.exec_()

def toolkit_ShowWarningMessage3(msg):
    msgBox = QMessageBox()
    msgBox.setText("Warning")
    msgBox.setInformativeText(msg)
    msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Save)
    # msgBox.setIcon(QMessageBox.Warning)
    res = APP_SETTINGS_SCALED_ICONS_RESOLUTION
    msgBox.setIconPixmap(QtGui.QPixmap('res/information.png').scaled(res,res))
    return msgBox.exec_()

def toolkit_ShowCriticalMessage(msg):
    msgBox = QMessageBox()
    msgBox.setText("Critical")
    msgBox.setInformativeText(msg)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.setDefaultButton(QMessageBox.Ok)
    # msgBox.setIcon(QMessageBox.Critical)
    res = APP_SETTINGS_SCALED_ICONS_RESOLUTION
    msgBox.setIconPixmap(QtGui.QPixmap('res/flag.png').scaled(res,res))
    return msgBox.exec_()

def toolkit_ShowDeleteMessage(msg):
    msgBox = QMessageBox()
    msgBox.setText("You are about to delete")
    msgBox.setInformativeText(msg)
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msgBox.setDefaultButton(QMessageBox.Cancel)
    # msgBox.setIcon(QMessageBox.Critical)
    res = APP_SETTINGS_SCALED_ICONS_RESOLUTION
    msgBox.setIconPixmap(QtGui.QPixmap('res/garbage.png').scaled(res,res))
    return msgBox.exec_()

def toolkit_ReportUndefinedBehavior(sErrMsg = ""):
    sMsg = "Unedfined error."
    sMsg += " Please contact Ali Saad for more information."
    toolkit_ShowWarningMessage(sErrMsg)
    toolkit_ErrorReport(sErrMsg)
    return

def toolkit_ErrorReport(sErrMsg = ""):
    sNonEncodedUrl = str(APP_SETTINGS_REPORTING) + sErrMsg
    sEncodedUrl = urllib.quote(sNonEncodedUrl)
    webbrowser.open_new_tab(APP_SETTINGS_REPORTING)
    return

def toolkit_new_item(table_widget, iRow, iCol, sText):
    qItem = table_widget.item(iRow, iCol) 
    if(qItem is None):
        qItem = QtGui.QTableWidgetItem()
        table_widget.setItem(iRow, iCol, qItem)
    qItem.setText(sText)
    qItem.setFlags(QtCore.Qt.ItemIsEnabled)
    return

def toolkit_compare_dicts(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, removed, modified #, same

class PriceChangeClass(QtCore.QObject):    
    PricesChanged = QtCore.Signal()

##################################################################
############### MODEL AND DELEGATES ##############################
##################################################################

# DoctorTableView is not a necessary implementation
# it is only based on QTableView, ie no delegates
class DoctorTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)
        
    # def focusOutEvent(self, event):
    #     # self.setFocus(QtCore.Qt.StrongFocus)
    #     selectionModel = self.selectionModel()
    #     selectedIndexes = selectionModel.selectedIndexes()
    #     qIndex = selectedIndexes[0]
    #     if not qIndex.isValid(): return 0
    #     selectionModel.select(qIndex, QtGui.QItemSelectionModel.Deselect)

class ActTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        
        QtGui.QTableView.__init__(self, *args, **kwargs)
        
        def mousePressEvent(self, qMouseEvent):
            if (qMouseEvent.button() == Qt.LeftButton):
                qModelIndex = indexAt(qMouseEvent.pos())
                # column you want to use for one click
                if (qModelIndex.column() == COL_ACTTYPE):  
                    edit(qModelIndex)

            QtGui.QTableView.mousePressEvent(qMouseEvent)

###################################################################################
class DoctorTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = parent.ParsedDentalDatabase
        self.doctorID = -1
        self.mylist = self.database.GetListDoctors()
        self.bUpToDate = True
        self.header = DOCTORS_HEADER_DICT.values()

    # ***************************************************
    def IsUpToDate(self):
        """ return boolean to check if user changed values """
        return self.bUpToDate
    # ***************************************************

    def rowCount(self, parent):
        # return len(self.mylist)
        return self.database.GetNbDoctors()
    
    def columnCount(self, parent):
        if len(self.mylist) == 0: 
            return len(self.header)
        else:
            return len(self.mylist[0])
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): return None
        iRow = index.row()
        iCol = index.column()
        dentalDoctor = self.mylist[iRow]

        if role == HASH_ROLE:
            return dentalDoctor.__getitem__(iCol)
            
        elif role == QtCore.Qt.DisplayRole:
            val = dentalDoctor.__getitem__(iCol)
            if iCol == COL_DRFIRSTNAME:
                return self.FormatFirstName(val)  
            if iCol == COL_DRLASTNAME:
                return self.FormatLastName(val)
            if iCol == COL_DRPHONE:
                return self.FormatPhoneNumber(val)

        else: return None

    def FormatFirstName(self, sVal):
        return sVal[0].upper() + sVal[1:].lower()

    def FormatLastName(self, sVal):
        return sVal.upper()

    def FormatPhoneNumber(self, sVal):
        # if len(sVal) != 8 : return "UNDEFINED"
        if APP_SETTINGS_PHONE_FORMAT == APP_SETTINGS_PHONE_OPTION1:
            return APP_SETTINGS_PHONE_OPTION1.format(sVal[0:2],sVal[2:5],sVal[5:8])
        if APP_SETTINGS_PHONE_FORMAT == APP_SETTINGS_PHONE_OPTION1:
            return APP_SETTINGS_PHONE_OPTION2.format(sVal[0:2],sVal[2:4],sVal[4:6],sVal[6:8])

    def UnFormatPhoneNumber(self, sVal):
        sUnformatted = str(sVal)
        sUnformatted.replace("-","")
        sUnformatted.replace(" ","")
        return sUnformatted

    def getHashIDFromSelectedDoctor(self, index):
        iRow = index.row()
        sFname = self.index(iRow, COL_DRFIRSTNAME).data(HASH_ROLE)
        sLname = self.index(iRow, COL_DRLASTNAME).data(HASH_ROLE)
        sPhone = self.index(iRow, COL_DRPHONE).data(HASH_ROLE)
        return HashClientID(sFname,sLname,sPhone)

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        """
        IMPORTANT: itemgetter is needed to determine a value at position
        it only works with standard containers unless i reimplement the 
        method __getitem__
        """
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder: self.mylist.reverse()
        self.layoutChanged.emit()
   
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        """ For now, we cannot modify a doctor but only add one
            so this function is not used
            TODO: check how to edit a doctor using the existing QDialog class
            then UPDATE THE HASH ID IN THE DATABASE FOR THIS DOCTOR
        """
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()            
            # dentalDoctor = self.mylist[iRow]
            doctorID = self.getHashIDFromSelectedDoctor(index)
            dentalDoctor = self.database.GetDoctorFromID(doctorID)
            if dentalDoctor is None: return None
            self.bUpToDate = False

            if iCol < 0 or iCol > self.columnCount(None): 
                return None
            elif iCol == COL_DRFIRSTNAME:
                dentalDoctor.SetVarFirstname(value)
            elif iCol == COL_DRLASTNAME:
                dentalDoctor.SetVarLastname(value)
            elif iCol == COL_DRPHONE:
                dentalDoctor.SetVarPhone(self.UnFormatPhoneNumber(value))

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsEditable
        

    def AddDoctorToDatabase(self, dentalClientInstance):
        self.layoutAboutToBeChanged.emit()
        self.database.AddDoctorByInstance(dentalClientInstance)
        # self.database.SetDoctorPricesByDoctorID(dentalClientInstance.id(), dictOfDoctorPrices)
        self.mylist = self.database.GetListDoctors()
        self.layoutChanged.emit()
        self.bUpToDate = False

    def RemoveDoctorFromDatabase(self, iDoctorID):
        self.layoutAboutToBeChanged.emit()
        self.database.RemoveDoctorByID(iDoctorID)
        self.mylist = self.database.GetListDoctors()
        self.layoutChanged.emit()
        self.bUpToDate = False
###################################################################################
class ActTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = parent.ParsedDentalDatabase
        self.doctorID = -1
        self.mylist = [] #initially not showing anything
        self.bUpToDate = True
        self.header = ACTS_HEADER_DICT.values()
        self.DoctorPrices = None

        self.MySignal = PriceChangeClass()

    def SetModelForDoctorByID(self, iDoctorID):
        """ table view using this model shoud use SetModel 
        after a call to this function """
        self.beginResetModel()
        self.doctorID = iDoctorID
        self.DoctorPrices = self.database.GetDoctorPricesByDoctorID(iDoctorID)
        self.mylist = self.database.GetListActsByDoctorID(iDoctorID)
        self.endResetModel()
        return

    def IsUpToDate(self):
        """ return boolean to check if user changed values """
        return self.bUpToDate

    def rowCount(self, parent):
        return len(self.mylist)
    
    def columnCount(self, parent):
        if len(self.mylist) == 0: 
            return len(self.header)
        else:
            return len(self.mylist[0])
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): return None
        iRow = index.row()
        iCol = index.column()
        dentalActAtRow = self.mylist[iRow]

        # BackgroundRole
        if role == QtCore.Qt.FontRole:
            if iCol in [COL_ACTUNITPRICE, COL_ACTQTY, COL_ACTSUBTOTAL]:
                return ACT_TABLE_FONT_FLOATS
            elif iCol == COL_ACTTYPE:
                return ACT_TABLE_FONT_TYPE
            elif iCol == COL_ACTPATIENT:
                return ACT_TABLE_FONT_PATIENT
            elif iCol == COL_ACTDATE:
                return ACT_TABLE_FONT_DATE
            elif iCol == COL_ACTNOTES:
                return ACT_TABLE_FONT_NOTES

        elif role == QtCore.Qt.TextAlignmentRole:
            if iCol in [COL_ACTUNITPRICE, COL_ACTQTY, COL_ACTSUBTOTAL]:
                return ACT_TABLE_ALIGNEMENT_FLOATS
            elif iCol == COL_ACTTYPE:
                return ACT_TABLE_ALIGNEMENT_TYPE
            elif iCol == COL_ACTPATIENT:
                return ACT_TABLE_ALIGNEMENT_PATIENT
            elif iCol == COL_ACTDATE:
                return ACT_TABLE_ALIGNEMENT_DATE
            elif iCol == COL_ACTNOTES:
                return ACT_TABLE_ALIGNEMENT_NOTES

        elif role == QtCore.Qt.DisplayRole:
            if iCol < 0 or iCol > self.columnCount(None): return None
            # `__getitem__` used also by "sorted"
            val = dentalActAtRow.__getitem__(iCol)
            if iCol == COL_ACTDATE: 
                qDate = QtCore.QDate.fromString(val, APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
                return qDate.toString(APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            else: 
                return val
        
        # elif role == QtCore.Qt.BackgroundRole:
        #     iPaid = dentalActAtRow.__getitem__(COL_ACTPAID)
        #     if(iPaid == 1): 
        #         background = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
        #     else:
        #         background = QtGui.QBrush(QtCore.Qt.GlobalColor.white)

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.layoutAboutToBeChanged.emit()
        """
        IMPORTANT: itemgetter is needed to determine a value at position
        it only works with standard containers unless i reimplement the 
        method __getitem__
        """
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder: self.mylist.reverse()
        self.layoutChanged.emit()
   

    # To enable editing in your model, you must also implement setData(), 
    # and reimplement flags() to ensure that ItemIsEditable is returned
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()            
            dentalAct = self.mylist[iRow]
            self.bUpToDate = False
            bDictPricesChanged = False

            if iCol < 0 or iCol > self.columnCount(None): 
                return None

            elif iCol == COL_ACTDATE:
                # if value == "": value = self.data(index)
                dentalAct.SetVarDate(value)

            elif iCol == COL_ACTTYPE:
                if value not in self.DoctorPrices:
                    if value != "":
                        sMsg = "The act type ({0}) is not supported.".format(value)
                        toolkit_ShowWarningMessage(sMsg)
                    return False
                dentalAct.SetVarType(value, self.DoctorPrices[value])

            elif iCol == COL_ACTNOTES:
                dentalAct.SetVarNotes(value)

            elif iCol == COL_ACTUNITPRICE:
                sType = dentalAct.__getitem__(COL_ACTTYPE)
                # change doctor prices 
                if sType not in self.DoctorPrices:
                    sMsg = str()
                    if value == "" or value == str(float(0.0)):
                        sMsg = "The unit price of this act cannot be changed because act type is empty. \n"
                        sMsg += "Select an act type from the combo list of available act types."
                    else:
                        sMsg = "The act type ({0}) is no longer supported, ".format(sType)
                        sMsg += "because you have probably deleted the corresponding "
                        sMsg += "act type from the application's Preferences. "
                        sMsg += "Therefore its unit price is locked. It can only be "
                        sMsg += "changed if you declare the act again in the Preferences."
                    toolkit_ShowWarningMessage(sMsg)
                    return False
                self.DoctorPrices[sType] = float(value)
                dentalAct.SetVarUnitPrice(value)
                bDictPricesChanged = True
            
            elif iCol == COL_ACTQTY: 
                dentalAct.SetVarQty(value)
            
            elif iCol == COL_ACTSUBTOTAL: 
                return False 
            
            elif iCol == COL_ACTPAID: 
                dentalAct.SetVarPaid(value)
            
            elif iCol == COL_ACTPATIENT: 
                dentalAct.SetVarPatientName(value)

            if bDictPricesChanged:
                self.database.SetDoctorPricesByDoctorID(self.doctorID, self.DoctorPrices)
                self.MySignal.PricesChanged.emit()
            
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.column in [ COL_ACTSUBTOTAL, COL_ACTDATE] :
            return QtCore.Qt.NoItemFlags
        else: 
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable  

    def addDentalAct(self, iDoctorID, dentalActInstance):
        self.beginResetModel()
        count = self.database.GetNbActsByDoctorID(iDoctorID)
        self.beginInsertRows(QtCore.QModelIndex(), count, count+1)
        self.database.AppendActByInstanceToDoctorByID(iDoctorID, dentalActInstance)
        self.endInsertRows()
        self.endResetModel()
        self.bUpToDate = False

    def removeDentalAct(self, iDoctorID, iRowIndex):
        self.beginResetModel()
        count = self.database.GetNbActsByDoctorID(iDoctorID)
        self.beginRemoveRows(QtCore.QModelIndex(), count, count-1)
        self.database.RemoveActByIndexByDoctorID(iDoctorID, iRowIndex)
        self.endRemoveRows()
        self.endResetModel()
        self.bUpToDate = False
####################################################################################
class PaymentTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = parent.ParsedDentalDatabase
        self.doctorID = -1
        self.mylist = [] #initially not showing anything
        self.bUpToDate = True
        self.header = PAYMENTS_HEADER_DICT.values()
    # ***************************************************    
    #private get set functions

    def SetModelForDoctorByID(self, iDoctorID):
        """ table view using this model shoud use SetModel 
        after a call to this function """
        self.beginResetModel()
        self.doctorID = iDoctorID
        self.mylist = self.database.GetListPaymentsByDoctorID(iDoctorID)
        self.endResetModel()
        return
    # ***************************************************
    def IsUpToDate(self):
        """ return boolean to check if user changed values """
        return self.bUpToDate
    # ***************************************************

    def rowCount(self, parent):
        return len(self.mylist)
    
    def columnCount(self, parent):
        if len(self.mylist) == 0: 
            return len(self.header)
        else:
            return len(self.mylist[0])
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if not index.isValid(): return None
        iRow = index.row()
        iCol = index.column()
        dentalPaymentAtRow = self.mylist[iRow]

        # BackgroundRole
        if role == QtCore.Qt.FontRole:
            if iCol == COL_PAYMENTSUM:
                return ACT_TABLE_FONT_FLOATS
            elif iCol == COL_PAYMENTDATE:
                return ACT_TABLE_FONT_DATE

        elif role == QtCore.Qt.TextAlignmentRole:
            if iCol == COL_PAYMENTSUM:
                return ACT_TABLE_ALIGNEMENT_FLOATS
            elif iCol == COL_PAYMENTDATE:
                return ACT_TABLE_ALIGNEMENT_DATE

        elif role == QtCore.Qt.DisplayRole:
            if iCol < 0 or iCol > self.columnCount(None): return None
            # `__getitem__` used also by "sorted"
            val = dentalPaymentAtRow.__getitem__(iCol)
            if iCol == COL_PAYMENTDATE: 
                qDate = QtCore.QDate.fromString(val, APP_SETTINGS_ACTDATE_FORMAT_DATABASE)
                return qDate.toString(APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            else: 
                return val

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.layoutAboutToBeChanged.emit()
        """
        IMPORTANT: itemgetter is needed to determine a value at position
        it only works with standard containers unless i reimplement the 
        method __getitem__
        """
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder: self.mylist.reverse()
        self.layoutChanged.emit()
   

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()            
            dentalPayment = self.mylist[iRow]
            self.bUpToDate = False

            if iCol < 0 or iCol > self.columnCount(None): 
                return None
            elif iCol == COL_PAYMENTDATE:
                # if value == "": value = self.data(index)
                dentalPayment.SetVarDate(value)
            elif iCol == COL_PAYMENTSUM:
                # if value == "": value = self.data(index)
                dentalPayment.SetVarSum(value)

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.column in [ COL_PAYMENTDATE] :
            return QtCore.Qt.NoItemFlags
        else: 
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable  

    def addDentalPayment(self, iDoctorID, dentalPaymentInstance):
        self.beginResetModel()
        count = self.database.GetNbActsByDoctorID(iDoctorID)
        self.beginInsertRows(QtCore.QModelIndex(), count, count+1)
        self.database.AppendPaymentByInstanceToDoctorByID(iDoctorID, dentalPaymentInstance)
        self.endInsertRows()
        self.endResetModel()
        self.bUpToDate = False

    def removeDentalPayment(self, iDoctorID, iRowIndex):
        self.beginResetModel()
        count = self.database.GetNbActsByDoctorID(iDoctorID)
        self.beginRemoveRows(QtCore.QModelIndex(), count, count-1)
        self.database.RemovePaymentByIndexByDoctorID(iDoctorID, iRowIndex)
        self.endRemoveRows()
        self.endResetModel()
        self.bUpToDate = False
####################################################################################
class DentalPaymentDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        
    def createEditor(self, parent, option, index):
        iCol = index.column()
        if(iCol in [ COL_PAYMENTSUM ]):
            editor = QtGui.QLineEdit(parent)
            return editor  
        elif(iCol == COL_PAYMENTDATE):
            editor = QtGui.QDateEdit(parent)
            editor.setDisplayFormat(APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            editor.setCalendarPopup(True)
            return editor
        
    def setEditorData(self, editor, index):
        if editor.metaObject().className() == "QLineEdit":
            # val can be a float (unit price) or string (patient name)
            val = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setText(str(val))
        elif editor.metaObject().className() == "QDateEdit":
            sDate = index.model().data(index, QtCore.Qt.DisplayRole)
            qDate = QtCore.QDate.fromString(sDate, APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            editor.setDate(qDate)

    def setModelData(self, editor, model, index):
     
        if editor.metaObject().className() == "QLineEdit":
            model.setData(index, editor.text(), QtCore.Qt.EditRole)

        elif editor.metaObject().className() == "QDateEdit":
            model.setData(index, editor.date().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE), QtCore.Qt.EditRole)

class DentalActDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None, argItemsList = []):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.list_of_default_acts = None
        self.setActTypesStringList(argItemsList)

    def createEditor(self, parent, option, index):
        iCol = index.column()
        if(iCol in [COL_ACTUNITPRICE, COL_ACTPATIENT, COL_ACTNOTES]):
            editor = QtGui.QLineEdit(parent)
            return editor            
        elif(iCol == COL_ACTDATE):
            editor = QtGui.QDateEdit(parent)
            editor.setDisplayFormat(APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            editor.setCalendarPopup(True)
            return editor
        elif iCol == COL_ACTQTY:
            editor = QtGui.QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(50)  
            return editor
        elif iCol == COL_ACTTYPE:
            editor = QtGui.QComboBox(parent)
            editor.setEditable(False)
            editor.addItems(self.list_of_default_acts)
            return editor

    def setEditorData(self, editor, index):
        # iCol = index.column()
        if editor.metaObject().className() == "QLineEdit":
            # val can be a float (unit price) or string (patient name)
            val = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setText(str(val))

        elif editor.metaObject().className() == "QDateEdit":
            sDate = index.model().data(index, QtCore.Qt.DisplayRole)
            qDate = QtCore.QDate.fromString(sDate, APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            editor.setDate(qDate)

        elif editor.metaObject().className() == "QSpinBox":
            value = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setValue(value)

        elif editor.metaObject().className() == "QComboBox":
            sComboText = index.model().data(index, QtCore.Qt.DisplayRole).upper()
            # which means ignore the default flag CaseSensitive
            itemID = editor.findText(sComboText, QtCore.Qt.MatchExactly)
            editor.setCurrentIndex(itemID)

    def setModelData(self, editor, model, index):
                
        if editor.metaObject().className() == "QLineEdit":
            model.setData(index, editor.text(), QtCore.Qt.EditRole)
            
        elif editor.metaObject().className() == "QDateEdit":
            model.setData(index, editor.date().toString(APP_SETTINGS_ACTDATE_FORMAT_DATABASE), QtCore.Qt.EditRole)
        
        elif editor.metaObject().className() == "QSpinBox":
            editor.interpretText()
            model.setData(index, editor.value(), QtCore.Qt.EditRole)

        elif editor.metaObject().className() == "QComboBox":
            sComboText = editor.currentText().upper()
            sModelText = index.model().data(index).upper()
            if sModelText == "" or sModelText == sComboText:
                model.setData(index, sComboText, QtCore.Qt.EditRole)
            else:
                sMsg = "Changing the type of act will remove the current unit price.\n"
                sMsg += "Do you want to proceed ?"
                ret = toolkit_ShowWarningMessage2(sMsg)
                if(ret == QMessageBox.Ok):
                    model.setData(index, sComboText, QtCore.Qt.EditRole)

    def setActTypesStringList(self, sList):
        """ this method only loads the Types without prices as these can vary 
            between clients.
        """
        self.list_of_default_acts = [sItem.upper() for sItem in sList]


"""
EDIT TRIGGERS FOR TABLE VIEWS
Constant    Value   Description
QAbstractItemView::NoEditTriggers   0   No editing possible.
QAbstractItemView::CurrentChanged   1   Editing start whenever current item changes.
QAbstractItemView::DoubleClicked    2   Editing starts when an item is double clicked.
QAbstractItemView::SelectedClicked  4   Editing starts when clicking on an already selected item.
QAbstractItemView::EditKeyPressed   8   Editing starts when the platform edit key has been pressed over an item.
QAbstractItemView::AnyKeyPressed    16  Editing starts when any key is pressed over an item.
QAbstractItemView::AllEditTriggers  31  Editing starts for all above actions.


This enum describes the properties of an item:

Constant            Value   Description
Qt::NoItemFlags         0   It does not have any properties set.
Qt::ItemIsSelectable    1   It can be selected.
Qt::ItemIsEditable      2   It can be edited.
Qt::ItemIsDragEnabled   4   It can be dragged.
Qt::ItemIsDropEnabled   8   It can be used as a drop target.
Qt::ItemIsUserCheckable 16  It can be checked or unchecked by the user.
Qt::ItemIsEnabled       32  The user can interact with the item.
Qt::ItemIsTristate      64  The item is checkable with three separate states.

Qt Types
QtCore.QVariant.Int
QtCore.QVariant.UInt
QtCore.QVariant.LongLong
QtCore.QVariant.ULongLong
QtCore.QVariant.Double
QtCore.QVariant.Char
QtCore.QVariant.Date
QtCore.QVariant.Time
QtCore.QVariant.DateTime
QtCore.QVariant.String

"""