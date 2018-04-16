class GAReportBuilder:
    def __init__(self, view_id=0):
        self.view_id = view_id
        self.date_ranges = []
        self.dimensions = []
        self.metrics = []

    def add_date_range(self, start_date='7daysAgo', end_date='today'):
        # TODO: Handle different types of date formats
        self.date_ranges.append({
            'startDate': start_date,
            'endDate': end_date
        })

    def add_dimension(self, dimension):
        self.dimensions.append(dimension)

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def add_metric(self, metric):
        self.metrics.append(metric)

    def set_metrics(self, metrics):
        self.metrics = metrics

    def build_request_date_ranges_array(self):
        if len(self.date_ranges) is 0:
            self.date_ranges.append({
                'startDate': '7daysAgo',
                'endDate': 'today'
            })

        return self.date_ranges

    def build_request_metrics_array(self):
        metrics_array = []

        for metric in self.metrics:
            metrics_array.append({'expression': metric})

        return metrics_array

    def build_request(self):
        # TODO: generate multiple (max 5) report requests
        report_request = {
            'viewId': self.view_id,
            'dateRanges': self.build_request_date_ranges_array(),
            'metrics': self.build_request_metrics_array()
        }

        return report_request
