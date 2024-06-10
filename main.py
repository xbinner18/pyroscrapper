import logging
import re
import requests
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from bs4 import BeautifulSoup as bs
from platform import python_version
from pyrogram.errors import FloodWait


API_ID = input("api_id=> ")
API_HASH = input("api_hash=> ")
CHANNEL_USERNAME = str(input("channel_username=> "))

app = Client("my_account", API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)


@app.on_message(filters.command(["alive", "start"], ".") & filters.me)
async def module_alive(client: Client, message: Message):
    await message.edit(f"**Userbot working fine**\n**Python:** {python_version()}")


@app.on_message()
async def my_handler(client, message):
    if re.match(r'\d{15,16}', str(message.text)):
        BIN = re.search(r'\d{15,16}', str(message.text))[0][:6]
        r = requests.get(f'https://bins.ws/search?bins={BIN}')
        soup = bs(r.text, features='html.parser')
        k = soup.find("div", {"class": "page"})
        MSG = f"""
{message.text}

{k.get_text()[62:]}
"""
        try:
            await app.send_message(CHANNEL_USERNAME, MSG)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await app.send_message(CHANNEL_USERNAME, MSG)

            
app.run()
