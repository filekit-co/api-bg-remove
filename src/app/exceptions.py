from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class InternalServerError(HTTPException):
    def __init__(
            self,
            msg: str = 'Internal server error',
            headers: Optional[Dict[str, Any]] = None,
        ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg,
            headers=headers
        )




class InvalidImageUrl(HTTPException):
    def __init__(
            self,
            url: str,
            headers: Optional[Dict[str, Any]] = None,
        ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image url is given url:{url}",
            headers=headers
        )

