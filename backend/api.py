import asyncio
import pathlib
import os
from contextlib import asynccontextmanager
from parser import TelegramParser

import fastapi
from fastapi import responses, staticfiles

from dotenv import load_dotenv

from db_manager import DBManager

load_dotenv()
FETCH_PARAM = os.environ["FETCH_PARAM"]

async def periodic_data_update():
    db_manager = app.state.db
    SLEEP_DURATION = 86400
    SLEEP_TEST = 5
    parser = app.state.parser

    while True:
        try:
            print("Fetching new posts using timer", flush=True)
            parsed_data = parser.get_parsed_data()
            await db_manager.insert_parsed_data(parsed_data)
        except Exception as e:
            print(f"didn't fetch new posts {e}")
        finally:
            await asyncio.sleep(SLEEP_DURATION)


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    db_manager = await DBManager.connect()
    app.state.db = db_manager
    app.state.parser = TelegramParser()
    asyncio.create_task(periodic_data_update())
    yield
    await db_manager.pool.close()


ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent
app = fastapi.FastAPI(lifespan=lifespan)
app.mount("/images", staticfiles.StaticFiles(directory=ROOT_PATH / "frontend" / "images"), name="images")
app.mount("/static", staticfiles.StaticFiles(directory=ROOT_PATH / "frontend" / "static"), name="static-files")


@app.get("/")
def root():
    return responses.FileResponse(ROOT_PATH / "frontend" / "index.html")

@app.get("/api/data")
async def export_data(section:int = 0):
    db_manager = app.state.db
    data = await db_manager.export(section)
    return data

@app.get("/api/fetch")
async def fetch_data(fetch_param:str):
    if fetch_param != FETCH_PARAM:
        print("wrong parameter entered in /api/fetch")
        return 
    print("correct parameter entered in /api/fetch")

    db_manager = app.state.db
    parser = app.state.parser
    try:
        print("Fetching new posts using api/fetch", flush=True)
        parsed_data = parser.get_parsed_data()
        await db_manager.insert_parsed_data(parsed_data)
    except Exception as e:
        print(f"didn't fetch new posts {e}")


if __name__ == "__main__":
    pass
