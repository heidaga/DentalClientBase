import cPickle as pickle
import os
from DentalClientBaseToolkit import HashClientID

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
		self.Paid = 0

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

		assert fname != ""
		assert sname != ""
		assert sphone != ""

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
		defaultprices["Ceramo-ceramique"]= 13.5
		defaultprices["Ceramo-metallic"]= 11.6
		defaultprices["Metal pur"]= 120
		pkl_save(defaultprices, DB_DEFAULTPRICES)
		return 0

	def test2():
		DB_CLIENTS_AND_ACTS = "res/Database2017.dat"
		
		MyDatabase = DentalDatabase()
		
		id1 = MyDatabase.AddDoctor("Samir", "Kassir", "0378936")
		id2 = MyDatabase.AddDoctor("Khalil", "Gebran", "71555444")
		id3 = MyDatabase.AddDoctor("Alaa", "Zalzali", "70885146")
		 
		MyDatabase.AppendActByDetailsToDoctorByID(id1, "05022015", "Ceramic", 2, 10)
		MyDatabase.AppendActByDetailsToDoctorByID(id1, "25032015", "Metal", 10, 6.5)
		MyDatabase.AppendActByDetailsToDoctorByID(id2, "01112016", "Ceramic", 1, 12)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "08122016", "Pont", 4, 37)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "20122016", "Ceramo-ceramique", 1, 50)
		MyDatabase.AppendActByDetailsToDoctorByID(id3, "22122016", "Metal-Metal", 6, 10)
		 
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


	# test()
	test2()
	# test3()

	