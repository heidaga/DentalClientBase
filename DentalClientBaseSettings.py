import os

#########################
# GENERAL SETTINGS
#########################
APP_NAME = "Dental Client Database"
APP_LICENSE = "(Licensed for Mr. Hussein FTOUNI)"
APP_RESOURCES = "res"
APP_DIR = os.getcwd()
APP_SETTINGS = os.path.join(APP_DIR, APP_RESOURCES, "settings.ini")

APP_SETTINGS_COLOR_TABLE ="""
QTableView 
{ 
	selection-background-color: #800000FF; 
	selection-color: yellow; 
}
"""

#########################
# TABLE- DOCTORS
#########################
APP_SETTINGS_TABLE_DOCTORS_FONT = "MS Shell Dlg 2" 
APP_SETTINGS_TABLE_DOCTORS_FONTSIZE = 12 

# Column indices - enum style
COL_DRFIRSTNAME     = 0
COL_DRLASTNAME      = 1
COL_DRPHONE         = 2

#########################
# TABLE- ACTS
#########################
APP_SETTINGS_TABLE_ACTS_FONT = "Courier New" 
APP_SETTINGS_TABLE_ACTS_FONTSIZE = 12

# Column indices - enum style
COL_ACTDATE         = 0
COL_ACTTYPE         = 1
COL_ACTUNITPRICE    = 2
COL_ACTQTY          = 3
COL_ACTSUBTOTAL     = 4
COL_ACTPAID         = 5 

# If this option is on, user can load
# APP_SETTINGS_ALLOW_CUSTOM_ACTTYPE = False

#########################
# TABLE- DEFAULT ACTS
#########################
APP_SETTINGS_TABLE_DEFAULTACTS_FONT = "MS Shell Dlg 2" 
APP_SETTINGS_TABLE_DEFAULTACTS_FONTSIZE = 10 

#########################
# ICONS
#########################
APP_SETTINGS_SCALED_ICONS_RESOLUTION = 100 # pixel