import asyncio
import logging
import shelve
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
db_file = 'users.db'

FONT = './сhococooky.ttf'


@dp.message(Command('start', 'help'))
async def send_welcome(message: types.Message):
    """
    This handler will be called when client send `/start` or `/help` commands.
    """
    await message.reply("Привет!\nЭто StickerBot!\nНапиши любой текст, и я сделаю из него стикер")


@dp.message(Command('bgcolor'))
async def bgcolor_change(message: types.Message):
    list = message.text.split(' ', 1)
    try:
        color = list[1]
    except IndexError:
        await message.reply("Укажите цвет в HEX формате!\nНапример /bgcolor #F0F0F0")
        return
    await message.reply(color)


@dp.message(Command('ftcolor'))
async def ftcolor_change(message: types.Message):
    color = message.text.split(' ', 1)[1]
    await message.reply(color)


@dp.message()
async def upload_photo(message: types.Message):
    getbuf = asyncio.create_task(generate_img(message=message.text))
    buf = await getbuf
    img = BufferedInputFile(file=buf.getbuffer().tobytes(), filename="image.png")
    print('start upload')
    await bot.send_sticker(chat_id=message.chat.id, sticker=img)
    print('complete upload')
    buf.close()


def split_message(text: str):
    strings = text.split('\n')
    longstring = ''
    scale = 0
    for string in strings:
        if scale < len(string):
            scale = len(string)
            longstring = string
    return longstring


async def generate_img(message: str, bgcolor=(0, 0, 0, 255), fontcolor=(255, 255, 255), transparency=0):
    text = message
    font_size = 75
    spacing = 10
    strings = len(text.split('\n'))
    textheight = strings * (font_size + spacing) + spacing
    if textheight > 512:
        font_size = int((512 - spacing * (strings + 2)) / strings)
    fnt = ImageFont.truetype(FONT, font_size)
    length = fnt.getlength(split_message(message))
    if length > 512 - spacing * 2:
        scale = (512 - spacing * 2) / length
        font_size = int(font_size * scale)
        fnt = ImageFont.truetype(FONT, font_size)
    if transparency == 1:
        imgheight = textheight + font_size
        bgcolor = (0, 0, 0, 0)
    else:
        imgheight = 512
    print(imgheight)
    img = Image.new('RGBA', (512, imgheight), color=bgcolor)
    d = ImageDraw.Draw(img)
    d.multiline_text((256, imgheight / 2), text, font=fnt, fill=fontcolor, anchor="mm", align="center", spacing=spacing)
    buf = BytesIO()
    img.save(buf, format='webp')
    buf.seek(0)
    return buf


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
