import os
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Telegram bot token
token = "7616896847:AAFeYheTLiBQ0mq7Nxap5FyGbEWbsgYUyhk"
telegram_api_token = token

class TelegramBotHandler:
    # Handler for the /stelstatus command (First service)
    @classmethod
    async def stelstatus(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (first service)
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
        result_list = []  # Save results for first service

        for channel_id, channel_name in channel_ids.items():
            url = chzzk_url.format(channelID=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                LiveStatus = f"{channel_name}: 📺 지금 방송 중이야!"
                result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야!"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final)

    # Handler for the /stardays_status command (Second service)
    @classmethod
    async def stardays_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (second service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'

        channel_ids = {
            'a54372e8197f6d241a43a318279860d6': '나츠키',
            '3a2d2f4e9132d822423f6aa879e598c5': '반',
            '0a2020b09b8cc7f2285b7ae5de2ce4d3': '테리'
        }
        result_list = []  # Save results for second service

        for channel_id, channel_name in channel_ids.items():
            url = chzzk_url.format(channelID=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                LiveStatus = f"{channel_name}: 📺 지금 방송 중이야!"
                result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야!"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final)

    # Handler for the /honeyz_status command (3rd service)
    @classmethod
    async def honeyz_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (3rd service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'

        channel_ids = {
            'c0d9723cbb75dc223c6aa8a9d4f56002': '허니츄러스',
            'abe8aa82baf3d3ef54ad8468ee73e7fc': '아야',
            'b82e8bc2505e37156b2d1140ba1fc05c': '담유이',
            '798e100206987b59805cfb75f927e965': '디디디용',
            '65a53076fe1a39636082dd6dba8b8a4b': '오화요',
            'bd07973b6021d72512240c01a386d5c9': '망내'
        }
        result_list = []  # Save results for 3rd service

        for channel_id, channel_name in channel_ids.items():
            url = chzzk_url.format(channelID=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                LiveStatus = f"{channel_name}: 📺 지금 방송 중이야!"
                result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야!"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final)

    # Handler for the /isedolstatus command (AfreecaTV using Selenium)
    @classmethod
    async def isedolstatus(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 2: Checking live status using Selenium (AfreecaTV channels)
        afreeca_channel_ids = {
            'jingburger1': '징버거',
            'inehine': '아이네',
            'lilpa0309': '릴파',
            'cotton1217': '주르르',
            'gosegu2': '고세구',
            'viichan6': '비챤'
        }

        result_list = []  # Save results for AfreecaTV

        # Set up Selenium (Edge options)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
        chrome_options.add_argument("--no-sandbox")  # Recommended for running as root
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional)

        # ChromDriver path
        webdriver_service = ChromeService('/home/pmh10132000/chromedriver-linux64/chromedriver')

        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        # Iterate through AfreecaTV channels
        for channel_id, channel_name in afreeca_channel_ids.items():
            url = f'https://bj.afreecatv.com/{channel_id}'
            driver.get(url)
            try:
                onAir_box = driver.find_element(By.CLASS_NAME, 'onAir_box')
                LiveStatus = f"{channel_name}: 📺 지금 방송 중이야!"
                result_list.append(LiveStatus)
            except NoSuchElementException:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야!"
                result_list.append(LiveStatus)

        # Close the Selenium driver after use
        driver.quit()

        # Combine results and send them back to the user
        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final)

if __name__ == "__main__":
    try:
        # Initialize the application
        application = ApplicationBuilder().token(token).build()

        # Add both handlers
        application.add_handler(CommandHandler('stelstatus', TelegramBotHandler.stelstatus))
        application.add_handler(CommandHandler('stardays_status', TelegramBotHandler.stardays_status))
        application.add_handler(CommandHandler('honeyz_status', TelegramBotHandler.honeyz_status))
        application.add_handler(CommandHandler('isedolstatus', TelegramBotHandler.isedolstatus))

        # Start the bot
        application.run_polling()
    except KeyboardInterrupt:
        pass
