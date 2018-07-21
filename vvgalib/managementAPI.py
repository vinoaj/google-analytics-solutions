class GAManagementAPI:
    def __init__(self, api_service, account_id, web_property_id):
        self.api_service = api_service
        self.account_id = account_id
        self.custom_dimensions = []
        self.web_property_id = web_property_id
        self.user_accounts = {}
        self.user_properties = {}
        self.user_views = {}

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
        self._generate_views()

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

        # print(self.user_accounts)

    def _generate_properties(self):
        response = self.api_service.v3_api.management().webproperties()\
                    .list(accountId='~all').execute()

        properties = response.get('items')

        for prop in properties:
            p = GAProperty(prop['id'])
            p.set_json_representation(prop)
            self.user_properties[prop['id']] = p

    def _generate_views(self):
        # for account_id, account in self.user_accounts.items():
        #     for property_id, prop in account.properties.items():
        #         response = self.api_service.v3_api.management().
        response = self.api_service.v3_api.management().profiles().list(
            accountId='~all', webPropertyId='~all').execute()
        views = response.get('items')
        # print(views)

        for view in views:
            v = GAView(view['id'])
            v.set_json_representation(view)
            self.user_views[view['id']] = v

    def print_views_list(self):
        views_by_web_property = {}
        for view_id, view in self.user_views.items():
            if view.property_id in views_by_web_property:
                views_by_web_property[view.property_id].append(view)
            else:
                views_by_web_property[view.property_id] = [view]

        print(views_by_web_property)



class GAView:
    def __init__(self, view_id):
        self.view_id = view_id
        self.property_id = None
        self.json_representation = {}

    def set_json_representation(self, json):
        # TODO: verification
        # TODO: explicitly set to JSON to prevent any security issues
        self.json_representation = json
        self.property_id = self.json_representation['webPropertyId']


class GAAccount:
    def __init__(self, account_id):
        self.account_id = account_id
        self.name = ''
        self.created = ''
        self.updated = ''
        self.starred = False
        self.properties = {}

    def get_account_id(self):
        return self.account_id

    def add_property(self, property):
        self.properties[property.property_id] = property


class GAProperty:
    def __init__(self, property_id):
        # self.account_id = account_id
        self.property_id = property_id
        self.json_representation = {}

    def set_json_representation(self, json):
        # TODO: verification
        # TODO: explicitly set to JSON to prevent any security issues
        self.json_representation = json
