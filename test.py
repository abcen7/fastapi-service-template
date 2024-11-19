import asyncio

import asyncpg


async def test_connection():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="postgres",
            database="fst_db",
            host="localhost",
            port=5432,
        )

        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")


asyncio.run(test_connection())
