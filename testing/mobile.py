url = "http://localhost:12890"

print("SETUP EMULATOR")
print("-" * 50)
import requests

print("LOADING DEVICE")
info = requests.get(url + "/info").json()["data"]
addr = requests.get(url + "/info/address").json()
addr = (addr["data"]["hostname"], addr["data"]["ip"]["local"])
print(f"Connected to: {addr}")

print("1| Check if Device is Setup")
r = requests.get(url + "/setup/check").json()["data"]
if r["setup"]:
    raise Exception("Device Already Setup!")

print("2| Request Setup Token")
r = requests.get(url + "/setup/request").json()
if not r["status"]["success"]:
    raise Exception(f"Failed to Request Setup: {r['data']['error']}")
token = r["data"]["token"]

print("3| Set Wifi Details")
with open("mobilewifi.txt", "r") as f:
    wifi_ssid, wifi_pass = f.read().split(":", 1)
r = requests.post(url + "/setup/wifi", params={"token": token}, data={"ssid": wifi_ssid, "password": wifi_pass})
