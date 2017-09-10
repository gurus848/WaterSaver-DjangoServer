from django.http import JsonResponse, HttpResponse, Http404
from django.template import loader
from models import Waterdata
from paho.mqtt import client
from WaterSaver.WaterRecord import WaterRecord
import time

#MQTT Constants
waterDataMQTTTopic = "waterUsage"
CLIENT_ID = 'server'
MQTT_SERVER_HOST = '10.0.0.3'

#Request Parameter Constants
FLOWRATE_PARAM = 'flow'
STOPTIME_PARAM = 'time'
FROMTIME_PARAM = 'fromTime'
TOTIME_PARAM = 'toTime'


def addWaterRecord(request):

    current_flow_rate = float(request.GET.get(FLOWRATE_PARAM))
    stop_time_epoch = int(request.GET.get(STOPTIME_PARAM))

    valid = 0

    if 0 < current_flow_rate < 500:  # for simple validation of the readings
        mqtt_client = client.Client(CLIENT_ID)
        mqtt_client.connect(MQTT_SERVER_HOST)
        mqtt_client.publish(waterDataMQTTTopic, current_flow_rate)
        mqtt_client.disconnect()

        last_reading_timestamp = Waterdata.objects.last().stoptimeepoch
        time_difference = int(stop_time_epoch) - int(last_reading_timestamp)

        if time_difference <= 5:
            valid = time_difference
            last_record = Waterdata.objects.last()
            if last_record.numberofwaterflowreadings > 2000:
                new_record = Waterdata()
                new_record.averagewaterflowrate = current_flow_rate
                new_record.stoptimeepoch = stop_time_epoch
                new_record.starttimeepoch = stop_time_epoch
                new_record.waterflowreadingstotal = current_flow_rate
                new_record.numberofwaterflowreadings = 1
                new_record.save()
            else:
                last_record.numberofwaterflowreadings += 1
                last_record.waterflowreadingstotal += current_flow_rate
                last_record.averagewaterflowrate = last_record.waterflowreadingstotal / last_record.numberofwaterflowreadings
                last_record.stoptimeepoch = stop_time_epoch
                last_record.save()
        else:
            new_record = Waterdata()
            new_record.averagewaterflowrate = current_flow_rate
            new_record.stoptimeepoch = stop_time_epoch
            new_record.starttimeepoch = stop_time_epoch
            new_record.waterflowreadingstotal = current_flow_rate
            new_record.numberofwaterflowreadings = 1
            new_record.save()

    return JsonResponse({'did something': 'true', 'validity': valid, 'stoptimeepoch':stop_time_epoch})


def getWaterReadings(request):
    from_time = int(request.GET.get(FROMTIME_PARAM))
    to_time = int(request.GET.get(TOTIME_PARAM))
    results = Waterdata.objects.filter(stoptimeepoch__gte=from_time).filter(starttimeepoch__lte=to_time)
    results_array = []
    for result in results:
        results_array.append({'id': result.id,
                              'startTimeEpoch': result.starttimeepoch,
                              'stopTimeEpoch': result.stoptimeepoch,
                              'averageWaterFlowRate': result.averagewaterflowrate})
    return JsonResponse(results_array, safe=False)


def getCurrentTime(request):
    return HttpResponse(int(time.time()))


def viewWaterRecords(request):
    data = Waterdata.objects.all().order_by("-id")[:10]
    formatted_data = []
    for record in data:
        formatted_data.append(WaterRecord(record.starttimeepoch, record.stoptimeepoch, record.averagewaterflowrate))

    context = {
        "data":formatted_data
    }
    template = loader.get_template("WaterSaver/view_water_records.html")
    return HttpResponse(template.render(context, request))

# def testMQTT(request):
#     mqtt_client = client.Client(CLIENT_ID)
#     mqtt_client.connect(MQTT_SERVER_HOST)
#     mqtt_client.publish(waterDataMQTTTopic, "12345")
#     mqtt_client.disconnect()
#     return JsonResponse({})
