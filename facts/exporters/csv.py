import csv
import logging


class CSVExporter(object):
    """Export data to scv file"""

    def __init__(self):
        self.logger = logging.getLogger("csv-exporter")

    def export_to_file(self, data, file_path):
        self.logger.info(f"Start saving data...")
        keys = data[0].keys()
        with open(file_path, "w") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

        self.logger.info(f"Stored csv feed ({len(data) - 1} items) in: {file_path}")
