import argparse
import httplib2
# import pandas as pd
from apiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools
# from pprint import pprint
# from vvgalib.reportbuilder import GAReportBuilder, GAReportParser

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


class GAAPIWrapper:
    def __init__(self):
        self.v3_api = self.initialize_analytics_service(api_version=3)
        self.v4_api = self.initialize_analytics_service(api_version=4)

    def initialize_analytics_service(self, api_version=4,
                                     no_local_webserver=False):
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