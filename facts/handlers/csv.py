import csv
import logging


class CSVHandler(object):
    """Read from and write to CSV files using Python’s Built-in CSV Library."""

    def __init__(self):
        self.logger = logging.getLogger("csv-handler")

    def read_from_file(self, file_path):
        self.logger.info(f"Start reading data from file {file_path}...")

        with open(file_path) as file:
            data = [item for item in csv.DictReader(file)]
        self.logger.info(f"Finished reading data ({len(data)} items) from csv file.")
        return data

    def export_to_file(self, data, file_path):
        if not data:
            self.logger.info(f"No data provided to be exported to the file.")
            return

        self.logger.info(f"Start saving data...")
        keys = data[0].keys()
        with open(file_path, "w") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        self.logger.info(f"Stored csv feed ({len(data)} items) in: {file_path}")
