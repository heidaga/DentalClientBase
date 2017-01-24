# http://stackoverflow.com/questions/18596410/importerror-no-module-named-mpl-toolkits-with-maptlotlib-1-3-0-and-py2exe
# http://www.py2exe.org/index.cgi/DealingWithWarnings
from distutils.core import setup
import py2exe
import sys
import matplotlib
import os
import glob
import re

# -----------------------------------
# Package dependencies and versions
# -----------------------------------
# from  numpy import __version__ as NUMPY_VERSION_STR
# from  matplotlib import __version__ as MPL_VERSION_STR
# from  scipy import __version__ as SCIPY_VERSION_STR
# from  py2exe import __version__ as PY2EXE_VERSION_STR
# from PyQt4.Qt import PYQT_VERSION_STR
# from sip import SIP_VERSION_STR
# from PyQt4.QtCore import QT_VERSION_STR

# assert(NUMPY_VERSION_STR == "1.9.0")
# assert(MPL_VERSION_STR == "1.5.1")
# assert(SCIPY_VERSION_STR == "0.15.1")
# assert(PY2EXE_VERSION_STR == "0.6.9")
# assert(PYQT_VERSION_STR == "4.11.3")
# assert(SIP_VERSION_STR == "4.16.4")
# assert(QT_VERSION_STR == "4.8.6")

# Additional DLLs
# Intel compiler dlls related to blas 
# C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_2016.3.207\windows\redist\ia32_win\compiler
## libifcoremd.dll 
## libiomp5md.dll 
## libmmd.dll 

from DentalClientBaseSettings import APP_RESOURCES
verbose = False
py_source_name =  'DentalClientBaseGUI.py'
resource_folder = APP_RESOURCES
app_logo = "logonew.ico"
app_logo_path = os.path.join(APP_RESOURCES, app_logo)

sys.argv.append('py2exe')

def main():    
    res_files = find_data_files("res", "res", ["*.*"])
    invoice_files=find_data_files("invoice", "invoice", ["*.*"])
    # sample_files = find_data_files("samples", "samples", ["*.*"])
    # mplfiles = matplotlib.get_py2exe_datafiles()
    # pyqt_files=[('imageformats',[  
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qjpeg4.dll',
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qgif4.dll',
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qico4.dll',
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qmng4.dll',
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qsvg4.dll',
    #                                 'C:\\Python27/Lib/site-packages/PyQt4/plugins/imageformats/qtiff4.dll'
    #                             ])]


    opts = {
        'py2exe': {

                    "bundle_files" : 3,
                    "compressed" : True,
                   # "includes" : [ "mainwindow_rc", "matplotlib.backends",  
                   #              "matplotlib.backends.backend_qt4agg",
                   #              "pylab", "numpy", "scipy.sparse.csgraph._validation", 
                   #              "scipy.special._ufuncs_cxx", "scipy.integrate" ,  
                   #              "numpy.core.multiarray",
                   #              "matplotlib.backends.backend_tkagg"
                   #              ],
                   #  'excludes': ['_gtkagg', '_tkagg', '_agg2', 
                   #              '_cairo', '_cocoaagg',
                   #              '_fltkagg', '_gtk', '_gtkcairo', ],
                    'dll_excludes': [	'libgdk-win32-2.0-0.dll',
                               			'libgobject-2.0-0.dll',
                               			'w9xpopen.exe',
                               			'numpy-atlas.dll', # after upgrading numpy from 1.9 to 1.11
                               			'MSVCP90.dll']
                  }
           }

    code = setup(
                windows=[{
		                    'script': py_source_name,
		                    'icon_resources':[(1, app_logo_path)],
		                    # 'bitmap_resources ':bitmap_resources,
		                    # other_resources = [get_manifest_resource("Your app name")],
		                    "dest_base" : "DentalClientBase",   #exe name
		                    "copyright" : "Copyright (c) 2017 Ali Saad",
		                    "company_name" : "Ali Saad Developments",
		                    "version" : "".join(grep('__version__',py_source_name).split()),
		                    "Name" : "Dental Client Base", # name in properties
                }],
                zipfile=None,
                options=opts, 
                data_files =res_files+invoice_files)

    return code




### ******* convenience functions ********

# Grep-like function to catch version from setup.py (it should be done the opposite way)
# version finding from source : http://stackoverflow.com/a/40263000/2192115
def grep(attrname, fname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval = ""
    with open(fname, 'r') as myfile:
        file_text = myfile.read()
        file_text.replace("\n"," ")
        strval,  = re.findall(pattern, file_text)
    return strval


def find_data_files(source,target,patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source,pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target,os.path.relpath(filename,source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path,[]).append(filename)
    return sorted(ret.items())



if __name__ == "__main__":

    print(">>> [0%] Building ... please wait")
    
    if verbose:
    	code = main()
    else:
	    # http://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto
	    old_stdout = sys.stdout
	    sys.stdout = open(os.devnull, "w")
	    try:
	        code = main()
	    finally:
	        sys.stdout.close()
	        sys.stdout = old_stdout

    if code is None:
    	print(">>> [xx%] Errors found ... check you configuration")
    else:
    	print(">>> [100%] Binary building complete in the 'dist' directory")