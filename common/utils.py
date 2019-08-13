from datetime import datetime

from scrapy.utils.project import get_project_settings

from facts.settings import FEED_URI_TEMPLATE, OUTPUT_FILE_TEMPLATE


def get_settings(output_file, source):
    output_file = output_file or datetime.now().strftime("auto%Y-%m-%dT%H:%M:%S.csv")

    raw_path = FEED_URI_TEMPLATE.format(source=source, filename=output_file)
    output_path = OUTPUT_FILE_TEMPLATE.format(source=source, filename=output_file)

    settings = get_project_settings()
    settings["FEED_URI"] = raw_path

    return settings, raw_path, output_path