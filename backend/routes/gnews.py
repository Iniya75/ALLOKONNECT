from fastapi import APIRouter
from workflows.news_workflow import run_news_workflow

router = APIRouter()

@router.get("/news")
def get_news():

    return run_news_workflow()