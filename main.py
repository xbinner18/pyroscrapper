import logging
import re
import requests
import asyncio

from pyrogram import Client, filters
from bs4 import BeautifulSoup as bs
from pyrogram.errors import FloodWait


API_ID = input("api_id=> ")
API_HASH = input("api_hash=> ")

app = Client("my_account", API_ID, API_HASH)

logging.basicConfig(level=logging.INFO)


@app.on_message()
async def my_handler(client, message):
    me = await app.get_me()
    # if message.peer_id == me.id: # skip cards if sending from client
        # return
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
            await app.send_message("rescrape", MSG) # set your channel username where you want cards should get posted i have set rescrape
        except FloodWait as e:
            await asyncio.sleep(e.value)

            
app.run()
