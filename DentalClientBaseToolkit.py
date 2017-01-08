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
from PySide.QtCore import qDebug
from enum import Enum
from DentalClientBaseSettings import *
import operator

import hashlib
import sys

# Non open to user modification
APP_SETTINGS_ACTDATE_FORMAT_DATABASE = "dd/MM/yyyy"

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

def sha1(x):
    return hashlib.sha1(x.encode(sys.getfilesystemencoding())).hexdigest()

def HashClientID(sFirstname, sLastName, sPhone):
    if sFirstname == "": return -1
    if sLastName == "": return -1
    if sPhone == "": return -1
    return sha1(sFirstname+sLastName+sPhone)

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

def toolkit_populate_table_from_dict(table_widget, values_dict):
    table_widget.setRowCount(len(values_dict))
    # table_widget.setColumnCount(2)
    # table_widget.setHorizontalHeaderLabels(['name', 'value'])
    for iRow, field in enumerate(values_dict):
        dValue = values_dict[field]
        toolkit_create_formatted_cell(table_widget, iRow, 0, field.upper() )        
        toolkit_create_formatted_cell(table_widget, iRow, 1, str(dValue) )

def toolkit_create_formatted_cell(table_widget, iRow, iCol, value):
    qItem = QtGui.QTableWidgetItem(value)
    qItem.setTextAlignment( QtCore.Qt.AlignCenter )
    sFont = APP_SETTINGS_TABLE_DEFAULTACTS_FONT
    iFontSize = APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE
    qItem.setFont(QtGui.QFont(sFont, iFontSize, QtGui.QFont.Bold))
    table_widget.setItem(iRow, iCol, qItem)
    return 0

def toolkit_format_existing_cell(table_widget, iRow, iCol):
    qItem = table_widget.item(iRow, iCol)
    qItem.setText(qItem.text().upper())
    qItem.setTextAlignment( QtCore.Qt.AlignCenter )
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

def toolkit_new_item(table_widget, iRow, iCol, sText):
    qItem = table_widget.item(iRow, iCol) 
    if(qItem is None):
        qItem = QtGui.QTableWidgetItem()
        table_widget.setItem(iRow, iCol, qItem)
    qItem.setText(sText)
    qItem.setFlags(QtCore.Qt.ItemIsEnabled)


######################################################################
# MODEL AND DELEGATES
##############################
# http://www.hanskalabs.net/editable-qcombobox-with-qabstracttablemodel.html
# header = ['Solvent Name', ' BP (deg C)', ' MP (deg C)', ' Density (g/ml)']
# data_list = [
# ('ACETIC ACID', 117.9, 16.7, 1.049),
# ('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087),
# ('ACETONE', 56.3, -94.7, 0.791)
# ]

# DoctorTableView is not a necessary implementation
# it is only based on QTableView, ie no delegates
class DoctorTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)
class ActTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)


class DoctorTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.database = parent.ParsedDentalDatabase
        myListOfDoctors = self.database.GetListDoctors()
        self.mylist = [(jDoctor.Firstname, 
                        jDoctor.Surname, 
                        jDoctor.Phone) 
                        for jDoctor in myListOfDoctors]
        self.header = ['First Name','Last Name', 'Phone number']
        # COL_DRFIRSTNAME     = 0
        # COL_DRLASTNAME      = 1
        # COL_DRPHONE         = 2

    def rowCount(self, parent):
        return len(self.mylist)
    
    def columnCount(self, parent):
        if len(self.mylist) == 0: 
            return len(self.header)
        else:
            return len(self.mylist[0])
    
    def data(self, index, role):
        iRow = index.row()
        iCol = index.column()
        if not index.isValid():
            return None

        elif role == QtCore.Qt.FontRole:
            boldFont = QtGui.QFont()
            boldFont.setBold(True)
            return boldFont

        elif role == QtCore.Qt.TextAlignmentRole:
             return QtCore.Qt.AlignCenter

        elif role == QtCore.Qt.DisplayRole:
            return self.mylist[iRow][iCol]
        else:
            return None
    
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.layoutChanged.emit()


    def addAct(self):
        self.layoutAboutToBeChanged.emit()
        self.mylist.append(["Khara", "Kleb", "03-001423"])
        self.layoutChanged.emit()

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
class ActTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, myListOfDentalActs, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = [(QtCore.QDate.fromString(jAct.Date, APP_SETTINGS_ACTDATE_FORMAT_DATABASE), 
                        jAct.Type, 
                        jAct.UnitPrice, 
                        jAct.Qty, 
                        jAct.SubTotal, 
                        jAct.Paid) 
                        for jAct in myListOfDentalActs]
        self.header = ['Date','Act type', 'Unit Price', 'Quantity','SubTotal', 'Paid']
        # COL_ACTDATE         = 0
        # COL_ACTTYPE         = 1
        # COL_ACTUNITPRICE    = 2
        # COL_ACTQTY          = 3
        # COL_ACTSUBTOTAL     = 4
        # COL_ACTPAID         = 5
    
    def load_from_list(self, myListOfDentalActs):
        self.mylist = [(QtCore.QDate.fromString(jAct.Date, APP_SETTINGS_ACTDATE_FORMAT_DATABASE), 
                        jAct.Type, 
                        jAct.UnitPrice, 
                        jAct.Qty, 
                        jAct.SubTotal, 
                        jAct.Paid) 
                        for jAct in myListOfDentalActs]
        self.layoutChanged.emit()
        return 0
    
    def rowCount(self, parent):
        return len(self.mylist)
    
    def columnCount(self, parent):
        if len(self.mylist) == 0: 
            return len(self.header)
        else:
            return len(self.mylist[0])
    
    def data(self, index, role):
        if not index.isValid(): return None
        
        elif role == QtCore.Qt.TextAlignmentRole:
            return  QtCore.Qt.AlignCenter
            # if index.column() == COL_ACTTYPE: 
                # print "returning QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft"
                # return QtCore.Qt.AlignLeft
            # else: 
                # print "returning QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter"
                # return QtCore.Qt.AlignHCenter
        elif role == QtCore.Qt.DisplayRole:
            return self.mylist[index.row()][index.column()]
        
        else:
            return None
    
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.layoutAboutToBeChanged.emit()
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        # self.emit(SIGNAL("layoutChanged()"))
        self.layoutChanged.emit()


    def addAct(self):
        # self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.layoutAboutToBeChanged.emit()
        qDate = QtCore.QDate.currentDate()
        self.mylist.append([qDate,"",0,0,0,1])
        # self.emit(SIGNAL("layoutChanged()"))
        self.layoutChanged.emit()

        """ 
            http://stackoverflow.com/questions/17914944/how-to-get-insertrows-source?rq=1

            View will call `YourModel::data` method immediately after inserting empty rows. 
            You don't need to do any extra operations. View will care about "filling" it.
            Overriding of `YourModel::setData` method is mostly used for interaction between 
            view and model, when user want to change data throught view widget.
        """
    

    # To enable editing in your model, you must also implement setData(), 
    # and reimplement flags() to ensure that ItemIsEditable is returned
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()
            
            actTupleAtGivenRow = self.mylist[iRow]
            actListAtGivenRow = list(actTupleAtGivenRow)
            actListAtGivenRow[iCol] = value
            self.mylist[iRow] = tuple(actListAtGivenRow)

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        # QtCore.Qt.ItemIsSelectable
        # QtCore.Qt.ItemIsEditable
        # QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        
        # if (index.column() == COL_ACTPAID):
        #     return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        # else:
        #     return QtCore.Qt.ItemIsEnabled




    # def insertRow(self, row, parent=QtCore.QModelIndex()):
    #     self.insertRows(row, 1, parent)

    # def insertRows(self, row, count, parent=QtCore.QModelIndex()):
    #     self.beginInsertRows(parent, row, row+count-1)
    #     for i in xrange(count):
    #         self.table.insert(row, ['',]*self.columns)
    #     self.endInsertRows()
    #     return True

    # def removeRow(self, row, parent=QtCore.QModelIndex()):
    #     self.removeRows(row, 1, parent)

    # def removeRows(self, row, count, parent=QtCore.QModelIndex()):
    #     self.beginRemoveRows(parent, row, row+count-1)
    #     for i in reversed(xrange(count)):
    #         self.table.pop(row+i)
    #     self.endRemoveRows()
    #     return True

class ActTableModelNew(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = parent.ParsedDentalDatabase
        self.defaultPrices = parent.DefaultActsDict
        self.doctorID = -1
        self.mylist = [] #initially not showing anything
        self.bUpToDate = True

        headerColumns = dict() 
        headerColumns[COL_ACTDATE] = 'Date'
        headerColumns[COL_ACTTYPE] = 'Act type'
        headerColumns[COL_ACTUNITPRICE] = 'Unit Price'
        headerColumns[COL_ACTQTY] = 'Quantity'
        headerColumns[COL_ACTSUBTOTAL] = 'SubTotal'
        headerColumns[COL_ACTPAID] = 'Paid'
        self.header = headerColumns.values()
    

    # ***************************************************    
    #private get set functions

    def SetModelForDoctorByID(self, iDoctorID):
        """ table view using this model shoud use SetModel 
        after a call to this function """
        self.beginResetModel()
        self.mylist = self.database.GetListActsByDoctorID(iDoctorID)
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
        iRow = index.row()
        iCol = index.column()
        dentalActAtRow = self.mylist[iRow]
        
        if not index.isValid(): 
            return None
        
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

            if iCol < 0 or iCol > self.columnCount(None): 
                return None
            elif iCol == COL_ACTDATE:
                # if value == "": value = self.data(index)
                dentalAct.SetVarDate(value)
            elif iCol == COL_ACTTYPE:
                dentalAct.SetVarType(value, self.defaultPrices[value])
            elif iCol == COL_ACTUNITPRICE:
                # if value == "": value = self.data(index)
                dentalAct.SetVarUnitPrice(value)
            elif iCol == COL_ACTQTY: 
                dentalAct.SetVarQty(value)
            elif iCol == COL_ACTSUBTOTAL: 
                return False 
            elif iCol == COL_ACTPAID: 
                dentalAct.SetVarPaid(value)

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.column in [ COL_ACTSUBTOTAL, COL_ACTDATE] :
            return QtCore.Qt.NoItemFlags
        else: 
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable  

class DoctorTableModelNew(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = parent.ParsedDentalDatabase
        self.doctorID = -1
        self.mylist = self.database.GetListDoctors()
        self.bUpToDate = True

        headerColumns = dict() 
        headerColumns[COL_DRFIRSTNAME] = 'First Name'
        headerColumns[COL_DRLASTNAME] = 'Last Name'
        headerColumns[COL_DRPHONE] = 'Phone Number'
        self.header = headerColumns.values()

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
        iRow = index.row()
        iCol = index.column()
        dentalDoctor = self.mylist[iRow]
        
        if not index.isValid(): 
            return None
        elif role == QtCore.Qt.DisplayRole:
            if iCol < 0 or iCol > self.columnCount(None): return None
            val = dentalDoctor.__getitem__(iCol)
            if iCol == COL_DRFIRSTNAME:
                return self.FormatFirstName(val)  
            if iCol == COL_DRLASTNAME:
                return val.upper()
            if iCol == COL_DRPHONE:
                return self.FormatPhoneNumber(val)
            return val

    def FormatFirstName(self, sVal):
        return sVal[0].upper() + sVal[1:].lower()

    def FormatPhoneNumber(self, sVal):
        if len(sVal) != 8 : return "UNDEFINED"
        if APP_SETTINGS_PHONE_FORMAT == APP_SETTINGS_PHONE_OPTION1:
            return APP_SETTINGS_PHONE_OPTION1.format(sVal[0:2],sVal[2:5],sVal[5:8])
        if APP_SETTINGS_PHONE_FORMAT == APP_SETTINGS_PHONE_OPTION1:
            return APP_SETTINGS_PHONE_OPTION2.format(sVal[0:2],sVal[2:4],sVal[4:6],sVal[6:8])


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
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()            
            dentalDoctor = self.mylist[iRow]
            self.bUpToDate = False

            if iCol < 0 or iCol > self.columnCount(None): 
                return None
            elif iCol == COL_DRFIRSTNAME:
                dentalAct.SetVarFirstname(value)
            elif iCol == COL_DRLASTNAME:
                dentalAct.SetVarLastname(value)
            elif iCol == COL_DRPHONE:
                dentalAct.SetVarPhone(value)

            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        

class ComboDelegate(QtGui.QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent, argItemsList = []):

        QtGui.QItemDelegate.__init__(self, parent)
        self.itemsList = argItemsList

    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        combo.setEditable(True)

        li = []
        if len(self.itemsList) == 0:
            li.append("Zero")
            li.append("One")
            li.append("Two")
            li.append("Three")
        else: 
            li = [sActType.upper() for sActType in self.itemsList]
        
        combo.addItems(li)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return combo

    def setEditorData(self, comboBox, index):
        sComboText = index.model().data(index).upper()
        itemID = comboBox.findText(sComboText)
        comboBox.setCurrentIndex(itemID)
        # comboBox.blockSignals(False)

    def setModelData(self, comboBox, model, index):
        sMsg = "Changing the type of act will remove the current unit price.\n"
        sMsg += "Proceed ?"
        sComboText = comboBox.currentText().upper()
        sOldText = index.model().data(index).upper()
        if sComboText != sOldText:
            ret = toolkit_ShowWarningMessage2(sMsg)
            if(ret == QMessageBox.Ok):
                model.setData(index, sComboText, QtCore.Qt.EditRole)

    def currentIndexChanged(self):
        self.commitData.emit(self.sender())
class SpinBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        spinBox = QtGui.QSpinBox(parent)
        spinBox.setMinimum(0)
        spinBox.setMaximum(100)  
        return spinBox
  
    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        spinBox.setValue(value)
  
    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value() 
        # print ">>> SpinBoxDelegate spinBox.value() ", value
        model.setData(index, value, QtCore.Qt.EditRole)
  
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
class CheckBoxDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent)
    def createEditor(self, parent, option, index):
        return None
    def paint(self, painter, option, index):
        checked = bool(index.model().data(index, QtCore.Qt.DisplayRole))
        check_box_style_option = QtGui.QStyleOptionButton()
        if (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QtGui.QStyle.State_Enabled
        else:
            check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
        if checked:
            check_box_style_option.state |= QtGui.QStyle.State_On
        else:
            check_box_style_option.state |= QtGui.QStyle.State_Off
        check_box_style_option.rect = self.getCheckBoxRect(option)
        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_CheckBox, check_box_style_option, painter)
    def editorEvent(self, event, model, option, index):
        if not (index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False
        # Do not change the checkbox-state
        if event.type() == QtCore.QEvent.MouseButtonRelease or event.type() == QtCore.QEvent.MouseButtonDblClick:
            if event.button() != QtCore.Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() != QtCore.Qt.Key_Space and event.key() != QtCore.Qt.Key_Select:
                return False
        else:
            return False
        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True
    def setModelData (self, editor, model, index):
        newValue = not bool(index.model().data(index, QtCore.Qt.DisplayRole))
        model.setData(index, newValue, QtCore.Qt.EditRole)
    def getCheckBoxRect(self, option):
        check_box_style_option = QtGui.QStyleOptionButton()
        check_box_rect = QtGui.QApplication.style().subElementRect(QtGui.QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QtCore.QPoint (option.rect.x() +
                             option.rect.width() / 2 -
                             check_box_rect.width() / 2,
                             option.rect.y() +
                             option.rect.height() / 2 -
                             check_box_rect.height() / 2)
        return QtCore.QRect(check_box_point, check_box_rect.size())       
class DentalActDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None, argItemsList = []):
        QtGui.QStyledItemDelegate.__init__(self, parent)
        self.list_of_default_acts = list(argItemsList)

    def createEditor(self, parent, option, index):
        iCol = index.column()
        if(iCol == COL_ACTUNITPRICE):
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
            fVal = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setText(str(fVal))

        elif editor.metaObject().className() == "QDateEdit":
            sDate = index.model().data(index, QtCore.Qt.DisplayRole)
            qDate = QtCore.QDate.fromString(sDate, APP_SETTINGS_ACTDATE_FORMAT_DISPLAY)
            editor.setDate(qDate)

        elif editor.metaObject().className() == "QSpinBox":
            value = index.model().data(index, QtCore.Qt.DisplayRole)
            editor.setValue(value)

        elif editor.metaObject().className() == "QComboBox":
            sComboText = index.model().data(index, QtCore.Qt.DisplayRole).upper()
            itemID = editor.findText(sComboText)
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
            if sComboText != sModelText:
                sMsg = "Changing the type of act will remove the current unit price.\n"
                sMsg += "Do you want to proceed ?"
                ret = toolkit_ShowWarningMessage2(sMsg)
                if(ret == QMessageBox.Ok):
                    model.setData(index, sComboText, QtCore.Qt.EditRole)


"""
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