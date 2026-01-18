# """
# FastAPI routes for metadata API.
# """

# from fastapi import APIRouter, HTTPException
# from app.scraper import fetch_work
# from app.cache import get_cached, set_cache
# from app.models import WorkResponse

# router = APIRouter()


# @router.get("/work/{work_id}", response_model=WorkResponse)
# async def get_work(work_id: str):
#     """Fetch metadata for a specific work_id, using cache if possible."""
#     cached = get_cached(work_id)
#     if cached:
#         return cached

#     try:
#         data = await fetch_work(work_id)
#         set_cache(work_id, data)
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool
from app.scraper import fetch_work_sync

router = APIRouter(prefix="/api/v1")


@router.get("/work/{work_id}")
async def get_work(work_id: str):
    """
    Fetch work data via sync scraper in a threadpool.
    Solves Playwright asyncio issue on Windows.
    """
    try:
        return await run_in_threadpool(fetch_work_sync, work_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
