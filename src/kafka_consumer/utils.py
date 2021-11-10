"""Some usefull utility functions."""

from argparse import ArgumentParser
from enum import Enum
from contextlib import contextmanager
from csv import DictWriter, QUOTE_NONNUMERIC

from dotenv import load_dotenv

ERROR_NO_TIMESTAMP = 'Timestamp of message creation not present, aborting...'


class Timestamp(Enum):
    """Various timestamps."""

    EVENT = 'event_ts'
    PRODUCED = 'produced_ts'
    CONSUMED = 'consumed_ts'


def get_args():
    """Get arguments and env vars."""
    load_dotenv()
    parser = ArgumentParser('consumer')
    parser.add_argument('--topic', type=str, default='wifi.movement')
    parser.add_argument('--timestamp_column', type=str,
                        default='recordTimestamp')
    return parser.parse_args()


@contextmanager
def create_writer():
    """Write row in specific format."""
    filepath = 'output/log.csv'
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        csv_writer = DictWriter(f, [t.value for t in Timestamp],
                                delimiter=",",
                                lineterminator='\n',
                                quoting=QUOTE_NONNUMERIC)
        csv_writer.writeheader()

        def _write(data):
            csv_writer.writerow(data)
        yield _write
