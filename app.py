import os
from json import loads, dumps
import os.path
import pygogo as gogo
import pulsar
import random
import time

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Starting Consumer!!")

    client = pulsar.Client(f"pulsar://{get_config('PULSAR_SERVER')}")
    consumer = client.subscribe(get_config('PULSAR_TOPIC'), get_config('PULSAR_SUBSCRIPTION'),
                                consumer_type=pulsar.ConsumerType.Shared)
    sleep_time = int(get_config('SLEEP_TIME_PER_MESSAGE'))

    while True:
        msg = consumer.receive()
        try:
            # decode from bytes, encode with backslashes removed, decode back to a string, then load it as a dict
            message_body = loads(msg.data().decode().encode('latin1', 'backslashreplace').decode('unicode-escape'))
            logger.info("Message received", extra={'message_body': message_body})
            consumer.acknowledge(msg)
            time.sleep(sleep_time)
        except:  # noqa: E722
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()


def main_producer():
    logger.info("Starting Producer!!")
    topic = get_config("PULSAR_TOPIC")
    pulsar_server = get_config('PULSAR_SERVER')
    client = pulsar.Client(f"pulsar://{pulsar_server}")
    producer = client.create_producer(topic)
    duration = 3600
    sleep_time = int(get_config('SLEEP_TIME_PER_MESSAGE'))
    for i in range(duration):
        message = {'number': random.randint(0, 10000)}
        producer.send(dumps(message).encode('utf-8'))
        logger.info("Message sent", extra={'message_body': message, 'topic': topic})
        time.sleep(sleep_time)
    client.close()


def get_config(key):
    if os.environ.get(key):
        logger.info("found {} in an environment variable".format(key))
        return os.environ.get(key)


if __name__ == '__main__':
    if os.environ.get("PRODUCER_MODE"):
        main_producer()
    else:
        main()
