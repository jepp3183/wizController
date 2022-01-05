import asyncio
from pywizlight import bulb, wizlight, PilotBuilder


class LightGroup:

    def __init__(self) -> None:
        self.lights = []

    def addLight(self, light: wizlight) -> None:
        self.lights.append(light)

    def addLightsFromFile(self, filename: str) -> None:
        with open(filename, 'r') as f:
            for line in f:
                self.addLight(wizlight(line.strip()))

    def removeLight(self, ip: str) -> None:
        for light in self.lights:
            if light.ip == ip:
                self.lights.remove(light)
                break

    async def setAll(self, pb: PilotBuilder) -> None:
        for light in self.lights:
            await asyncio.wait_for(light.turn_on(pb), timeout=5)

    async def turnOffAll(self) -> None:
        for light in self.lights:
            await asyncio.wait_for(light.turn_off(), timeout=5)

    async def turnOnAll(self) -> None:
        pb = PilotBuilder(colortemp=2700, brightness=255)
        await self.setAll(pb)

    async def toggleAll(self) -> None:
        for light in self.lights:
            await asyncio.wait_for(light.lightSwitch(), timeout=5)

