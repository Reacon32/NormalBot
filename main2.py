from aiogram import Bot, Dispatcher, types, executor
from NeiroImages.main import generate_image
from NeiroImages.neiro_assistent import get_response
from NeiroImages.neiro_consult import get_sovet

Api = '7397505038:AAEybXzkntQkyry2d63MPOBH8VC9Gz53DYU'
bot = Bot(token= Api)
dp = Dispatcher(bot)

@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.answer('Привет! Я нейронка импорто-замещения, которая может генироривоть изображения, а также давать советы')

@dp.message_handler(commands='sovet')
async  def analize_message(message:types.Message):
    user = message.get_args()
    response_text = await get_sovet(user)
    await message.answer(response_text)

@dp.message_handler(commands='generate_image')
async def handle_message(message: types.Message):
    user = message.get_args()
    response_text = await get_response(user)
    user_text = response_text
    await message.reply(f"Вот твой улучшенный промпт {user_text}")
    print(user_text)
    await message.reply('Ожидайте, изображение скоро появится')

    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as  e:
        await message.reply(f"Бот затупил: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)