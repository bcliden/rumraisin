import io
from typing import Any
import zmq
from pathlib import Path

from PIL import Image as im
from PIL.Image import Image

from signal import signal, SIGINT, SIG_DFL

from base64 import b64decode, b64encode


"""
Tests to write...
- invalid hex colors values
- valid hex colors
    - # prefixed
    - non-# prefixed
    - mixed prefices
- missing one color/property
"""

# assuming we're at the project root
test_image = Path.cwd() / "tests" / "last_recieved_test_image.png"


def main() -> None:
    # maybe use argparser or something for host, port, etc

    host = "localhost"
    port = "8672"

    # please exit when someone presses ctrl+C
    signal(SIGINT, SIG_DFL)

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{host}:{port}")

    # quote = """
    # “Buy a man eat fish, he day,
    #  teach fish man, to a lifetime.”
    # """
    # quote = "Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old."
    # quote = """Traditionally, art has been for the select few. We have been brainwashed to believe that Michaelangelo had to pat you on the head at birth. Well, we show people that anybody can paint a picture that they're proud of -- Bob Ross"""
    # quote = "Has Anyone Really Been Far Even as Decided to Use Even Go Want to do Look More Like?"
    # socket.send_json({ "text": quote })
    # socket.send_json({"text": quote, "color": {"bg": "#FEF", "text": "#010"}})

    print(f"reading image file: {test_image}")
    with open(test_image, "rb") as f:
        data = f.read()
        b64data = b64encode(data).decode("ascii")
        print(f"sending {str(b64data[0:10])}... image")
        socket.send_json({"image": b64data})

    response: Any = socket.recv_json()

    print("recieved response: ", response)

    if response["status"] == "ok":
        img = response["image"]
        img_bytes = b64decode(img)

        parent_folder = Path(__file__).parent.resolve()
        with open(parent_folder / "last_recieved_test_image.png", "wb") as f:
            f.write(img_bytes)

        b = io.BytesIO(img_bytes)
        i: Image = im.open(b)
        i.show()


if __name__ == "__main__":
    main()
