"""Kafka consumer."""

from datetime import datetime as dt
from json import loads
from os import getenv

from kafka import KafkaConsumer

from kafka_consumer.utils import (ERROR_NO_TIMESTAMP, Timestamp,
                                  create_writer, get_args)


def get_consumer(args):
    """Initialize kafka consumer."""
    config = {
        'bootstrap_servers': getenv('BOOTSTRAP_SERVERS'),
        'sasl_plain_username': getenv('SASL_USERNAME'),
        'sasl_plain_password': getenv('SASL_PASSWORD'),
        'security_protocol': getenv('SECURITY_PROTOCOL'),
        'sasl_mechanism': getenv('SASL_MECHANISMS')
    }
    return KafkaConsumer(args.topic, **config)


def main(args=[]):
    """Run main program."""
    args = args or get_args()
    consumer = get_consumer(args)

    with create_writer() as write:
        print('Consumer reading...')
        counter = 0
        for message in consumer:
            assert message.timestamp, ERROR_NO_TIMESTAMP

            try:
                jmessage = loads(message.value)
            except Exception:
                print()
                print('Something went terribly wrong reading json message...')
                continue

            ts_produced = dt.fromtimestamp(message.timestamp / 1000)
            ts_event = dt.fromtimestamp(jmessage[args.timestamp_column] / 1000)
            ts_consumed = dt.now()

            write({
                Timestamp.EVENT.value: ts_event,
                Timestamp.PRODUCED.value: ts_produced,
                Timestamp.CONSUMED.value: ts_consumed,
            })

            counter += 1
            print(f"Received: {counter}", end='\r', flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('You stopped the program.')
