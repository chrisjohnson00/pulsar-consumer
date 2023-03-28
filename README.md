# pulsar-consumer
A sample Pulsar consumer/producer in Python

## PyPi Dependency updates

    docker run -it --rm -v ${PWD}:/repo -w /repo python:3.10.7-slim bash
    pip install --upgrade pip
    pip install --upgrade pulsar-client pygogo
    pip freeze > requirements.txt

## Environment variables

Some env vars are requierd to run

Sample for producer:

```
        env:
        - name: PULSAR_TOPIC
          value: test-topic
        - name: PULSAR_SUBSCRIPTION
          value: test-subscription
        - name: PULSAR_SERVER
          value: pulsar-broker.pulsar:6650
        - name: PRODUCER_MODE
          value: foobar
        - name: SLEEP_TIME_PER_MESSAGE
          value: '1'
```

Sample for consumer:

``` 
        env:
        - name: PULSAR_TOPIC
          value: test-topic
        - name: PULSAR_SUBSCRIPTION
          value: test-subscription
        - name: PULSAR_SERVER
          value: pulsar-broker.pulsar:6650
        - name: SLEEP_TIME_PER_MESSAGE
          value: '5'
```

  - `PULSAR_TOPIC` - The topic name to produce/consume against
  - `PULSAR_SUBSCRIPTION` - The topic subscription to produce/consume against
  - `PULSAR_SERVER` - The hostname for Pulsar
  - `PRODUCER_MODE` - If this env var is set (any value) the app runs in producern mode
  - `SLEEP_TIME_PER_MESSAGE` - The number of seconds to sleep after producing/consuming a message.  Helpful to set 
    producer:consumer ratios for testing auto scaling.
