import asyncio
import os

import asyncpg
from dotenv import load_dotenv

load_dotenv()
URI = os.environ.get("URI")
if not URI:
    raise ValueError("URI is not set")


class DBManager:
    def __init__(self, pool):
        self.pool = pool

    @classmethod
    async def connect(cls):
        pool = await asyncpg.create_pool(URI)
        return cls(pool)

    async def _create_table(self):
        async with self.pool.acquire() as con:
            await con.execute("""
            CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            post_id TEXT UNIQUE,
            post_date DATE,
            author TEXT,
            post_content TEXT
            ); 
            """)

    async def insert_parsed_data(self, parsed_data: list[dict]):
        async with self.pool.acquire() as con:
            for post_dict in parsed_data:
                post_id = post_dict["id"]
                post_author = post_dict["author"]
                post_content = post_dict["text"]
                post_date = post_dict["date"]

                await con.execute(
                    """
                INSERT INTO posts (post_id,post_date,author,post_content)
                VALUES ($1,$2,$3,$4)
                ON CONFLICT (post_id) DO NOTHING
                """,
                    post_id,
                    post_date,
                    post_author,
                    post_content,
                )
    
    async def insert_one(self, post_id, date, author, content):
        async with self.pool.acquire() as con:
            await con.execute(
                """
            INSERT INTO posts (post_id,post_date,author,post_content)
            VALUES ($1,$2,$3,$4)
            ON CONFLICT (post_id) DO NOTHING
            """,
                post_id,
                date,
                author,
                content,
            )

    async def clear_table(self):
        async with self.pool.acquire() as con:
            await con.execute("""
            DELETE FROM posts
            """)

    async def export(self):
        async with self.pool.acquire() as con:
            rows = await con.fetch("""
            SELECT * FROM posts
            """)
        return [dict(row) for row in rows]


async def main():
    test = await DBManager.connect()
    await test._create_table()
    res = await test.export()
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
