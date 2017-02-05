"""
Resources:

https://github.com/NextStepWebs/simple-html-invoice-template
http://pbpython.com/pdf-reports.html

"""
from jinja2 import Environment, FileSystemLoader
# from weasyprint import HTML
import os
# import base64

from DentalClientBaseStructs import *
from DentalClientBaseToolkit import *
from DentalClientBaseSettings import *

# logoPath = os.path.join(APP_RESOURCES_FOLDER, "logo.png")
# logoHtmlSrc = os.path.join(APP_INVOICE_RESOURCES_FOLDER, "logo_src.txt")
# encoded_logo = base64.b64encode(open(APP_BANNER_PATH, "rb").read())
# with open(logoHtmlSrc, "w") as text_file:
#     text_file.write(encoded_logo)

def to_html_dentalActInstance(iID , dentalActInstance, mode = 1):
    Act = dentalActInstance
    s = str()
    if mode == 1:
        s+= "    <tr>\n"
    elif mode == 2:
        s+= "    <tr class=\"item\">\n"
    
    s+= "      <td>Act #{0}</td>\n".format(iID)
    
    for iHeader in ACTS_HEADER_DICT:
        if iHeader in HEADERS_TO_EXCLUDE_FROM_INVOICE: continue
        css_class = str()
        sval = str()
        if iHeader == COL_ACTDATE : css_class = " class=\"service\""
        if iHeader == COL_ACTTYPE : css_class = " class=\"desc\""
        if iHeader == COL_ACTUNITPRICE : css_class = " class=\"unit\""
        if iHeader == COL_ACTQTY : css_class = " class=\"qty\""
        if iHeader == COL_ACTSUBTOTAL : css_class = " class=\"total\""

        val = Act.__getitem__(iHeader)
        if iHeader in [COL_ACTUNITPRICE, COL_ACTSUBTOTAL]:
            sval = format(val, INVOICE_FLOAT_FORMAT)
            sval += " {0}".format(STRSETTING_Currency_symbol)
        else:
            sval = val 

        s+= "      <td{0}>{1}</td>\n".format(css_class, sval)

    return s

# modes 1/2 depend on which css using (check folders invoice and invoice2)
def to_html_actdetails(listOfDentalActInstances, mode = 1):
    s = str()
    for j, jAct in enumerate(listOfDentalActInstances):
        if jAct.SubTotal != 0:
            s += to_html_dentalActInstance(j+1, jAct, mode)
    return s

# modes 1/2 depend on which css using (check folders invoice and invoice2)
def to_html_actheaders(mode = 1):
    s = str()
    s+= "  <thead>\n"
    if mode == 1:
        s+= "    <tr style=\"text-align: right;\">\n"
    elif mode == 2:
        s+= "    <tr class=\"heading\">\n"
    s+= "      <th></th>\n"
    for iHeader in ACTS_HEADER_DICT:
        if iHeader in HEADERS_TO_EXCLUDE_FROM_INVOICE: continue
        s+= "      <th>{0}</th>\n".format(ACTS_HEADER_DICT[iHeader])
    s+= "    </tr>\n"
    s+= "  </thead>\n"
    return s

def to_html_acts_header_and_details(listOfDentalActInstances, mode = 1):
    s = str()
    s+= "<table>\n"
    s+= to_html_actheaders(mode)
    s+= "  <tbody>\n"
    s+= to_html_actdetails(listOfDentalActInstances, mode)
    s+= "  </tbody>\n"
    s+= "</table>\n"
    return s


def ExportInvoice(iInvoiceID, sMonth, sYear, dentalClient, listDentalActs, listDentalPayments):
    
    sActualDate = "01-{0}-{1}".format(sMonth, sYear)
    sDueDate = str()
    if sMonth == "12": sDueDate = "01-01-{0}".format(int(sYear)+1)
    else: 
        sDueMonth = str(int(sMonth)+1).zfill(2)
        sDueDate = "01-{0}-{1}".format(sDueMonth, sYear)


    css_style = 1
    act_headers_and_details = to_html_acts_header_and_details(listDentalActs, css_style)
    fPaid = 0.0
    fGrandTotal = 0.0
    for jPayment in listDentalPayments:
        fPaid += jPayment.Sum
    for jAct in listDentalActs:
        fGrandTotal += jAct.SubTotal

    sGrandTotal = format(fGrandTotal, INVOICE_FLOAT_FORMAT)
    sPaid = format(fPaid, INVOICE_FLOAT_FORMAT)
    sReported = format(fGrandTotal-fPaid, INVOICE_FLOAT_FORMAT)

    sGrandTotal += " {0}".format(STRSETTING_Currency_symbol)
    sPaid += " {0}".format(STRSETTING_Currency_symbol)
    sReported += " {0}".format(STRSETTING_Currency_symbol)

    # if logo hash function unchanged, store this value and re-use to save time
    # sEncodedLogo = base64.b64encode(open(APP_BANNER_PATH, "rb").read())

    sHtmlTemplatePath = "index_template.html"
    # sHtmlTemplatePath = os.path.join(APP_INVOICE_RESOURCES_FOLDER,"index_template.html") 
    sHtmlCSSPath = os.path.join(APP_INVOICE_RESOURCES_FOLDER, "style.css")

    env = Environment(loader=FileSystemLoader(APP_INVOICE_RESOURCES_FOLDER))
    template = env.get_template(sHtmlTemplatePath)
    template_vars = {
                     # "tag_logo" : sEncodedLogo,
                     "tag_user_notice" : "Nothing to mention",
                     "tag_invoice_id": iInvoiceID,
                     "tag_actual_date": sActualDate,
                     "tag_due_date": sDueDate,
                     "tag_doctor_full_name": dentalClient.GetFullName(),
                     "tag_doctor_address": dentalClient.Address,
                     "tag_doctor_email": dentalClient.Email,
                     "tag_payment_method": "Cash",
                     "tag_payment_identifier": "-",
                     "tag_acts_header_and_details": act_headers_and_details,
                     "tag_total_sum": sGrandTotal, 
                     "tag_total_paid": sPaid,
                     "tag_total_remaining": sReported,
                     }

    # Render our file and create the PDF using our css style file
    sHtmlContent = template.render(template_vars)

    sName = dentalClient.GetFullName()
    sNameNoSpace = sName.replace(" ", "_")
    sOutputFname = "invoice_{0}____{1}".format(iInvoiceID,sNameNoSpace)
    HtmlOutPath = os.path.join(APP_INVOICE_EXPORT_DIR,sOutputFname+".html") 

    with open(HtmlOutPath, "w") as text_file:
        text_file.write("{0}".format(sHtmlContent))

    PdfOutPath = os.path.join(APP_INVOICE_EXPORT_DIR,sOutputFname+".pdf") 
    # HTML(string=sHtmlContent).write_pdf(PdfOutPath, stylesheets=[sHtmlCSSPath])  

    return HtmlOutPath, PdfOutPath


if __name__ == "__main__":
    
    def test():
        DB_CLIENTS_AND_ACTS = "res/Database2017.dat"
        ParsedDatabase =  pickle.load( open( DB_CLIENTS_AND_ACTS , "rb" ) )
        list_doctors = ParsedDatabase.GetListDoctors()
        last_doctor = list_doctors[-1]
        list_of_acts = ParsedDatabase.GetListActsByDoctorID(last_doctor.id())
        list_of_payments = ParsedDatabase.GetListPaymentsByDoctorID(last_doctor.id())

        sPathToInvoiceHTML = str()
        sPathToInvoicePDF = str()
        sPathToInvoiceHTML , sPathToInvoicePDF  = ExportInvoice(56, "02" , "2016", last_doctor, list_of_acts, list_of_payments)

    test()

"""
Template tags

{{ tag_logo }}
{{ tag_user_notice }}
{{ tag_invoice_id }}
{{ tag_actual_date }}
{{ tag_due_date }}
{{ tag_doctor_full_name }}
{{ tag_doctor_address }}
{{ tag_doctor_email }}
{{ tag_payment_method }}
{{ tag_payment_identifier }}
{{ tag_act_header_list }}
{{ tag_act_details_list }}
{{ tag_acts_header_and_details }}
{{ tag_total_sum }}
{{ tag_total_paid }}
{{ tag_total_remaining }}

"""