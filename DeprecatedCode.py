##################################################################
##################################################################
##################################################################


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

##################################################################
##################################################################
##################################################################


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
           if verbose: print "Selected doctor: ", sName, sSurname

        return 0



    def OnTableComboChangeValue__DEPRECATED(self, iNumber):
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



##################################################################
##################################################################
##################################################################




class DoctorTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.database = parent.ParsedDentalDatabase
        myListOfDoctors = self.database.GetListDoctors()
        self.mylist = [(jDoctor.Firstname, 
                        jDoctor.Lastname, 
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

    def AddDoctorToDatabase(self, dentalClientInstance):
        self.layoutAboutToBeChanged.emit()
        # self.mylist.append(["Khara", "Kleb", "03-001423"])
        self.database.AddDoctorByInstance(dentalClientInstance)
        self.mylist = self.database.GetListDoctors()
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
