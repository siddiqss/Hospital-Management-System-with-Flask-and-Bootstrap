import thingspeak
import json

channel_id = 1270496  # PUT CHANNEL ID HERE
write_key = "XXXXXXXXXXXXXXXX"  # PUT YOUR WRITE KEY HERE, (only needed if writing data)
read_key = "XXXXXXXXXXXXXXXX" # PUT YOUR API KEY HERE, (read access only)

channel = thingspeak.Channel(id=channel_id, api_key=read_key)

# If you want text output instead of json try this
# channel = thingspeak.Channel(id=channel_id,api_key=api_key, fmt='txt')
def read_patient_data():
    try:
        pat_id_data = channel.get_field(field="field4", options={"results": 1})
        pat_id_data = json.loads(pat_id_data)
        pat_id_data = pat_id_data.get('feeds')[0].get('field4')
        temp_data = channel.get_field(field="field3", options={"results": 1})
        temp_data = json.loads(temp_data)
        temp_data = temp_data.get('feeds')[0].get('field3')
        # Get the last 2 results from field 1 of your channel
        pulse_data = channel.get_field(field="field1", options={"results": 1})
        pulse_data = json.loads(pulse_data)
        pulse_data = pulse_data.get('feeds')[0].get('field1')

        timestamp_data = channel.get_field(field="field5", options={"results": 1})
        timestamp_data = json.loads(timestamp_data)
        timestamp_data = timestamp_data.get('feeds')[0].get('field5')

        lat_data = channel.get_field(field="field6", options={"results": 1})
        lat_data = json.loads(lat_data)
        lat_data = lat_data.get('feeds')[0].get('field6')

        lng_data = channel.get_field(field="field7", options={"results": 1})
        lng_data = json.loads(lng_data)
        lng_data = lng_data.get('feeds')[0].get('field7')

        return pat_id_data, temp_data, pulse_data, lat_data, lng_data, timestamp_data
        # Get the age of the last data in field 1 of your channel in seconds
        # print(channel.get_last_data_age(field="field1"))
        # Get the last data in field 1 of your channel
        # print(channel.get_field_last(field="field1"))
    except:
        raise print("connection failed")

