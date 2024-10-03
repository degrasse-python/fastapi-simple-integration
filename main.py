import requests
import json
from typing import List

import redis
from fastapi import (FastAPI,
                     Request)
import openmeteo_requests
from pydantic import BaseModel

# connect to redis
rd = redis.Redis(host='localhost', port=6379, db=0)
# create api
app = FastAPI()
# globals
URL="https://climate-api.open-meteo.com/v1/climate"
CLIENT = openmeteo_requests.Client()

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

@app.get("/weather/dewpoint/")
async def test(weather: Weather):
  # check cache
  cache = rd.get(weather)
  if cache:
    print("cache hit")
    # return json.loads(cache)
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
    # rd.set("user", daily_dew_point_2m_mean)

  return f"Current {response.Daily()}"



@app.post("/test/")
async def test(request: Request):
  try : 
    data = await request.json()
    d = dict(data)
    print(f'request json : {d['latitude']}')
  except Exception as err:
    # could not parse json
    data = await request.body()
    print(f'request body : {data}')    
  return {"received_request_body": await request.body()}


@app.post("/test_model/")
async def test(weather: Weather):
  # check cache
  cache = rd.get(str(weather))
  if cache:
    print("cache hit")
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
    rd.set(str(weather), weather.model_dump_json())
    # print(weather.model_dump_json())

  return f"Current {response.Daily()}"