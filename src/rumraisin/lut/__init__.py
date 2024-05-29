import importlib
import logging
from importlib.resources import as_file, files
from typing import Optional
from pillow_lut import load_cube_file
from PIL.ImageFilter import Color3DLUT

logger = logging.getLogger(__name__)


def load_all_luts_into_memory() -> None:
    current_module = importlib.import_module(__name__)

    for entry in files("rumraisin.lut").iterdir():
        if not entry.is_file():
            continue
        with as_file(entry) as file:
            if file.suffix != ".cube":
                continue
            logger.info(f'loading "{file.stem}" LUT into memory')
            setattr(
                current_module,
                file.stem.lower(),
                load_cube_file(file.read_text().splitlines()),
            )


# load_all_luts_into_memory()

luts: dict[str, Color3DLUT] = dict()


def get_lut(name: str) -> Optional[Color3DLUT]:
    if name in luts:
        logger.info("found %s LUT in cache", name)
        return luts[name]
    try:
        contents = files("rumraisin.lut").joinpath(f"{name}.cube").read_text()
        lut = load_cube_file(contents.splitlines())
        luts[name] = lut
        logger.info("loaded %s LUT from file", name)
    except FileNotFoundError:
        logger.warn("couldn't load LUT: %s", name)
        raise SystemError(f"Couldn't load filter named: {name}")
    return lut
