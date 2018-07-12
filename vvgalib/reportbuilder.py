# from pprint import pprint


class GAReportBuilder:
    def __init__(self, view_id=0):
        self.view_id = view_id
        self.date_ranges = []
        self.dimensions = []
        self.metrics = []
        self.order_bys = []
        self.api_client = None

    def add_date_range(self, start_date='7daysAgo', end_date='today'):
        self.date_ranges.append({
            'startDate': start_date,
            'endDate': end_date
        })

    def add_dimension(self, dimension):
        self.dimensions.append(dimension)

    def add_dimensions(self, dimensions):
        self.dimensions = self.dimensions + dimensions

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def add_metric(self, metric):
        self.metrics.append(metric)

    def set_metrics(self, metrics):
        self.metrics = metrics

    def add_order_by(self, field, direction='DESCENDING'):
        self.order_bys.append({
            'fieldName': field,
            'sortOrder': direction
        })

    def build_request_date_ranges_array(self):
        if len(self.date_ranges) is 0:
            self.date_ranges.append({
                'startDate': '7daysAgo',
                'endDate': 'today'
            })

        return self.date_ranges

    def build_request_dimensions_array(self):
        dimensions_array = []

        for dimension in self.dimensions:
            dimensions_array.append({'name': dimension})

        return dimensions_array

    def build_request_metrics_array(self):
        metrics_array = []

        for metric in self.metrics:
            metrics_array.append({'expression': metric})

        return metrics_array

    def build_request(self):
        # TODO: generate multiple (max 5) report requests
        request_body = {'reportRequests': []}

        report_request = {
            'viewId': self.view_id,
            'dateRanges': self.build_request_date_ranges_array(),
            'metrics': self.build_request_metrics_array(),
            'dimensions': self.build_request_dimensions_array()
        }
        request_body['reportRequests'].append(report_request)
        return request_body


class GAReportParser:
    def __init__(self, request_response):
        self.request_response = request_response
        # column_indices = {}

    def get_csv(self):
        csv_rows = [self.get_header_csv()]
        rows = self.request_response['data']['rows']
        for row in rows:
            # pprint(row['dimensions'])
            row_csv = ','.join(row['dimensions'])
            metrics = row['metrics']
            for metric in metrics:
                row_csv += ',' + ','.join(metric['values'])
            csv_rows.append(row_csv)

        return "\n".join(csv_rows)

    def get_header_csv(self):
        headers = self.request_response['columnHeader']['dimensions']
        metricHeaders = self.request_response['columnHeader'][
            'metricHeader']['metricHeaderEntries']
        for metricHeader in metricHeaders:
            headers.append(metricHeader['name'])

        headers_csv = ','.join(headers)
        return headers_csv