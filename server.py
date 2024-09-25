import grpc
from concurrent import futures
import weather_pb2
import weather_pb2_grpc

import requests
from bs4 import BeautifulSoup

class WeatherServicer(weather_pb2_grpc.WeatherServicer):
    def Forecast(self, request, context):
        # Enter city name
        city = request.city 

        # Creating URL and making requests instance
        url = "https://www.google.com/search?q=" + "weather" + city
        html = requests.get(url).content

        # Getting raw data using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extracting the temperature
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text

        # Extracting the time and sky description
        str_ = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        data = str_.split('\n')
        time = data[0]
        sky = data[1]

        # Getting all div tags with the specific class name
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})

        # Extracting other required data
        strd = listdiv[5].text
        pos = strd.find('Wind')
        other_data = strd[pos:]

        return weather_pb2.WeatherResponse(temp=temp, time=time, sky=sky)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    weather_pb2_grpc.add_WeatherServicer_to_server(WeatherServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()