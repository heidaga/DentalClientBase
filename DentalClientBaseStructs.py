import cPickle as pickle
import os
from DentalClientBaseToolkit import HashClientID
from DentalClientBaseSettings import *

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

# dic_save = { "lion": "yellow", "kitty": "red" }
# pickle.dump( dic_save, open( "save.p", "wb" ) )
# dic_load = pickle.load( open( "save.p", "rb" ) )

def pkl_save(obj, filename):
    # if filename == ""
    filedir = os.path.dirname(filename)    
    basename = os.path.basename(filename)    
    if not os.path.exists(filedir):
        filename = os.path.join(APP_RESOURCES,basename)
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, 0) # pickle.HIGHEST_PROTOCOL

def pkl_load(sDatabasePath):
    if sDatabasePath == "": return None
    DatabaseData = pickle.load( open( sDatabasePath , "rb" ) )
    if(len(DatabaseData) == 0): 
        print "Database is empty !"
        return None
    else:
        return DatabaseData
    
# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalAct:
	""" Implementation of a single dental act """

	def __init__(self, sDate, sPatient = "", sType= "", iQty = 0, fUnitPrice = 0.0):
		# self.Firstname = fname
		# self.Lastname = sname
		# ObjClient is instance of DentalClient
		
		# self.client = ObjClient # no need anymore coz instanciated as part of DentalClient
		self.Date = sDate
		self.Type = sType
		self.Qty = iQty
		self.UnitPrice = fUnitPrice
		self.SubTotal = self.Qty  * self.UnitPrice
		self.PatientName = sPatient
		self.Notes = ""

		# Not to be viewed
		self.Paid = 0

	def __len__(self):
		""" returns number of member variables to be used externally (by Qt) """
		return 7

	def GetMonth(self):
		# ATTENTION: APP_SETTINGS_ACTDATE_FORMAT_DISPLAY
		return str(self.Date.split("/")[1])

	def GetYear(self):
		# ATTENTION: APP_SETTINGS_ACTDATE_FORMAT_DISPLAY
		return str(self.Date.split("/")[2])

	def SetVarDate(self, sDate):
		self.Date = str(sDate)
		return 0

	def SetVarQty(self, iNewQty):
		self.Qty = int(iNewQty)
		self.SubTotal = self.Qty  * self.UnitPrice
		return 0

	def SetVarUnitPrice(self, fNewUnitPrice):
		self.UnitPrice = float(fNewUnitPrice)
		self.SubTotal = self.Qty  * self.UnitPrice
		return 0

	def SetVarPaid(self, iPaid):
		self.Paid = int(iPaid)
		return 0

	def SetVarPatientName(self, sPatientName):
		self.PatientName = str(sPatientName)
		return 0

	def SetVarType(self, sType, fDefaultUnitPrice = None):
		self.Type = str(sType)
		if fDefaultUnitPrice is not None:
			self.SetVarUnitPrice(fDefaultUnitPrice)
		return 0

	def SetVarNotes(self, sNotes):
		self.Notes = str(sNotes)
		return 0

	""" ONLY FOR SORTING : acts as a getter 
		To sort dates, i only return the date string
		then the output value is Qt-formatted in the GUI class 
	"""
	def __getitem__(self, iCol):
		if iCol == COL_ACTDATE: 
			return self.Date
			# return QtCore.QDateTime.fromString(self.Date, "ddmmyyyy")
		elif iCol == COL_ACTTYPE: 
			return self.Type
		elif iCol == COL_ACTUNITPRICE: 
			return self.UnitPrice
		elif iCol == COL_ACTQTY: 
			return self.Qty
		elif iCol == COL_ACTSUBTOTAL: 
			# return self.SubTotal 
			return self.Qty  * self.UnitPrice 
		elif iCol == COL_ACTPATIENT: 
			return self.PatientName
		elif iCol == COL_ACTPAID: 
			return self.Paid
		elif iCol == COL_ACTNOTES: 
			return self.Notes
		else: raise IndexError("Index used in __getitem__ is not supported")

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalClient:
	def __init__(self, fname, sname, sphone , email = "", address = ""):
		self.Firstname = fname   	# string required
		self.Lastname = sname 		# string required
		self.Phone = sphone			# string required

		self.Email = email 			# string optional
		self.Address = address 		# string optional

		self.acts = list()
		self.payments = list()
		self.defaultprices = dict()

	def __len__(self):
		""" returns number of member variables to be used externally (by Qt) """
		return 3

	def AppendPaymentByDetails(self, sDate, fSum):
		cNewPayment = DentalPayment(sDate, fSum)
		self.payments.append(cNewPayment)

		
	def AppendActByDetails(self, sDate, sPatientName, sType, iQty):
		fUnitPrice = 0.0
		if sType in self.defaultprices:
			fUnitPrice = self.defaultprices[sType]
		# else:
			# print("Warning::AppendActByDetails: sType {0} not found".format(sType))
			# return
		cNewAct = DentalAct(sDate, sPatientName, sType, iQty, fUnitPrice)
		self.acts.append(cNewAct)
		
	# def AppendActByInstance(self, cNewAct):
	# 	if cNewAct is None: 
	# 		raise Exception("AddActToDoctor:: dentalAct is None")
	# 		return 0
	# 	else:
	# 		self.acts.append(cNewAct)
	# 	return 0
		
	def RemovePaymentByIndex(self, iIndex):
		if iIndex < 0: return 0
		else: del self.payments[iIndex]
		return 0
	
	def RemoveActByIndex(self, iIndex):
		if iIndex < 0: return 0
		else: del self.acts[iIndex]
		return 0

	def id(self):
		# return sha1(self.Firstname+self.Lastname+self.Phone)
		return HashClientID(self.Firstname,self.Lastname,self.Phone)

	def GetFullName(self):
		return "Dr. {0} {1}".format(self.Firstname, self.Lastname)

	def GetExportName(self):
		sName = self.GetFullName()
		sNameNoSpace = sName.replace(" ", "_")
		return sNameNoSpace

	def SetVarFirstname(self, sVal):
		self.Firstname = str(sVal)

	def SetVarLastname(self, sVal):
		self.Lastname = str(sVal)

	def SetVarPhone(self, sVal):
		self.Phone = str(sVal)

	def SetVarEmail(self, sVal):
		self.Email = str(sVal)

	def SetVarAddress(self, sVal):
		self.Address = str(sVal)

	""" 
		ONLY FOR SORTING : acts as a getter 
		To sort dates, i only return the date string
		then the output value is Qt-formatted in the GUI class 
	"""

	def GetDoctorPrices(self):
		return dict(self.defaultprices)
	
	def SetDoctorPrices(self, dictOfDefaultPrices):
		self.defaultprices = dict(dictOfDefaultPrices)
		return

	def __getitem__(self, iCol):
		if iCol == COL_DRFIRSTNAME: 
			return self.Firstname
		elif iCol == COL_DRLASTNAME: 
			return self.Lastname
		elif iCol == COL_DRPHONE: 
			return self.Phone
		else: raise IndexError("Index used in __getitem__ is not supported")

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalPayment:
	""" Implementation of a single dental payment """

	def __init__(self, sDate, fSum = 0.0):
		
		# self.client = ObjClient # no need anymore coz instanciated as part of DentalClient
		self.Date = sDate
		self.Sum = fSum

	def __len__(self):
		""" returns number of member variables to be used externally (by Qt) """
		return 2

	def GetMonth(self):
		# ATTENTION: APP_SETTINGS_ACTDATE_FORMAT_DISPLAY
		return str(self.Date.split("/")[1])

	def GetYear(self):
		# ATTENTION: APP_SETTINGS_ACTDATE_FORMAT_DISPLAY
		return str(self.Date.split("/")[2])

	def SetVarDate(self, sDate):
		self.Date = str(sDate)
		return 0

	def SetVarSum(self, fSum):
		self.Sum = float(fSum)
		return 0

	""" ONLY FOR SORTING : acts as a getter 
		To sort dates, i only return the date string
		then the output value is Qt-formatted in the GUI class 
	"""
	def __getitem__(self, iCol):
		if iCol == COL_PAYMENTDATE: 
			return self.Date
			# return QtCore.QDateTime.fromString(self.Date, "ddmmyyyy")
		elif iCol == COL_PAYMENTSUM: 
			return self.Sum
		else: raise IndexError("Index used in __getitem__ is not supported")


# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalDatabase:
	def __init__(self, listDentalClients = []):
		self.ClientsMap = dict()
		if len(listDentalClients) != 0:
			for client in listDentalClients:
				self.ClientsMap[client.id()] = client

	def __len__(self):
		return len(self.ClientsMap)

	def AppendActByInstanceToDoctorByID(self, iDoctorID, dentalActInstance):
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is not None:
			doctor.AppendActByDetails(dentalActInstance.Date, 
									  dentalActInstance.PatientName, 
									  dentalActInstance.Type, 
									  dentalActInstance.Qty)
		return 0
	
	def AppendPaymentByInstanceToDoctorByID(self, iDoctorID, dentalPaymentInstance):
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is not None:
			doctor.AppendPaymentByDetails(	dentalPaymentInstance.Date, 
									  		dentalPaymentInstance.Sum)
		return 0
	
	def RemovePaymentByIndexByDoctorID(self, iDoctorID, iIndex):
		doctor = self.GetDoctorFromID(iDoctorID)
		doctor.RemovePaymentByIndex(iIndex)
		return 0
	
	def RemoveActByIndexByDoctorID(self, iDoctorID, iIndex):
		doctor = self.GetDoctorFromID(iDoctorID)
		doctor.RemoveActByIndex(iIndex)
		return 0
	
	def RemoveDoctorByID(self, iDoctorID):
		if not iDoctorID in self.ClientsMap: 
			return 0
		del self.ClientsMap[iDoctorID]
		return 0

	def GetDoctorFromID(self, iID):
		""" returns a DentalClient instance """
		if iID not in self.ClientsMap: 
			print "DentalDatabase::GetDoctorFromID: Requested doctor ID not found in database"
			return None 
		return self.ClientsMap[iID]

	def AddDoctorByDetails(self, sFname, sLname, sPhone, sAddress = "", sEmail=""):
		newdoctor = DentalClient(sFname, sLname, sPhone, sEmail, sAddress)
		newdoctor_id = newdoctor.id()
		if newdoctor_id in self.ClientsMap:
			print "Doctor is exists already in the database"
			return 0
		else: 
			self.ClientsMap[newdoctor_id] = newdoctor
			return newdoctor_id

	def AddDoctorByInstance(self, dentalClientInstance):
		newdoctor = DentalClient(dentalClientInstance.Firstname,
								 dentalClientInstance.Lastname, 
								 dentalClientInstance.Phone,
								 dentalClientInstance.Email,
								 dentalClientInstance.Address)
		newdoctor.SetDoctorPrices(dentalClientInstance.GetDoctorPrices())
		newdoctor_id = newdoctor.id()
		if newdoctor_id in self.ClientsMap:
			print "Doctor is exists already in the database"
			return -1
		else: 
			self.ClientsMap[newdoctor_id] = newdoctor
			return newdoctor_id
	#TODO
	# def MirrorActsFromDoctor1ToDoctor2(self, dentalClient1, dentalClient2):
	# 	return 0

	def AppendActsFromDoctor1ToDoctor2(self, dentalClient1, dentalClient2):
		id1 = dentalClient1.id()
		id2 = dentalClient2.id()
		sMsg = "AppendActsFromDoctor1ToDoctor2 (Error):\n"
		if not id1 in self.ClientsMap: 
			sMsg += "the SOURCE dental client instance is not the database"
			print sMsg
			return 0
		if not id2 in self.ClientsMap: 
			sMsg += "the DESTINATION dental client instance is not the database"
			print sMsg
			return 0

		dentalClient2.acts.extend(list(dentalClient1.acts))
		# for jAct in lacts:
			# self.AppendActByInstanceToDoctorByID(id2, jAct)
		return 0

	def GetNbDoctors(self):
		return len(self.ClientsMap)

	def GetListDoctors(self):
		""" returns a list of DentalClient instances """
		return self.ClientsMap.values()

	def GetListActsByDoctorID(self, iDoctorID):
		""" returns a list of DentalAct instances """
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is None:
			return []
		else: 
			return doctor.acts

	def GetListPaymentsByDoctorID(self, iDoctorID):
		""" returns a list of DentalPayment instances """
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is None:
			return []
		else: 
			return doctor.payments

	def GetListActsByDoctorIdByDate(self, iDoctorID, sMonth, sYear):
		""" returns a list of DentalAct instances for a given date (month and year) """
		lacts = self.GetListActsByDoctorID(iDoctorID)
		newlacts = list()
		for jAct in lacts:
			if jAct.GetMonth() != sMonth: continue
			if jAct.GetYear() != sYear: continue
			newlacts.append(jAct)
		return  newlacts

	def GetListPaymentsByDoctorIdByDate(self, iDoctorID, sMonth, sYear):
		""" returns a list of DentalPayment instances for a given date (month and year) """
		lpayments = self.GetListPaymentsByDoctorID(iDoctorID)
		newlpayments = list()
		for jPayment in lpayments:
			if jPayment.GetMonth() != sMonth: continue
			if jPayment.GetYear() != sYear: continue
			newlpayments.append(jPayment)
		return  newlpayments

	def GetNbActsByDoctorID(self, iDoctorID):
		return len(self.GetListActsByDoctorID(iDoctorID))

	def GetNbPaymentsByDoctorID(self, iDoctorID):
		return len(self.GetListPaymentsByDoctorID(iDoctorID))

	def GetDoctorPricesByDoctorID(self, iDoctorID):
		""" returns a dictionary of acts and their 
		default unit prices for a given doctor """
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is None: return 0
		return doctor.GetDoctorPrices()


	def SetDoctorPricesByDoctorID(self, iDoctorID, dictOfDefaultPrices):
		""" returns a dict """
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is None: return 0
		doctor.SetDoctorPrices(dictOfDefaultPrices)
		return 0

	def EditDoctorInformationByID(self, iDoctorID, newDentalClient):
		doctor = self.GetDoctorFromID(iDoctorID)
		oldID = iDoctorID
		newID = newDentalClient.id()
		if doctor is None: return 0
		bUpdateDatabaseMap = False
		
		if doctor.Firstname != newDentalClient.Firstname:
			bUpdateDatabaseMap = True
			doctor.SetVarFirstname(newDentalClient.Firstname)

		if doctor.Lastname != newDentalClient.Lastname:
			bUpdateDatabaseMap = True
			doctor.SetVarLastname(newDentalClient.Lastname)

		if doctor.Phone != newDentalClient.Phone:
			bUpdateDatabaseMap = True
			doctor.SetVarPhone(newDentalClient.Phone)

		doctor.SetVarEmail(newDentalClient.Email)
		doctor.SetVarAddress(newDentalClient.Address)
		
		if bUpdateDatabaseMap:
			self.ClientsMap[newID] = self.ClientsMap.pop(oldID)
			# print "DEBUG: oldID ({0}) has been replaced by newID ({1})".format(oldID, newID)

		return 0

instance_of_dental_database = DentalDatabase()
TYPE_DENTAL_DATABASE = type(instance_of_dental_database)

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

if __name__ == '__main__':

	def test():
		
		DB_DEFAULTPRICES = "res/DefaultPrices2017.dat"
		
		defaultprices = dict()
		defaultprices["CERAMIC"]= 13.5
		defaultprices["CCM"]= 13.5
		defaultprices["FM"]= 11.6
		defaultprices["FULL-DENTURE"]= 120

		pkl_save(defaultprices, DB_DEFAULTPRICES)
		return 0

	def test2():
		DB_CLIENTS_AND_ACTS = "res/Database2017.dat"
		
		defaultprices = dict()
		defaultprices["CERAMIC"]= 13.5
		defaultprices["CCM"]= 13.5
		defaultprices["FM"]= 11.6
		defaultprices["FULL-DENTURE"]= 120

		MyDatabase = DentalDatabase()
		
		id1 = MyDatabase.AddDoctorByDetails("Samir", "Kassir", "03789366")
		id2 = MyDatabase.AddDoctorByDetails("Khalil", "Gebran", "71555444")
		id3 = MyDatabase.AddDoctorByDetails("Alaa", "Zalzali", "70885146")

		MyDatabase.SetDoctorPricesByDoctorID(id1, defaultprices)
		MyDatabase.SetDoctorPricesByDoctorID(id2, defaultprices)
		MyDatabase.SetDoctorPricesByDoctorID(id3, defaultprices)
		 
		MyDatabase.AppendActByInstanceToDoctorByID(id1, DentalAct("05/02/2015", "Sahar K.", "CERAMIC", 2))
		MyDatabase.AppendActByInstanceToDoctorByID(id1, DentalAct("25/03/2015", "Ali M.","FULL-DENTURE", 10))
		MyDatabase.AppendActByInstanceToDoctorByID(id1, DentalAct("25/01/2017", "Sahar K.","CCM", 10))
		MyDatabase.AppendActByInstanceToDoctorByID(id1, DentalAct("30/01/2017", "Sahar K.","FULL-DENTURE", 10))
		MyDatabase.AppendActByInstanceToDoctorByID(id2, DentalAct("01/01/2016", "Rabih A.", "CERAMIC", 1))
		MyDatabase.AppendActByInstanceToDoctorByID(id3, DentalAct("08/12/2016", "Lilia K.", "FULL-DENTURE", 4))
		MyDatabase.AppendActByInstanceToDoctorByID(id3, DentalAct("20/01/2017", "Tanjara S.", "CERAMIC", 1))
		MyDatabase.AppendActByInstanceToDoctorByID(id3, DentalAct("22/12/2016", "Esaaf R.", "CCM", 6))
		MyDatabase.AppendActByInstanceToDoctorByID(id3, DentalAct("22/12/2016", "Elham U.", "FM", 6))
		MyDatabase.AppendActByInstanceToDoctorByID(id3, DentalAct("28/01/2017", "Samar K.", "FULL-DENTURE", 6))

		MyDatabase.AppendPaymentByInstanceToDoctorByID(id1, DentalPayment("05/02/2015", 150.0))
		MyDatabase.AppendPaymentByInstanceToDoctorByID(id1, DentalPayment("06/02/2016", 250.0))
		MyDatabase.AppendPaymentByInstanceToDoctorByID(id1, DentalPayment("06/07/2017", 450.0))
		MyDatabase.AppendPaymentByInstanceToDoctorByID(id2, DentalPayment("23/01/2017", 220.0))
		MyDatabase.AppendPaymentByInstanceToDoctorByID(id3, DentalPayment("16/01/2017", 113.0))
		 
		pkl_save(MyDatabase  , DB_CLIENTS_AND_ACTS)

		ParsedDatabase =  pickle.load( open( DB_CLIENTS_AND_ACTS , "rb" ) )
		print "len(ParsedDatabase)", len(ParsedDatabase)
		print "Nb parsed doctors", ParsedDatabase.GetNbDoctors()

		list_doctors = ParsedDatabase.GetListDoctors()
		for doctor in list_doctors:
			print "Doctor name", doctor.GetFullName()

	test()
	test2()

	