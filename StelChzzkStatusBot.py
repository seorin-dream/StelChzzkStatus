import os
import telegram
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# Telegram bot token
with open('telegram_token', 'r') as file:
    token = file.read().strip()
telegram_api_token = token
print(telegram_api_token)

# Chzzk Adult Token
cookies_file = json.loads(Path('chzzk_cookies.json').read_text())
chzzk_cookies = {key: value[0] for key, value in cookies_file.items()}

class TelegramBotHandler:
    # Handler for the /stelstatus command (First service)
    @classmethod
    async def stelstatus(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (first service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

        channel_ids = {
            '45e71a76e949e16a34764deb962f9d9f': '유니',
            '36ddb9bb4f17593b60f1b63cec86611d': '후야',
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
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers, cookies=chzzk_cookies)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                    
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

    # Handler for the /aesther_status command (Second service)
    @classmethod
    async def aesther_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (second service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

        channel_ids = {
            '4de764d9dad3b25602284be6db3ac647': '아리사',
            '32fb866e323242b770cdc790f991a6f6': '카린',
            '17d8605fc37fb5ef49f5f67ae786fe4e': '에리스',
            '475313e6c26639d5763628313b4c130e': '엘리'
        }
        result_list = []  # Save results for second service

        for channel_id, channel_name in channel_ids.items():

            url = chzzk_url.format(channelID=channel_id)
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

    # Handler for the /stardream_status command (Second service)
    @classmethod
    async def stardream_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (second service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

        channel_ids = {
            '7ca6c5f45a9b16f75970f54c309623c0': '하나빈',
            'e984779fd445e71bfd8c99106e432bf1': '이루네',
            '4f650f02bc4ab38a998d74e3abb1b68b': '유레이',
            '91caa53fc6cf5ee3cdbc802bd23bf155': '온하얀'
        }
        result_list = []  # Save results for second service

        for channel_id, channel_name in channel_ids.items():

            url = chzzk_url.format(channelID=channel_id)
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

    # Handler for the /acaxia_status command (Second service)
    @classmethod
    async def acaxia_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (second service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

        channel_ids = {
            '3e3781d3bd20dadc2f6f6d5d30091195': '포포포포',
            '5c897b3e639045ca6e314bbaff991f73': '모네',
            'dae2de8eaa005a59163f2e4c045e1aa1': '로즈',
            'b33c957eac9335d38e4043c3dca97675': '하시요',
            'f36320c432d9f06095ce2cfbbf681c26': '류시호'
        }
        result_list = []  # Save results for second service

        for channel_id, channel_name in channel_ids.items():

            url = chzzk_url.format(channelID=channel_id)
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

    # Handler for the /stardays_status command (Second service)
    @classmethod
    async def stardays_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (second service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

        channel_ids = {
            'a54372e8197f6d241a43a318279860d6': '나츠키',
            '0a2020b09b8cc7f2285b7ae5de2ce4d3': '테리'
        }
        result_list = []  # Save results for second service

        for channel_id, channel_name in channel_ids.items():

            url = chzzk_url.format(channelID=channel_id)
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

    # Handler for the /honeyz_status command (3rd service)
    @classmethod
    async def honeyz_status(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        bot = telegram.Bot(token)

        # Part 1: Checking live status using requests (3rd service)
        headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
        chzzk_url = 'https://api.chzzk.naver.com/service/v1/channels/{channelID}'
        chzzk_ch_live_url = 'https://chzzk.naver.com/live/{channelID}'
        chzzk_station_url = 'https://chzzk.naver.com/{channelID}'
        chzzk_live_url = 'https://api.chzzk.naver.com/service/v2/channels/{channel_api_id}/live-detail'

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
            channel_url = chzzk_ch_live_url.format(channelID=channel_id)
            station_url = chzzk_station_url.format(channelID=channel_id)
            api_url = chzzk_live_url.format(channel_api_id=channel_id)
            response = requests.get(url, headers=headers)
            data = response.json()

            open_live_status = data['content']['openLive']
            if open_live_status:
                api_response = requests.get(api_url, headers=headers, cookies=chzzk_cookies)
                api_data = api_response.json()
                api_content_data = api_data["content"]
                api_livePlayback_data = api_content_data["livePlaybackJson"]
                if api_content_data["adult"]:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 연령 제한 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
                else:
                    playback = json.loads(api_livePlayback_data)
                    for media in playback["media"]:
                        if media["mediaId"] == "HLS":
                            HLS_Address = media["path"]
                            LiveStatus = f"{channel_name}: 📺 지금 방송 중이야! [Web]({channel_url}) [HLS]({HLS_Address})"
                            result_list.append(LiveStatus)
            else:
                LiveStatus = f"{channel_name}: ❌ 방송 중이 아니야! [채널]({station_url})"
                result_list.append(LiveStatus)

        result_list_final = '\n'.join(result_list)
        print(result_list_final)
        await bot.send_message(chat_id=update.message.chat_id, text=result_list_final, parse_mode= 'Markdown', disable_web_page_preview=True)

if __name__ == "__main__":
    try:
        # Initialize the application
        application = ApplicationBuilder().token(token).build()

        # Add both handlers
        application.add_handler(CommandHandler('stelstatus', TelegramBotHandler.stelstatus))
        application.add_handler(CommandHandler('aesther_status', TelegramBotHandler.aesther_status))
        application.add_handler(CommandHandler('stardream_status', TelegramBotHandler.stardream_status))
        application.add_handler(CommandHandler('stardays_status', TelegramBotHandler.stardays_status))
        application.add_handler(CommandHandler('honeyz_status', TelegramBotHandler.honeyz_status))
        application.add_handler(CommandHandler('acaxia_status', TelegramBotHandler.acaxia_status))

        # Start the bot
        application.run_polling()
    except KeyboardInterrupt:
        pass
