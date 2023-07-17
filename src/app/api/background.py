import logging

import aiohttp
from asyncer import asyncify
from fastapi import APIRouter, File, Query, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from rembg import remove

from app.exceptions import InternalServerError, InvalidImageUrl
from consts import IMAGE_MODEL
from infra.u2net import get_onnx_session
from utils import generate_chunks

router = APIRouter(prefix='/bg')

def im_without_bg(file_bytes) -> Response:
    img = remove(file_bytes, alpha_matting=True, session=get_onnx_session(IMAGE_MODEL))
    return img

@router.get(
        path="/remove",
        tags=["Background Removal"],
        summary="Remove from URL",
        description="Removes the background from an image obtained by retrieving an URL.",
    )
async def get_index(
        url: str = Query(
            default=..., description="URL of the image that has to be processed."
        ),
    ):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_bytes = await response.read()
                processed_image = await asyncify(im_without_bg)(file_bytes)
                return StreamingResponse(generate_chunks(processed_image), media_type="image/png")
    except aiohttp.InvalidURL as e:
        logging.error(e)
        raise InvalidImageUrl(url)
    except aiohttp.ClientError as e:
        # aiohttp 클라이언트 에러 처리
        # 예: 네트워크 연결 실패, 요청 시간 초과 등
        logging.error(f"Aiohttp ClientError: {str(e)}")
        raise e        
    except Exception as e:
        raise InternalServerError(str(e))



@router.post(
        path="/remove",
        summary="Remove from Stream",
        description="Removes the background from an image sent within the request itself.",
        status_code=status.HTTP_200_OK,
        )
async def remove_background(
        image: UploadFile=File(...),
    ):
    file_bytes = await image.read()
    processed_image =  await asyncify(im_without_bg)(file_bytes)
    return StreamingResponse(generate_chunks(processed_image), media_type="image/png")
