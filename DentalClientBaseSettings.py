import os

#########################
# GENERAL SETTINGS
#########################
APP_NAME = "Dental Client Database"
APP_LICENSE = "(Licensed for Mr. Hussein FTOUNI)"
APP_RESOURCES_FOLDER = "res"
APP_SETTINGS_FILE = "settings.ini"
APP_LOGO_NAME = "logonew_tr.png"
APP_BANNER_NAME = "banner_tr.png"

APP_SETTINGS_COLOR_TABLE ="""
QTableView 
{ 
	/*selection-background-color: #e6ecff; */
	selection-background-color: qlineargradient(x1: 0, y1: 0.0, x2: 0.9, y2: 0.9,
                                stop: 0 #9999ff, stop: 1 white);
	selection-color: black; 
}

QMainWindow::separator {
    background: yellow;
    width: 10px; /* when vertical */
    height: 10px; /* when horizontal */
}

QMainWindow::separator:hover {
    background: red;
}

QPushButton:default {
    border-color: navy; /* make the default button prominent */
}
"""

APP_SETTINGS_FONT = "MS Shell Dlg 2" 
APP_SETTINGS_FONTSIZE = 12

#########################
# TABLE- DOCTORS
#########################
APP_SETTINGS_TABLE_DOCTORS_FONT =  APP_SETTINGS_FONT
APP_SETTINGS_TABLE_DOCTORS_FONTSIZE = 12 

# Column indices - enum style
COL_DRFIRSTNAME     = 0
COL_DRLASTNAME      = 1
COL_DRPHONE         = 2

# Phone number format
APP_SETTINGS_PHONE_OPTION1 = "{0} - {1} {2}"
APP_SETTINGS_PHONE_OPTION2 = "{0} - {1} {2} {3}"
APP_SETTINGS_PHONE_FORMAT = APP_SETTINGS_PHONE_OPTION1

#########################
# TABLE- ACTS
#########################
APP_SETTINGS_TABLE_ACTS_FONT = "Courier New" 
APP_SETTINGS_TABLE_ACTS_FONTSIZE = 10

# Column indices - enum style
COL_ACTDATE         = 0
COL_ACTTYPE         = 1
COL_ACTUNITPRICE    = 3
COL_ACTQTY          = 4
COL_ACTSUBTOTAL     = 5
COL_ACTPATIENT      = 2 
COL_ACTPAID         = 6 

# Date format for each act
# APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MMMM/yyyy"  #  01/January/2000
# APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MMM/yyyy"	#  01/Jan/2000
APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MM/yyyy"		#  01/01/2000

#########################
# TABLE- DEFAULT ACTS
#########################
APP_SETTINGS_TABLE_DEFAULTACTS_FONT = "MS Shell Dlg 2" 
APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE = 10 

#########################
# ICONS
#########################
APP_SETTINGS_SCALED_ICONS_RESOLUTION = 100 # pixel


#########################
# INVOICE
#########################
INVOICE_FLOAT_FORMAT = '.2f'




###############################################
# ADDITIONAL SETTINGS NON USER MODIFIABLE
###############################################

APP_DIR = os.getcwd()
APP_RESOURCES = os.path.join(APP_DIR, APP_RESOURCES_FOLDER)
APP_SETTINGS = os.path.join(APP_RESOURCES, APP_SETTINGS_FILE)
APP_LOGO_PATH = os.path.join(APP_RESOURCES, APP_LOGO_NAME)
APP_BANNER_PATH = os.path.join(APP_RESOURCES, APP_BANNER_NAME)


ACTS_HEADER_DICT = dict() 
ACTS_HEADER_DICT[COL_ACTDATE] = 'Date'
ACTS_HEADER_DICT[COL_ACTTYPE] = 'Act type'
ACTS_HEADER_DICT[COL_ACTUNITPRICE] = 'Unit Price'
ACTS_HEADER_DICT[COL_ACTQTY] = 'Quantity'
ACTS_HEADER_DICT[COL_ACTSUBTOTAL] = 'SubTotal'
ACTS_HEADER_DICT[COL_ACTPATIENT] = 'Patient Name'
