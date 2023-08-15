import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import ThingSpeakData
from django.db.models import F

def fetch_and_store_thingspeak_data(request):
    channel_url = 'https://api.thingspeak.com/channels/2235681/feeds.json?api_key=Z6CFXHDNACTN0571&results=2&timezone=Africa/Nairobi'

    try:
        response = requests.get(channel_url)
        data = response.json()
        number_of_entries = len(data['feeds'])
        print(number_of_entries)
        
        for n in range(number_of_entries):
        # Extract latitude and longitude from the data
            latitude = data['feeds'][n]['field1']
            longitude = data['feeds'][n]['field2']
            timestamp = data['feeds'][n]['created_at']

            existing_record = ThingSpeakData.objects.filter(latitude=latitude, longitude=longitude, timestamp=timestamp).first()

            if existing_record:
                pass
            else:
                # Create and save a ThingSpeakData instance
                thingspeak_data = ThingSpeakData(latitude=latitude, longitude=longitude, timestamp=timestamp)
                thingspeak_data.save()

        response_data = {
            'latitude': latitude,
            'longitude': longitude,
            'timestamp' : timestamp
        }
    except requests.RequestException as e:
        response_data = {
            'error': 'Error fetching data from ThingSpeak.'
        }

    return JsonResponse(response_data)

# def show_latest_data_on_map(request):
#     channel_url = 'https://api.thingspeak.com/channels/2235681/feeds.json?api_key=Z6CFXHDNACTN0571&results=2&timezone=Africa/Nairobi'

#     try:
#         response = requests.get(channel_url)
#         data = response.json()
#         number_of_entries = len(data['feeds'])
#         print(number_of_entries)
#         latitude = []
#         longitude = []
#         timestamp = []

#         for n in range(number_of_entries):
#             # Extract latitude and longitude from the data
#             if n == (number_of_entries - 1):
#                 last_latitude = data['feeds'][n]['field1']
#                 last_longitude = data['feeds'][n]['field2']
#                 last_timestamp = data['feeds'][n]['created_at']

#             else:
#                 latitude.append(data['feeds'][n]['field1'])
#                 longitude.append(data['feeds'][n]['field2'])
#                 timestamp.append(data['feeds'][n]['created_at'])

#         context = {
#             'latitude' : latitude,
#             'longitude' : longitude,
#             'timestamp' : timestamp,
#             'last_latitude' : last_latitude,
#             'last_longitude' : last_longitude,
#             'last_timestamp' : last_timestamp
#         }


#     except requests.RequestException as e :
#         print('Failed')

#     return render(request, 'map.html', context)


def show_latest_data_on_map(request):
    latitude = []
    longitude = []
    timestamp = []
    other_data = ThingSpeakData.objects.all()
    for data in other_data:
        latitude.append(data.latitude)
        longitude.append(data.longitude)
        timestamp.append(data.timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    latest_data = ThingSpeakData.objects.order_by('-timestamp').first()
    
    data_dict = {
        "latitude": latest_data.latitude,
        "longitude": latest_data.longitude,
        "timestamp": latest_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    latest_data_json = json.dumps(data_dict)
    # q; how do i make the json data of combined_data serialisable




    combined_data = list(zip(latitude, longitude, timestamp))
    json_data = json.dumps(combined_data)

    if latest_data:
        context = {
            'json_data': json_data,
            'latest_data_json': latest_data_json,
            # 'latitude': latitude,
            # 'longitude': longitude,
            # 'timestamp': timestamp,
            # 'latest_latitude': latest_data.latitude,
            # 'latest_longitude': latest_data.longitude,
            # 'latest_timestamp': latest_data.timestamp,
        }
    else:
        context = {
            'error': 'No data available.'
        }

    return render(request, 'map1.html', context)
