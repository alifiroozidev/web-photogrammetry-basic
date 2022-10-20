# meshroom-web
Web client to interact with the meshroom cli

# Commands
Start the flask webclient by running `python -m flask run` or `python -m flask run --host="0.0.0.0"` when running inside the container to make sure it is exposed to the host.
Start the websocket server by running `python websocket.py`.
Build the docker image by running `docker build -t <yourtag>`.
Run the docker image by running `docker -p 5000:5000 -p 5678:5678 -it run <yourtag>`. This runs the image interactively in which you can call the commands mentioned above. Port 5000 is exposed for the flask application. Port 5678 is exposed for the websocket server. Thus, `localhost:5000` for the web client, and `ws://127.0.0.1:5678` for the websocket.