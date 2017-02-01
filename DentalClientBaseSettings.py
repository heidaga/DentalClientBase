import os

#########################
# GENERAL SETTINGS
#########################
# VERSION=      MAJOR_VERSION . MINOR_VERSION  . IMPROVEMENT_FEATURE . BUG_CORRECTION
__version__ =  '      0       .       11       .           3         .         2      '

APP_NAME = "Dental Client Database"
APP_LICENSE = "(Licensed for Mr. Hussein FTOUNI)"
APP_RESOURCES_FOLDER = "res"
APP_INVOICE_EXPORT_FOLDER = "invoice_exports"
APP_SETTINGS_FILE = "settings.ini"
APP_LOGO_PNG_NAME = "logonew.png"
APP_LOGO_ICO_NAME = "logonew.ico"
APP_BANNER_NAME = "banner.png"
APP_MAIN_SCRIPT = 'DentalClientBaseGUI.py'

# selection-background-color: qlineargradient(x1: 0, y1: 0.0, x2: 0.9, y2: 0.9,
                                # stop: 0 #9999ff, stop: 1 white);
APP_SETTINGS_COLOR_TABLE ="""
QTableView 
{ 
	selection-background-color: #e6ecff;
	/* selection-background-color: qlineargradient(x1: 0, y1: 0.0, x2: 0.9, y2: 0.9,
                                stop: 0 #9999ff, stop: 1 white);*/
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

# this string will be url-encoded so it shouldnt contain any pre encoded character
APP_SETTINGS_REPORTING = r"mailto:alisaad05@gmail.com?subject=DentalClientBase_v{0}_issue&body=Issue Description:".format("".join(__version__).split())

#########################
# TABLE- DOCTORS
#########################
APP_SETTINGS_TABLE_DOCTORS_FONT =  APP_SETTINGS_FONT
APP_SETTINGS_TABLE_DOCTORS_FONTSIZE = 10 

# Column indices - enum style
COL_DRFIRSTNAME     = 0
COL_DRLASTNAME      = 1
COL_DRPHONE         = 2

# Phone number format
# warning: unformatting phone numbers is based on "-" only for now
# option1: 01 - 631 714
APP_SETTINGS_PHONE_OPTION1 = "{0} - {1} {2}" 
# option2: 01 - 63 17 14
APP_SETTINGS_PHONE_OPTION2 = "{0} - {1} {2} {3}"
# Default option
APP_SETTINGS_PHONE_FORMAT = APP_SETTINGS_PHONE_OPTION1

DOCTOR_TABLE_COLUMNSIZE_FIRSTNAME = 0.6  # 100
DOCTOR_TABLE_COLUMNSIZE_LASTNAME  = 0.6  # 100
DOCTOR_TABLE_COLUMNSIZE_PHONE     = 0.6  # 100

#########################
# TABLE- ACTS
#########################
APP_SETTINGS_TABLE_ACTS_FONT = "MS Shell Dlg 2" #"Courier New" 
APP_SETTINGS_TABLE_ACTS_FONTSIZE = 10

# Column indices - enum style
COL_ACTDATE         = 0
COL_ACTPATIENT      = 1 
COL_ACTTYPE         = 2
COL_ACTUNITPRICE    = 3
COL_ACTQTY          = 4
COL_ACTSUBTOTAL     = 5
COL_ACTNOTES        = 6 

COL_ACTPAID         = 7 

# Date format for each act
# APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MMMM/yyyy"  #  01/January/2000
# APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MMM/yyyy"	#  01/Jan/2000
APP_SETTINGS_ACTDATE_FORMAT_DISPLAY = "dd/MM/yyyy"		#  01/01/2000

# Column size
ACT_TABLE_COLUMNSIZE_DATE 		= 0.15 # 200
ACT_TABLE_COLUMNSIZE_TYPE 		= 0.15 # 200
ACT_TABLE_COLUMNSIZE_PATIENT 	= 0.15 # 200
ACT_TABLE_COLUMNSIZE_NOTES 		= 0.35 # 400
ACT_TABLE_COLUMNSIZE_UNITPRICE 	= 0.1  # 100
ACT_TABLE_COLUMNSIZE_QTY 		= 0.1  # 100
ACT_TABLE_COLUMNSIZE_TOTAL 		= 0.1  # 100


#########################
# TABLE- PAYMENTS
#########################
APP_SETTINGS_TABLE_PAYMENTS_FONT = "MS Shell Dlg 2" #"Courier New" 
APP_SETTINGS_TABLE_PAYMENTS_FONTSIZE = 10

# Column indices - enum style
COL_PAYMENTDATE     = 0
COL_PAYMENTSUM      = 1 

PAYMENT_TABLE_COLUMNSIZE_DATE   = 0.5 # 100
PAYMENT_TABLE_COLUMNSIZE_SUM    = 0.5 # 100


#########################
# TABLE- DEFAULT ACTS
#########################
APP_SETTINGS_TABLE_DEFAULTACTS_FONT = "MS Shell Dlg 2" 
APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE = 8 


#########################
# ICONS
#########################
APP_SETTINGS_SCALED_ICONS_RESOLUTION = 128 # pixel


#########################
# INVOICE
#########################
INVOICE_FLOAT_FORMAT = '.2f'
HEADERS_TO_EXCLUDE_FROM_INVOICE = [ COL_ACTNOTES ]



#########################
# OTHER SETTINGS/SWITCHES
#########################

BOOLSETTING_Initialize_Columnsize_On_Client_Activation = True
BOOLSETTING_Confirm_before_exit_application = True
BOOLSETTING_Confirm_before_delete_doctor_via_remove_button = True
BOOLSETTING_Confirm_before_delete_act_via_remove_button = True
BOOLSETTING_Confirm_before_delete_payment_via_remove_button = True
BOOLSETTING_Preview_exported_invoice_in_Invoice_Viewer = False
BOOLSETTING_Preview_exported_invoice_in_internet_browser = True
BOOLSETTING_Convert_exported_invoice_to_pdf_without_preview = True
INTSETTING_Maximum_number_of_invoice_tabs_in_Invoice_Viewer = 5


###############################################
# ADDITIONAL SETTINGS NON USER MODIFIABLE
###############################################

APP_DIR = os.getcwd()
APP_RESOURCES = os.path.join(APP_DIR, APP_RESOURCES_FOLDER)
APP_SETTINGS = os.path.join(APP_RESOURCES, APP_SETTINGS_FILE)
APP_LOGO_PNG_PATH = os.path.join(APP_RESOURCES, APP_LOGO_PNG_NAME)
APP_LOGO_ICO_PATH = os.path.join(APP_RESOURCES, APP_LOGO_ICO_NAME)
APP_BANNER_PATH = os.path.join(APP_RESOURCES, APP_BANNER_NAME)
APP_INVOICE_RESOURCES_FOLDER = os.path.join(APP_RESOURCES, "invoice")
APP_INVOICE_EXPORT_DIR = os.path.join(APP_DIR, APP_INVOICE_EXPORT_FOLDER)


ACTS_HEADER_DICT = dict() 
ACTS_HEADER_DICT[COL_ACTDATE] = 'Date'
ACTS_HEADER_DICT[COL_ACTTYPE] = 'Act type'
ACTS_HEADER_DICT[COL_ACTNOTES] = 'Notes'
ACTS_HEADER_DICT[COL_ACTUNITPRICE] = 'Unit Price'
ACTS_HEADER_DICT[COL_ACTQTY] = 'Quantity'
ACTS_HEADER_DICT[COL_ACTSUBTOTAL] = 'SubTotal'
ACTS_HEADER_DICT[COL_ACTPATIENT] = 'Patient Name'
# ACTS_HEADER_DICT[COL_ACTPAID] = 'Paid' # not included

DOCTORS_HEADER_DICT = dict() 
DOCTORS_HEADER_DICT[COL_DRFIRSTNAME] = 'First Name'
DOCTORS_HEADER_DICT[COL_DRLASTNAME] = 'Last Name'
DOCTORS_HEADER_DICT[COL_DRPHONE] = 'Phone Number'

PAYMENTS_HEADER_DICT = dict() 
PAYMENTS_HEADER_DICT[COL_PAYMENTDATE] = 'Date'
PAYMENTS_HEADER_DICT[COL_PAYMENTSUM] = 'Received Sum'