from random import choice
from typing import Callable, Optional, final, TypedDict, Literal, Type
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageFilter import Color3DLUT
from PIL import ImageFont as imf
from rumraisin.lut import get_lut
from pillow_lut import amplify_lut

picks: dict[str, Optional[Color3DLUT]] = {
    "Old": get_lut("Faded"),  # or Tweed or Pasadena?
    "Vibrant": get_lut("Teigen"),  # or Magic Hour?
    "B&W": get_lut("SoftBlackAndWhite"),  # or Zeke?
}

font = imf.load_default(60)


def process_lut(name: str) -> Callable[[Image, float], Image]:
    if name not in picks:
        raise SystemError(f"Invalid LUT: '{name}'")

    lut = picks[name]

    def process_image(image: Image, intensity: float) -> Image:
        amplified = amplify_lut(lut, intensity)
        image = image.filter(amplified)
        draw = ImageDraw(image)
        # TODO/bcl: not working rn
        draw.text(xy=(10, 10), text=name, font=font, fill="white", stroke_fill="black")
        return image

    return process_image


antique = process_lut("Old")


def random_filter(image: Image, intensity: float) -> Image:
    name = choice(list(picks.keys()))
    return process_lut(name)(image, intensity)
