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

	def __init__(self, sDate, sType= "", iQty = 0, fUnitPrice = 0.0):
		# self.Firstname = fname
		# self.Surname = sname
		# ObjClient is instance of DentalClient
		
		# self.client = ObjClient # no need anymore coz instanciated as part of DentalClient
		self.Date = sDate
		self.Type = sType
		self.Qty = iQty
		self.UnitPrice = fUnitPrice
		self.SubTotal = self.Qty  * self.UnitPrice
		self.Paid = 0

	def __len__(self):
		""" returns number of member variables to be used externally (by Qt) """
		return 6

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

	def SetVarType(self, sType, fDefaultUnitPrice = None):
		self.Type = str(sType)
		if fDefaultUnitPrice is not None:
			self.SetVarUnitPrice(fDefaultUnitPrice)
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
		elif iCol == COL_ACTPAID: 
			return self.Paid
		else: raise IndexError("Index used in __getitem__ is not supported")


# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

class DentalClient:
	def __init__(self, fname, sname, sphone , email = "", address = ""):
		self.Firstname = fname   	# string required
		self.Surname = sname 		# string required
		self.Phone = sphone			# string required

		self.Email = email 			# string optional
		self.Address = address 		# string optional

		self.acts = list()
		self.defaultprices = dict()

	def __len__(self):
		""" returns number of member variables to be used externally (by Qt) """
		return 3

	def AppendActByDetails(self, sDate, sType, iQty, fUnitPrice):
		cNewAct = DentalAct(sDate, sType, iQty, fUnitPrice)
		self.acts.append(cNewAct)
		
	def AppendActByInstance(self, cNewAct):
		if cNewAct is None: 
			raise Exception("AddActToDoctor:: dentalAct is None")
			return 0
		else:
			self.acts.append(cNewAct)
		return 0

	def id(self):
		# return sha1(self.Firstname+self.Surname+self.Phone)
		return HashClientID(self.Firstname,self.Surname,self.Phone)

	def GetFullName(self):
		return self.Firstname + " " + self.Surname

	def SetVarFirstname(self, sVal):
		self.Firstname = str(sVal)

	def SetVarLastname(self, sVal):
		self.Surname = str(sVal)

	def SetVarPhone(self, sVal):
		self.Phone = str(sVal)

	""" 
		ONLY FOR SORTING : acts as a getter 
		To sort dates, i only return the date string
		then the output value is Qt-formatted in the GUI class 
	"""

	def AssignDoctorPrices(self, dictOfDefaultPrices):
		self.defaultprices = dict(dictOfDefaultPrices)
		return

	def __getitem__(self, iCol):
		if iCol == COL_DRFIRSTNAME: 
			return self.Firstname
		elif iCol == COL_DRLASTNAME: 
			return self.Surname
		elif iCol == COL_DRPHONE: 
			return self.Phone
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

	def AppendActByDetailsToDoctorByID(self, iDoctorID,  sDate, sType, iQty, fUnitPrice):
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is not None:
			doctor.AppendActByDetails(sDate, sType, iQty, fUnitPrice)
		return 0

	def AppendActByInstanceToDoctorByID(self, iDoctorID, dentalAct):
		doctor = self.GetDoctorFromID(iDoctorID)
		if doctor is not None:
			doctor.AppendActByDetails(sDate, sType, iQty, fUnitPrice)
		return 0

	def GetDoctorFromID(self, iID):
		""" returns a DentalClient instance """
		if iID not in self.ClientsMap: 
			print "DentalDatabase::GetDoctorFromID: Requested doctor ID not found in database"
			return None 
		return self.ClientsMap[iID]

	def AddDoctor(self, sFname, sLname, sPhone):
		newdoctor = DentalClient(sFname, sLname, sPhone)
		newdoctor_id = newdoctor.id()
		if newdoctor_id in self.ClientsMap:
			print "Doctor is exists already in the database"
			return 0
		else: 
			self.ClientsMap[newdoctor_id] = newdoctor
			return newdoctor_id

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


instance_of_dental_database = DentalDatabase()
TYPE_DENTAL_DATABASE = type(instance_of_dental_database)

# ***********************************************************************
# ***********************************************************************
# ***********************************************************************

if __name__ == '__main__':

	def test():
		
		DB_DEFAULTPRICES = "test_defaultprices.pkl"
		
		defaultprices = dict()
		defaultprices["CERAMIC"]= 13.5
		defaultprices["CCM"]= 13.5
		defaultprices["FM"]= 11.6
		defaultprices["FULL-DENTURE"]= 120

		pkl_save(defaultprices, DB_DEFAULTPRICES)
		return 0

	def test2():
		DB_CLIENTS_AND_ACTS = "res/Database2017.dat"
		
		MyDatabase = DentalDatabase()
		
		id1 = MyDatabase.AddDoctor("Samir", "Kassir", "03 - 789 366")
		id2 = MyDatabase.AddDoctor("Khalil", "Gebran", "71 - 555 444")
		id3 = MyDatabase.AddDoctor("Alaa", "Zalzali", "70 - 885 146")
		 
		MyDatabase.AppendActByDetailsToDoctorByID(id1, "05/02/2015", "CERAMIC", 2, 10)
		MyDatabase.AppendActByDetailsToDoctorByID(id1, "25/03/2015", "FULL-DENTURE", 10, 6.5)
		MyDatabase.AppendActByDetailsToDoctorByID(id1, "25/03/2015", "CCM", 10, 6.5)
		MyDatabase.AppendActByDetailsToDoctorByID(id2, "01/11/2016", "CERAMIC", 1, 12)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "08/12/2016", "FULL-DENTURE", 4, 37)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "20/12/2016", "CERAMIC", 1, 50)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "22/12/2016", "CCM", 6, 10)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "22/12/2016", "FM", 6, 10)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "28/12/2016", "FULL-DENTURE", 6, 10)
		 
		pkl_save(MyDatabase  , DB_CLIENTS_AND_ACTS)

		ParsedDatabase =  pickle.load( open( DB_CLIENTS_AND_ACTS , "rb" ) )
		print "len(ParsedDatabase)", len(ParsedDatabase)
		print "Nb parsed doctors", ParsedDatabase.GetNbDoctors()

		list_doctors = ParsedDatabase.GetListDoctors()
		for doctor in list_doctors:
			print "Dr.", doctor.GetFullName()


	def test3():
		# with open(r"C:\Users\RASPI\Desktop\Misc_coding\clientdatabase-tableview\res\DefaultPricesoooo.dat", 'r') as fo:
			# print "opening file 1 succeeded"
		with open(r"C:\Users\RASPI\Desktop\Misc_coding\clientdatabase-tableview\res\DefaultPrices.dat", 'r') as fo:
			print "opening file 2 succeeded"


	test()
	test2()
	# test3()

	