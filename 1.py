import requests
import time
import datetime
import statistics

URL = "https://yandex.com/time/sync.json?geo=213"

# a)
raw = requests.get(URL).json()
print("a)\n", raw, "\n", sep="")

# b)
now_utc = datetime.datetime.fromtimestamp(raw["time"] / 1000, datetime.timezone.utc)
time_zone = raw.get("clocks", {}).get("213", {}).get("offsetString")
print("b)\n", now_utc.strftime("%d-%m-%Y %H:%M:%S"), sep="")
print(time_zone)

# c)
print("\nc)")
start = time.time()
server_time = raw["time"] / 1000
delta = abs(server_time - start)
print(f"{delta:.5f} sec")

# d)
print("\nd)")
deltas = []
for i in range(5):
    start = time.time()
    server_time = raw["time"] / 1000
    delta = abs(server_time - start)
    deltas.append(delta)
    time.sleep(1)
result = statistics.mean(deltas)
print(f"{result:.5f} sec")
