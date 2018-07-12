from vvgalib.gaapiwrapper import GAAPIWrapper
from vvgalib.managementAPI import GAManagementAPI
from vvgalib.reportbuilder import GAReportBuilder

ACCOUNT_ID = 3172639
WEB_PROPERTY_ID = 'UA-3172639-1'
VIEW_ID = 59236323

def main_2():
    ga_api_wrapper = GAAPIWrapper()
    mapi = GAManagementAPI(ga_api_wrapper, ACCOUNT_ID, WEB_PROPERTY_ID)
    mapi.get_accounts()



def main():
    ga_api_wrapper = GAAPIWrapper()
    mapi = GAManagementAPI(ga_api_wrapper, ACCOUNT_ID, WEB_PROPERTY_ID)
    print(mapi.custom_dimensions)

    for cd in mapi.custom_dimensions:
        print("{0}, {2}, {1}".format(cd['id'], cd['name'], cd['scope']))
        rb = GAReportBuilder(VIEW_ID)
        rb.add_date_range('2018-01-01', 'today')
        rb.add_dimension(cd['id'])

        primary_metric = 'ga:hits'
        # if cd['scope'] is 'SESSION':
        #     primary_metric = 'ga:sessions'
        # elif cd['scope'] is 'USER':
        #     primary_metric = 'ga:users'

        rb.add_metric(primary_metric)
        rb.add_order_by(primary_metric)

        rbr = rb.build_request()
        # print(rbr)


if __name__ == '__main__':
    main_2()