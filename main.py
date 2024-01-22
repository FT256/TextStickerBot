import asyncio
import logging
from io import BytesIO

from PIL import Image, ImageFont, ImageDraw
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import BufferedInputFile

API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command('start', 'help'))
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Hi!\nI'm StickerBot!")


@dp.message()
async def upload_photo(message: types.Message):
    buf = generate_img(message=message.text)
    img = BufferedInputFile(file=buf.getbuffer().tobytes(), filename="image.png")
    await bot.send_sticker(chat_id=message.chat.id, sticker=img)
    buf.close()


def splitMessage(text: str):
    list = text.split('\n')
    longString =''
    scale = 0
    for string in list:
        if scale < len(string):
            scale = len(string)
            longString = string
    return longString


def generate_img(message: str):
    text = message
    fontSize = 75
    spacing = 10
    strings = len(text.split('\n'))
    textheight = strings*(fontSize+spacing)+spacing
    print(textheight)
    if textheight > 512:
        fontSize = int((512-spacing*(strings+2))/strings)
    print(fontSize)
    img = Image.new('RGB', (512, 512), color='black')
    fnt = ImageFont.truetype('./isocpeur.ttf', fontSize)
    length = fnt.getlength(splitMessage(message))
    if length > 512-spacing*2:
        scale = (512-spacing*2)/length
        fontSize = int(fontSize*scale)
        print(fontSize)
        fnt = ImageFont.truetype('./isocpeur.ttf', fontSize)
    d = ImageDraw.Draw(img)
    d.multiline_text((256, 256), text, font=fnt, fill=(255, 255, 255), anchor="mm", align="center", spacing=spacing)
    buf = BytesIO()
    img.save(buf, format='webp')
    buf.seek(0)
    return buf


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

