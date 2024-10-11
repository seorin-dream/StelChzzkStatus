import os
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests
import asyncio

token = "7616896847:AAFeYheTLiBQ0mq7Nxap5FyGbEWbsgYUyhk"
telegram_api_token = token
# 유출에 주의

class TelegramBotHandler:
    @classmethod
    async def stelstatus(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'

        channel_ids = {
            'f722959d1b8e651bd56209b343932c01': '칸나',
            '45e71a76e949e16a34764deb962f9d9f': '유니',
            'b044e3a3b9259246bc92e863e7d3f3b8': '히나',
            '4515b179f86b67b4981e16190817c580': '마시로',
            '4325b1d5bbc321fad3042306646e2e50': '리제',
            'a6c4ddb09cdb160478996007bff35296': '타비',
            '64d76089fba26b180d9c9e48a32600d9': '시부키',
            '516937b5f85cbf2249ce31b0ad046b0f': '린',
            '4d812b586ff63f8a2946e64fa860bbf5': '나나',
            '8fd39bb8de623317de90654718638b10': '리코'
        }
        result_list = [] # 저장된 결과가 담길 리스트

        for channel_id, channel_name in channel_ids.items():
            url = chzzk_url.format(channelID=channel_id)
            response = requests.get(url, headers=headers)

            data = response.json()  # HTML 쓰면 안된다고 JSON 데이터 파싱
            open_live_status = data['content']['openLive']

            if open_live_status:
                LiveStatus = f"{channel_name}: 📺 지금 방송 중이야!"
                result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야!"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        # await bot.send_message(chat_id="-4552916950", text=result_list_final)
        await update.message.reply_text(text=result_list_final)

if __name__ == "__main__":
    try:
        application = ApplicationBuilder().token(token).build()
        application.add_handler(CommandHandler('stelstatus', TelegramBotHandler.stelstatus))
        application.run_polling()
    except KeyboardInterrupt:
        pass
