import grpc
import weather_pb2
import weather_pb2_grpc

def run(city):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherStub(channel)
        response = stub.Forecast(weather_pb2.WeatherRequest(city=city))
    print(f"Temperature: {response.temp}")
    print(f"Time: {response.time}")
    print(f"Sky: {response.sky}")

if __name__ == '__main__':
    # Get user Input 
    city = str(input("Please input city: "))
    run(city)