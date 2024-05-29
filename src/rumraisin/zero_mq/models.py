from typing import Annotated, Literal

from PIL.Image import Image
from pydantic import BaseModel, Field, PlainValidator, PlainSerializer

from rumraisin.serialization.image import encode_jpeg, decode


class Request(BaseModel):
    image: Annotated[Image, PlainValidator(decode)]
    intensity: Annotated[int, Field(ge=0, le=150, default=100)]

    class Config:
        # so pydantic won't panic about Image
        arbitrary_types_allowed = True


class SuccessReply(BaseModel):
    status: Literal["ok"] = "ok"
    image: Annotated[Image, PlainSerializer(lambda i: encode_jpeg(i))]

    class Config:
        # so pydantic won't panic about Image
        arbitrary_types_allowed = True


class ErrorReply(BaseModel):
    status: Literal["error"] = "error"
    message: str
