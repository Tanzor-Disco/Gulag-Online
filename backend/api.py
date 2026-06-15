import fastapi
import pathlib
import asyncio

from fastapi import responses
from fastapi import staticfiles
from parser import TelegramParser
from db_manager import DBManager
from contextlib import asynccontextmanager


async def periodic_data_update():

    SLEEP_DURATION = 86400
    SLEEP_TEST = 5
    parser = TelegramParser()
    db_manager = DBManager()

    while True:
        try:
            print("Fetching new posts",flush=True)
            parsed_data = parser.get_parsed_data()
            db_manager.insert_parsed_data(parsed_data)
        except Exception as e:
            print(f"didn't fetch new posts {e}")
        finally:
            await asyncio.sleep(SLEEP_DURATION)

@asynccontextmanager
async def lifespan(app:fastapi.FastAPI):
    asyncio.create_task(periodic_data_update())
    yield

ROOT_PATH =pathlib.Path(__file__).resolve().parent.parent
app = fastapi.FastAPI(lifespan=lifespan)
app.mount("/images",staticfiles.StaticFiles(directory=ROOT_PATH/"frontend"/"images"),name="images")
app.mount("/static",staticfiles.StaticFiles(directory=ROOT_PATH/"frontend"/"static"),name="static-files")

@app.get("/")
def root():
    return responses.FileResponse(ROOT_PATH/"frontend"/"index.html")

    
@app.get("/api/data")
def export_data():
    db_manager = DBManager()
    try:
        data = db_manager.export()
        return data
    finally:
        db_manager.close()


if __name__ == "__main__":
    pass
