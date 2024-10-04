import os
import requests
import json
from json import JSONEncoder
from typing import List

import numpy
import redis
from fastapi import (FastAPI,
                     Request)
import openmeteo_requests
from pydantic import BaseModel

# globals
URL="https://climate-api.open-meteo.com/v1/climate"
CLIENT = openmeteo_requests.Client()

BACKEND_URI = os.environ['BACKEND_URI']
BACKEND_PORT = os.environ['BACKEND_PORT']
BACKEND_DB = os.environ['BACKEND_DB']
BACKEND_USER = os.environ['BACKEND_USER']
BACKEND_PASS = os.environ['BACKEND_PASS']

# connect to redis
rd = redis.Redis(host=BACKEND_URI, 
                 port=BACKEND_PORT, 
                 db=BACKEND_DB,
                 username="default", # use your Redis user. More info https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/
                 password="secret",) # use your Redis password
                 #ssl=True,
                 #ssl_certfile="./redis_user.crt",
                 #ssl_keyfile="./redis_user_private.key",
                 #ssl_ca_certs="./redis_ca.pem")

# create api
app = FastAPI()

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

# data model
class Weather(BaseModel):
  # declare data expected by body
  latitude: float
  longitude: float
  start: str
  end: str

@app.get("/")
def read_root():
  return "Hello World"

@app.post("/weather/")
async def get_body(weather: Weather):
  return weather

@app.post("/weather/dewpoint/")
async def postDailyDewPoint2mMean(weather: Weather):
  # check cache
  cache = rd.get(str(weather))
  if cache:
    print("cache hit")
    print(json.loads(cache))
    return json.loads(cache)
  else:
    print("cache miss")
    weather_dict = weather.model_dump()
    # request get from open weather api
    params = {
          "latitude": weather.latitude, #52.5
          "longitude": weather.longitude, #13.41
          "start_date": weather.start, #"2024-01-01"
          "end_date": weather.end, # "2024-01-02"
          "models": ["CMCC_CM2_VHR4", "FGOALS_f3_H", "HiRAM_SIT_HR", "MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR", "NICAM16_8S"],
          "daily": "dew_point_2m_mean"
        }
    responses = CLIENT.weather_api(URL, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_dew_point_2m_mean = daily.Variables(0).ValuesAsNumpy()
    print(f"Daily Dew Point 2mim Mean {daily_dew_point_2m_mean}")
    print(f"Weather: {str(weather)}")
    encodedNumpyData = json.dumps(daily_dew_point_2m_mean, cls=NumpyArrayEncoder)
    # TODO: return actual json data that looks decent
    rd.set(str(weather), encodedNumpyData)
    return f"Current {encodedNumpyData}"
  

@app.post("/test_model/")
async def testModel(weather: Weather):
  # check cache
  cache = rd.get(str(weather))
  if cache:
    print("cache hit")
    print(json.loads(cache))
    return json.loads(cache)
  else:
    print("cache miss")
    weather_dict = weather.model_dump()
    # request get from open weather api
    params = {
          "latitude": weather.latitude, #52.5
          "longitude": weather.longitude, #13.41
          "start_date": weather.start, #"2024-01-01"
          "end_date": weather.end, # "2024-01-02"
          "models": ["CMCC_CM2_VHR4", "FGOALS_f3_H", "HiRAM_SIT_HR", "MRI_AGCM3_2_S", "EC_Earth3P_HR", "MPI_ESM1_2_XR", "NICAM16_8S"],
          "daily": "dew_point_2m_mean"
        }
    responses = CLIENT.weather_api(URL, params=params)
    response = responses[0]
    daily = response.Daily()
    daily_dew_point_2m_mean = daily.Variables(0).ValuesAsNumpy()
    print(f"Daily Dew Point 2mim Mean {daily_dew_point_2m_mean}")
    print(f"Weather: {str(weather)}")
    encodedNumpyData = json.dumps(daily_dew_point_2m_mean, cls=NumpyArrayEncoder)
    # TODO: return actual json data that looks decent
    rd.set(str(weather), encodedNumpyData)
    return f"Current {encodedNumpyData}"

