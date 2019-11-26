#!/usr/bin/env python
import os

from alpha_vantage.timeseries import TimeSeries
import paho.mqtt.publish as publish

LAST_FILE = '/tmp/last.txt'

def main():
    ts = TimeSeries(key=os.environ['API_KEY'], output_format='csv')
    data, meta = ts.get_intraday(os.environ.get('STOCK', 'GOOGL'), interval=os.environ.get('INTERVAL', '15min'))

    # get csv indexes
    header = next(data)
    i_close = header.index('close')
    i_ts = header.index('timestamp')

    # most recent data
    recent = next(data)
    if os.path.isfile(LAST_FILE):
        with open(LAST_FILE) as f:
            # is there actually new data?
            if f.read().strip() == recent[i_ts]:
                return

    # get the difference between the newest data and the previous
    change = float(recent[i_close]) - float(next(data)[i_close])
    print(f'change over last 15 minutes: {change:.3f}')

    with open(LAST_FILE, 'w') as f:
        # save the most recent data's timestamp
        print(recent[i_ts], file=f)

    if 'MQTT_HOST' not in os.environ:
        return

    topic = f'cmnd/{os.environ.get("SONOFF_TOPIC", "stonkmaster")}/Power'
    state = 'ON' if change > 0 else 'OFF'
    auth = {'username': os.environ['MQTT_USERNAME'], 'password': os.environ['MQTT_PASSWORD']}

    print(f'publishing to topic "{topic}" to turn StonkMaster {state}"')
    publish.single(topic, state, hostname=os.environ['MQTT_HOST'], port=int(os.environ.get('MQTT_PORT', 1883)),
        auth=auth)

if __name__ == '__main__':
    main()
