"""
Resources:

https://github.com/NextStepWebs/simple-html-invoice-template
http://pbpython.com/pdf-reports.html

"""
# from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import pandas as pd
import os

from DentalClientBaseStructs import *
from DentalClientBaseToolkit import *
from DentalClientBaseSettings import *


def create_pivot(df, infile, index_list=["Manager", "Rep", "Product"], value_list=["Price", "Quantity"]):
    """
    Create a pivot table from a raw DataFrame and return it as a DataFrame
    """
    table = pd.pivot_table(df, index=index_list, values=value_list,
                           aggfunc=[np.sum, np.mean], fill_value=0)
    return table

def get_summary_stats(df,product):
    """
    For certain products we want National Summary level information on the reports
    Return a list of the average quantity and price
    """
    results = []
    results.append(df[df["Product"]==product]["Quantity"].mean())
    results.append(df[df["Product"]==product]["Price"].mean())
    return results

def test_main():
    parser = argparse.ArgumentParser(description='Generate PDF report')
    parser.add_argument('infile', type=argparse.FileType('r'),
    help="report source file in Excel")
    parser.add_argument('outfile', type=argparse.FileType('w'),
    help="output file in PDF")
    args = parser.parse_args()
    # Read in the file and get our pivot table summary
    df = pd.read_excel(args.infile.name)
    sales_report = create_pivot(df, args.infile.name)
    # Get some national summary to include as well
    manager_df = []
    for manager in sales_report.index.get_level_values(0).unique():
        manager_df.append([manager, sales_report.xs(manager, level=0).to_html()])
    # Do our templating now
    # We can specify any directory for the loader but for this example, use current directory
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("myreport.html")
    template_vars = {"title" : "National Sales Funnel Report",
                     "CPU" : get_summary_stats(df, "CPU"),
                     "Software": get_summary_stats(df, "Software"),
                     "national_pivot_table": sales_report.to_html(),
                     "Manager_Detail": manager_df}
    # Render our file and create the PDF using our css style file
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf(args.outfile.name,stylesheets=["style.css"])





# mimic to_html function used in pandas

def to_html_dentalActInstance(iID , dentalActInstance, mode = 1):
    Act = dentalActInstance
    s = str()
    if mode == 1:
        s+= "    <tr>\n"
    elif mode == 2:
        s+= "    <tr class=\"item\">\n"
    s+= "      <th>Act #{0}</th>\n".format(iID)
    s+= "      <td>{0}</td>\n".format(Act.__getitem__(COL_ACTDATE))
    s+= "      <td>{0}</td>\n".format(Act.__getitem__(COL_ACTTYPE))
    s+= "      <td>{0}</td>\n".format(Act.__getitem__(COL_ACTUNITPRICE))
    s+= "      <td>{0}</td>\n".format(Act.__getitem__(COL_ACTQTY))
    s+= "      <td>{0}</td>\n".format(Act.__getitem__(COL_ACTSUBTOTAL))
    s+= "    </tr>\n"
    return s

# modes 1/2 depend on which css using (check folders invoice and invoice2)
def to_html_actdetails(listOfDentalActInstances, mode = 1):
    s = str()
    for j, actj in enumerate(listOfDentalActInstances):
        s+= to_html_dentalActInstance(j+1, actj, mode)
    return s

# modes 1/2 depend on which css using (check folders invoice and invoice2)
def to_html_actheaders(sHeaderList, mode = 1):
    s = str()
    s+= "  <thead>\n"
    if mode == 1:
        s+= "    <tr style=\"text-align: right;\">\n"
    elif mode == 2:
        s+= "    <tr class=\"heading\">\n"
    s+= "      <th></th>\n"
    for sHeader in sHeaderList:
        s+= "      <th>{0}</th>\n".format(sHeader)
    s+= "    </tr>\n"
    s+= "  </thead>\n"
    return s

def to_html_acts_header_and_details(sHeaderList, listOfDentalActInstances, mode = 1):
    s = str()
    s+= "<table border=\"1\" class=\"dataframe\">\n"
    s+= to_html_actheaders(sHeaderList, mode)
    s+= "  <tbody>\n"
    s+= to_html_actdetails(listOfDentalActInstances, mode)
    s+= "  </tbody>\n"
    s+= "</table>\n"
    return s
    
 

if __name__ == "__main__":
    
    def test():
        DB_CLIENTS_AND_ACTS = "res/Database2017.dat"
        
        ParsedDatabase =  pickle.load( open( DB_CLIENTS_AND_ACTS , "rb" ) )
        print "len(ParsedDatabase)", len(ParsedDatabase)
        print "Nb parsed doctors", ParsedDatabase.GetNbDoctors()

        list_doctors = ParsedDatabase.GetListDoctors()
        for doctor in list_doctors:
            print "Dr.", doctor.GetFullName()

        last_doctor = list_doctors[-1]
        list_of_acts = ParsedDatabase.GetListActsByDoctorID(last_doctor.id())
        fPaid = 100
        fGrandTotal = 0.0
        for jAct in list_of_acts:
            fGrandTotal += jAct.SubTotal

        headerColumns = dict() 
        headerColumns[COL_ACTDATE] = 'Date'
        headerColumns[COL_ACTTYPE] = 'Act type'
        headerColumns[COL_ACTUNITPRICE] = 'Unit Price'
        headerColumns[COL_ACTQTY] = 'Quantity'
        headerColumns[COL_ACTSUBTOTAL] = 'SubTotal'
        sHeaderList = headerColumns.values()

        # test the output on:
        # http://htmledit.squarefree.com/
        print "\n\n **********************"

        css_style = 1
        act_headers_and_details = to_html_acts_header_and_details(sHeaderList, list_of_acts, css_style)
        act_headers = to_html_actheaders(sHeaderList, css_style)
        act_details = to_html_actdetails(list_of_acts, css_style)

        sHtmlTemplatePath = str()
        sHtmlCSSPath = str()
        sFolderPath = str()
        if css_style == 1:
            sFolderPath = "invoice"
            sHtmlTemplatePath = "index_template.html"
            sHtmlCSSPath = os.path.join(sFolderPath, "style.css")
        elif css_style == 2:
            sFolderPath = "invoice2"
            sHtmlTemplatePath = "index_template2.html"
            sHtmlCSSPath = os.path.join(sFolderPath, "style.css")

        env = Environment(loader=FileSystemLoader(sFolderPath))
        template = env.get_template(sHtmlTemplatePath)
        template_vars = {
                         "tag_user_notice" : "Nothing to mention",
                         "tag_invoice_id": "425",
                         "tag_actual_date": "01 Jan 2017",
                         "tag_due_date": "01 Feb 2017",
                         "tag_doctor_full_name": "Ali Saad",
                         "tag_doctor_address": "Ghbayreh ya tayreh",
                         "tag_doctor_email": "khara.kleb@gmail.com",
                         "tag_payment_method": "Cash",
                         "tag_payment_identifier": "-",
                         "tag_act_header_list": act_headers,
                         "tag_act_details_list": act_details,
                         "tag_acts_header_and_details": act_headers_and_details,
                         "tag_total_sum": fGrandTotal,
                         "tag_total_paid": fPaid,
                         "tag_total_remaining": fGrandTotal-fPaid,
                         }

        # Render our file and create the PDF using our css style file
        sHtmlContent = template.render(template_vars)

        sOutputFname = "index_parsed_stylesheet_{0}".format(css_style)    

        with open(sOutputFname+".html", "w") as text_file:
            text_file.write("{0}".format(sHtmlContent))

        HTML(string=sHtmlContent).write_pdf(sOutputFname+".pdf", stylesheets=[sHtmlCSSPath])

    test()




"""
Template tags

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