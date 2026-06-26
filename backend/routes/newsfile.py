import json
from fastapi import APIRouter

router = APIRouter()

@router.get("/saved-news")
def get_saved_news():

    with open(
        "output/news.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)