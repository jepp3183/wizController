import asyncio
from pywizlight import discovery
from pywizlight.bulb import wizlight


class BulbFinder:
    def __init__(self, broadcast_space):
        self.broadcast_space = broadcast_space
        self.lights = []

    async def findBulbs(self) -> list[wizlight]:
        self.lights = await discovery.discover_lights(broadcast_space=self.broadcast_space)
        return self.lights

    def printBulbsToFile(self, filename) -> None:
        with open(filename, 'w') as f:
            for light in self.lights:
                f.write(light.ip + '\n')