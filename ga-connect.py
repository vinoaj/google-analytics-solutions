import argparse
import httplib2
import pandas as pd
from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from pprint import pprint
from vvgalib.reportbuilder import GAReportBuilder, GAReportParser

# https://developers.google.com/identity/protocols/googlescopes#analyticsv3
GOOGLE_ANALYTICS_SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/analytics.edit',
    'https://www.googleapis.com/auth/analytics.manage.users'
]

# For authentication
# https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_PATH = 'client_secrets.json'
# Credentials are stored in this file
FILE_STORAGE_PATH = 'analyticsreporting.dat'


def initialize_analytics_service(api_version=4, no_local_webserver=False):
    # v3 required for Management API
    # v4 required for the Core Reporting API

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])

    if no_local_webserver is True:
        flags = parser.parse_args(['--noauth_local_webserver'])
    else:
        flags = parser.parse_args([])

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=GOOGLE_ANALYTICS_SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them. If the
    # credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(FILE_STORAGE_PATH)
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)

    api_version_str = 'v' + str(api_version)
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    analytics = build('analytics', api_version_str, http=http)

    return analytics


def get_accounts(analytics):
    accounts = analytics.management().accounts().list().execute()

    if accounts.get('items'):
        return accounts.get('items')
    else:
        return []


def print_accounts(accounts):
    print(accounts)

    col_headers = accounts[0].keys()
    df = pd.DataFrame(columns=col_headers).set_index('id')
    # df = pd.DataFrame()

    for account in accounts:
        print('AAAAAAA')
        print(df)
        account_df = pd.io.json.json_normalize(account).set_index('id')
        df = df.append(account_df)
        # df = df.append(pd.DataFrame(account).set_index('id'))

    df.sort_values('name', inplace=True)
    print(df.name)

    lens_id = [len('Account ID')]
    lens_name = [len('Account Name')]
    accounts_copy = accounts
    account_details_by_name = {}

    for account in accounts_copy:
        account_id = account.get('id')
        account_name = account.get('name')
        account_details_by_name[account_name] = {
            'account_id': account_id,
            'account': account
        }
        lens_id.append(len(account_id))
        lens_name.append(len(account_name))

    max_len_id = max(lens_id)
    max_len_name = max(lens_name)

    # Sort keys by name
    account_names = sorted(account_details_by_name.keys())

    print('Account Name'.ljust(max_len_name), '|', 'Account ID'.ljust(max_len_id), '|')
    # print('=' * (max_len_name + max_len_id + 2))

    for account_name in account_names:
        account = account_details_by_name[account_name]['account']
        account_id = account.get('id')
        account_name = account.get('name')
        print(account_name.ljust(max_len_name), '|', account_id.rjust(max_len_id), '|')


def get_properties(analytics, account_id):
    properties = analytics.management().webproperties().list(
        accountId=account_id).execute().get('items')

    print(properties)
    return properties


def print_properties(properties):
    lens_id = [len('Property ID')]
    lens_name = [len('Property Name')]
    properties_copy = properties
    property_details_by_name = {}

    for property in properties_copy:
        property_id = property.get('id')
        property_name = property.get('name')
        property_details_by_name[property_name] = {
            'property_id': property_id,
            'property': property
        }
        lens_id.append(len(property_id))
        lens_name.append(len(property_name))

    max_len_id = max(lens_id)
    max_len_name = max(lens_name)

    # Sort keys by name
    property_names = sorted(property_details_by_name.keys())

    # print(len('Account ID'), max_len_id)
    # print(max_len_id, max_len_name)

    print('Property Name'.ljust(max_len_name), '|', 'Property ID'.ljust(max_len_id), '|')
    # print('=' * (max_len_name + max_len_id + 2))

    for property_name in property_names:
        property = property_details_by_name[property_name]['property']
        property_id = property.get('id')
        property_name = property.get('name')
        print(property_name.ljust(max_len_name), '|', property_id.rjust(max_len_id), '|')


def get_views(analytics, account_id, property_id):
    views = analytics.management().profiles().list(
        accountId=account_id,
        webPropertyId=property_id).execute()

    return views


def print_views(views):
    print(views)
    views_copy = views

    for view in views_copy.get('items'):
        print("{view_id} - {view_name} \n".format(view_id=view.get('id'),
                                                  view_name=view.get('name')))


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response"""

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                # print header + ': ' + dimension
                pass

            for i, values in enumerate(dateRangeValues):
                # print 'Date range (' + str(i) + ')'
                pass

                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    # print metricHeader.get('name') + ': ' + value
                    pass


def main2():
    analytics_v4 = initialize_analytics_service(4, False)
    rb = GAReportBuilder('174820262')
    rb.add_date_range('2018-05-01', 'today')
    rb.add_dimensions(['ga:dateHourMinute', 'ga:eventCategory',
                       'ga:eventAction',
                      'ga:eventLabel', 'ga:dimension1']);
    rb.add_metric('ga:hits')
    rbr = rb.build_request()
    pprint(rbr)

    r = analytics_v4.reports().batchGet(body=rbr).execute()
    pprint(r)

    rp = GAReportParser(r['reports'][0])
    csv = rp.get_csv()
    print(csv)


def main():
    analytics_v3 = initialize_analytics_service(3, False)
    analytics_v4 = initialize_analytics_service(4, False)
    # print(dir(analytics_v4))

    accounts = get_accounts(analytics_v3)
    print_accounts(accounts)
    account_id = int(input('Select Account ID #> '))

    properties = get_properties(analytics_v3, account_id)
    print_properties(properties)
    property_id = (input('Select Property ID #> '))

    views = get_views(analytics_v3, account_id, property_id)
    print_views(views)


if __name__ == "__main__":
    main2()