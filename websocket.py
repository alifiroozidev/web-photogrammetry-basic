# Include our application
import asyncio
import websockets
import json
from app.lib.meshroom import Meshroom
from os import path
from functools import partial

async def pipe(websocket, output):
    """Pipe the output of a meshroom run to a websocket"""
    await websocket.send(output)

async def consumer(websocket, message):
    """
    Consumer callback called when the websocket server receives a message.
    It is expected that every message is a JSON string.
    """

    # Decode the incoming message to a dictionary
    message = json.loads(message)

    # Bind the websocket as first parameter to the pipe function so it only
    # accepts a single argument, which allows us to pass it to the run method
    wspipe = partial(pipe, websocket)

    # Handle a run request, at which we want to start a new meshroom process
    if (message['type'] == 'run'):

        # Set up a new meshroom process
        m = Meshroom(path.join('model', 'input'), path.join('model', 'output'))
        await m.run(path.join('model', 'default.json'), pipe=wspipe)

async def consumer_handler(websocket, path):
    """Handler that installs a callback for when the websocket server receives a message"""
    async for message in websocket:
        await consumer(websocket, message)

# Define the ip address and port at which to run the websocket server
ip = '0.0.0.0'
port = 5678

# Run the websocket server at the designated ip address and port
print(f"starting websocket server at {ip}:{port}")
server = websockets.serve(consumer_handler, ip, port)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
