import time
import requests
import base64
from random import randint
from aiogram import Bot, Dispatcher, types, executor

Api = '7397505038:AAEybXzkntQkyry2d63MPOBH8VC9Gz53DYU'
bot = Bot(token= Api)
dp = Dispatcher(bot)

@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.answer('Привет! Я нейронка импорто-замещения, которая может генироривоть изображения')

def generate_image(prompt_text):
    prompt = {
        "modelUri": "art://b1gok529us99nbhikhqq/yandex-art/latest",
        "generationOptions": {
          "seed": randint(10, 10000000)
        },
        "messages": [
          {
            "weight": 1,
            "text": prompt_text
          }
        ]
        }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"

    headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key AQVN1Oo7XJ2sOFNIiD1J0pPHf5r0TsQxqY94vnOK"
        }

    response = requests.post(url= url, headers= headers, json= prompt)
    result = response.json()
    print(result)

    operation_id = result['id']

    operation_url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"

    while True:
        operation_response = requests.get(url= operation_url, headers= headers)
        operation_result = operation_response.json()
        if 'response' in operation_result:
            image_base64 = operation_result['response']['image']
            image_data = base64.b64decode(image_base64)
            return image_data
        else:
            print('Ожидайте, изображение скоро появится')
            time.sleep(5)

@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    await message.reply('Ожидайте, изображение скоро появится')

    try:
        image_data = generate_image(user_text)
        await message.reply_photo(photo= image_data)
    except Exception as  e:
        await message.reply(f"Бот затупил: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)