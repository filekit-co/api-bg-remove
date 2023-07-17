from functools import lru_cache

from rembg import new_session


@lru_cache()
def get_onnx_session(IMAGE_MODEL):
    return new_session(IMAGE_MODEL)