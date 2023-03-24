from fastapi import APIRouter, Request, Response, status

router = APIRouter(
    prefix="/base",
    tags=["base"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("")
async def base(request: Request):
    return Response()
