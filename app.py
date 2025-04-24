from flask import Flask, request
from LightGroup import LightGroup
from BulbFinder import BulbFinder
from pywizlight.bulb import PilotBuilder
import asyncio
import os

room = LightGroup()
async def setup():
    bf = BulbFinder("192.168.0.255")
    await bf.findBulbs()
    bf.printBulbsToFile("bulbs.txt")
    room.addLightsFromFile("bulbs.txt")
asyncio.run(setup())

app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World!'
    
@app.route("/on", methods=["POST"])
async def on():
    await room.turnOnAll()
    return "Bulbs turned on"

@app.route("/off", methods=["POST"])
async def off():
    await room.turnOffAll()
    return "Bulbs turned off"
    
@app.route("/toggle", methods=["POST"])
async def toggle():
    await room.toggleAll()
    return "Bulbs toggled"
    
@app.route("/set", methods=["POST"])
async def set():
    temp = request.args.get("temp", default=2700, type=int)
    brightness = request.args.get("brightness", default=255, type=int)
    brightness = min(255, brightness)

    pb = PilotBuilder(colortemp=temp, brightness=brightness)

    await room.setAll(pb)
    return f'Bulbs set to {pb.pilot_params["temp"]}k and {pb.pilot_params["dimming"]} brightness {brightness}'

@app.route("/increment", methods=["POST"])
async def increment():
    temp = request.args.get("temp", default=2700, type=int)
    current_brightness = await room.getBrightness()
    new_brightness = min(255, current_brightness + 10)
    
    pb = PilotBuilder(colortemp=temp, brightness=new_brightness)
    
    await room.setAll(pb)
    return f'Brightness incremented to {new_brightness}'

@app.route("/decrement", methods=["POST"])
async def decrement():
    temp = request.args.get("temp", default=2700, type=int)
    current_brightness = await room.getBrightness()
    new_brightness = max(0, current_brightness - 10)
    
    pb = PilotBuilder(colortemp=temp, brightness=new_brightness)
    
    await room.setAll(pb)
    return f'Brightness decremented to {new_brightness}'


if __name__ == '__main__':
    port = os.environ.get("PORT", "5000")
    port = int(port)
    app.run(host='0.0.0.0', port=port)


