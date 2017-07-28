import argparse

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPES = [
    'https://www.googleapis.com/auth/analytics.readonly',
    'https://www.googleapis.com/auth/analytics.edit',
    'https://www.googleapis.com/auth/analytics.manage.users'
]
# DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
CLIENT_SECRETS_PATH = 'client_secrets.json'
FILE_STORAGE_PATH = 'analyticsreporting.dat'
VIEW_ID = '<REPLACE_WITH_VIEW_ID>'


def initialize_analytics_service(api_version=4):
    flags = get_flags()

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRETS_PATH, scope=SCOPES,
        message=tools.message_if_missing(CLIENT_SECRETS_PATH))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
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


"""
def initialize_analytics_service_v3():
    flags = get_flags()

    # Set up a Flow object to be used if we need to authenticate.
    flow = client.flow_from_clientsecrets(
        client_secrets_path, scope=scope,
        message=tools.message_if_missing(client_secrets_path))

    # Prepare credentials, and authorize HTTP object with them.
    # If the credentials don't exist or are invalid run through the native client
    # flow. The Storage object will ensure that if successful the good
    # credentials will get written back to a file.
    storage = file.Storage(api_name + '.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, flags)
  
    http = credentials.authorize(http=httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service
"""


def get_flags():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    flags = parser.parse_args([])
    return flags


def list_accounts(analytics):
    accounts = analytics.management().accounts().list().execute()

    if accounts.get('items'):
        accounts = accounts.get('items')

        for account in accounts:
            account_id = account.get('id')
            account_name = account.get('name')
            print(account_name)
            print(account_id)


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


def main():
    service_v3 = initialize_analytics_service(3)
    # service_v4 = initialize_analytics_service()
    # print(dir(service_v3))
    list_accounts(service_v3)


if __name__ == "__main__":
    main()