"""
# USEFUL LINKS
http://www.informit.com/articles/article.aspx?p=1405547&seqNum=3

# Qt
http://doc.qt.io/qt-4.8/qabstractitemmodel.html#endResetModel
"""

# *** qt specific
from PySide import QtGui, QtCore
from PySide.QtGui import QMessageBox
from PySide.QtCore import qDebug
from enum import Enum
from DentalClientBaseSettings import *
import operator

import hashlib
import sys

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
        toolkit_create_formatted_cell(table_widget, iRow, 0, field )        
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

# class ACTCOLUMN(Enum):
#     DATE         = 0
#     TYPE         = 1
#     UNITPRICE    = 2
#     QTY          = 3
#     SUBTOTAL     = 4
#     PAID         = 5

# DoctorTableView is not a necessary implementation
# it is only based on QTableView, ie no delegates
class DoctorTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)

class ActTableView(QtGui.QTableView):
    def __init__(self, *args, **kwargs):
        QtGui.QTableView.__init__(self, *args, **kwargs)

        # self.setItemDelegateForColumn(COL_ACTDATE, DateItemDelegate(self))
        # self.setItemDelegateForColumn(COL_ACTTYPE, ComboDelegate(self))
        # self.setItemDelegateForColumn(COL_ACTQTY, SpinBoxDelegate(self))
        # self.setItemDelegateForColumn(COL_ACTPAID, CheckBoxDelegate(self))
        # setItemDelegate

class DoctorTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, myListOfDoctors, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
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

        # elif role == QtCore.Qt.BackgroundRole:
            # if (row == 1 && col == 2):
                # return 

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
        # if (index.column() == COL_ACTPAID):
            # return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled

class ActTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, myListOfDentalActs, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = [(QtCore.QDateTime.fromString(jAct.Date, "ddmmyyyy"), 
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
        self.mylist = [(QtCore.QDateTime.fromString(jAct.Date, "ddmmyyyy"), 
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
        qDate = QtCore.QDateTime.currentDateTime()
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
    def __init__(self, parent, dentalDatabaseInstance, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)

        self.database = dentalDatabaseInstance
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
    # def GetDentalActDetail(self, DentalActInstance, iCol):
    #     jAct = DentalActInstance

    # ***************************************************
    def SetDentalActDetail(self, DentalActInstance, iCol, value):
        jAct = DentalActInstance
        if iCol < 0 or iCol > self.columnCount(None): return None
        elif iCol == COL_ACTDATE: 
            jAct.SetVarDate(QtCore.QDateTime.toString(value, "ddmmyyyy"))
        elif iCol == COL_ACTTYPE: 
            jAct.Type = value
            return 
        elif iCol == COL_ACTUNITPRICE: 
            return jAct.SetVarUnitPrice(value)
        elif iCol == COL_ACTQTY: 
            return jAct.SetVarQty(value)
        # elif iCol == COL_ACTSUBTOTAL: 
            # return jAct.SubTotal 
        elif iCol == COL_ACTPAID: 
            return jAct.SetVarPaid(value)
    # ***************************************************
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
    
    def data(self, index, role):
        if not index.isValid(): return None
        elif role == QtCore.Qt.DisplayRole:
            iRow = index.row()
            iCol = index.column()
            if iCol < 0 or iCol > self.columnCount(None): 
                return None
            
            dentalActAtRow = self.mylist[iRow]
            val = dentalActAtRow.__getitem__(iCol) # used also by "sorted"
            # special formatting when displaying dates
            if iCol == COL_ACTDATE: 
                return QtCore.QDateTime.fromString(val, "ddmmyyyy")
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
   

    # To enable editing in your model, you must also implement setData(), 
    # and reimplement flags() to ensure that ItemIsEditable is returned
    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        if(role == QtCore.Qt.EditRole):
            iRow = index.row()
            iCol = index.column()            
            dentalActAtRow = self.mylist[iRow]
            self.bUpToDate = False
            self.SetDentalActDetail(dentalActAtRow, iCol, value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        # QtCore.Qt.ItemIsSelectable
        # QtCore.Qt.ItemIsEditable
        # QtCore.Qt.ItemIsEnabled
        if index.column == COL_ACTSUBTOTAL:
            return QtCore.Qt.ItemIsEnabled
        else: 
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        


class ComboDelegate(QtGui.QItemDelegate):
    """
    A delegate that places a fully functioning QComboBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):

        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        combo.setEditable(True)

        li = []
        li.append("Zero")
        li.append("One")
        li.append("Two")
        li.append("Three")
        li.append("Four")
        li.append("Five")
        combo.addItems(li)
        self.connect(combo, QtCore.SIGNAL("currentIndexChanged(int)"), self, QtCore.SLOT("currentIndexChanged()"))
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(int(index.model().data(index)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex())

    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

class SpinBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
  
        return editor
  
    def setEditorData(self, spinBox, index):
        # print "index", index
        # print "index row", index.row()
        # print "index column", index.column()
        # print "index model", index.model()
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        spinBox.setValue(value)
  
    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value() 
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

class DateItemDelegate(QtGui.QStyledItemDelegate):
    def __init__(self, parent = None):
        QtGui.QStyledItemDelegate.__init__(self, parent) 
    def displayText(self, value, locale):
        # if(value.type() == QtCore.QVariant.DateTime):
        return value.toString("dd/MM/yyyy")
        # return value.toDateTime().toString(QtCore.Qt.ISODate)
        # else: return ""
        
# class PopupNewDoctor(QtGui.QWidget):
#     def __init__(self):
#         QtGui.QWidget.__init__(self)

#     def paintEvent(self, e):
#         dc = QPainter(self)
#         dc.drawLine(0, 0, 100, 100)
#         dc.drawLine(100, 0, 0, 100)

# Qt Types
# QtCore.QVariant.Int
# QtCore.QVariant.UInt
# QtCore.QVariant.LongLong
# QtCore.QVariant.ULongLong
# QtCore.QVariant.Double
# QtCore.QVariant.Char
# QtCore.QVariant.Date
# QtCore.QVariant.Time
# QtCore.QVariant.DateTime
# QtCore.QVariant.String