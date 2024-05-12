from flask import Flask, jsonify
import asyncio

app = Flask(__name__)


async def background_task():
    while True:
        print("Doing background task...")
        await asyncio.sleep(1)


def start_async_tasks():
    loop = asyncio.get_event_loop()
    loop.create_task(background_task())


@app.route("/")
def index():
    return jsonify({"message": "Hello from Flask with asyncio!"})


if __name__ == "__main__":
    start_async_tasks()
    app.run(debug=True)
