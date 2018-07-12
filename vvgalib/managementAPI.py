class GAManagementAPI:
    def __init__(self, api_service, account_id, web_property_id):
        self.api_service = api_service
        self.account_id = account_id
        self.custom_dimensions = []
        self.web_property_id = web_property_id
        self.user_accounts = {}

        self.generate_account_property_view_list()
        # self.get_custom_dimensions()

    def get_custom_dimensions(self):
        # analytics.management().accounts().list().execute()
        response = self.api_service.v3_api.management().customDimensions().list(
            accountId=self.account_id, webPropertyId=self.web_property_id)\
            .execute()

        self.custom_dimensions = response.get('items')
        return self.custom_dimensions

    def generate_account_property_view_list(self):
        self._generate_accounts()
        self._generate_properties()

    def _generate_accounts(self):
        response = self.api_service.v3_api.management().accounts().list(

        ).execute()

        accounts = response.get('items')
        for account in accounts:
            # print(account)
            a = GAAccount(account['id'])
            a.name = account['name']
            a.created = account['created']
            a.updated = account['updated']
            if 'starred' in accounts:
                a.starred = True

            self.user_accounts[account['id']] = a

        print(self.user_accounts)

    def _generate_properties(self):
        for account_id, account in self.user_accounts.items():
            response = self.api_service.v3_api.management().webproperties(

            ).list(accountId=account_id

            ).execute()

            properties = response.get('items')
            print(properties)


class GAAccount:
    def __init__(self, account_id):
        self.account_id = account_id
        self.name = ''
        self.created = ''
        self.updated = ''
        self.starred = False

    def get_account_id(self):
        return self.account_id


class GAProperty:
    def __init__(self, account_id, property_id):
        self.account_id = account_id
        self.property_id = property_id
