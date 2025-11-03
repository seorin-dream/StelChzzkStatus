// CF Worker Telegram Webhook + chzzk status (Prev. Python code over Compute Engine)
// TELEGRAM_TOKEN  : Telegram bot token
// CHZZK_COOKIES : Encryption save -> {"NID_AUT":["KEY"],"NID_SES":["KEY"]}

export default {
  async fetch(request, env) {
    // Health check
    if (request.method === "GET") {
      return new Response("Telegram chzzk Worker running", { status: 200 });
    }

    // POST (Telegram Webhook)
    if (request.method !== "POST") {
      return new Response("Only POST (Telegram webhook) is supported.", { status: 405 });
    }

    let update;
    try {
      update = await request.json();
    } catch (e) {
      console.error("Invalid JSON body", e);
      return new Response("Bad request", { status: 400 });
    }

    const message = update.message || update.edited_message;
    const chatId = message?.chat?.id;
    const text = message?.text?.trim();

    if (!chatId || !text) {
      // Extension for Callback Query
      return new Response("No chat/message found", { status: 200 });
    }

    // User-Agent Header
    const UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36";

    // COOKIES HEADER
    let cookieHeader = "";
    try {
      const cookiesJson = env.CHZZK_COOKIES || "{}";
      const cookiesObj = JSON.parse(cookiesJson);
      cookieHeader = Object.entries(cookiesObj).map(([k, v]) => `${k}=${v}`).join("; ");
    } catch (e) {
      console.warn("CHZZK_COOKIES parse failed:", e);
      cookieHeader = "";
    }

    // Helper (send Message to Telegram)
    async function sendTelegram(chat_id, textBody) {
      try {
        await fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/sendMessage`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id,
            text: textBody,
            parse_mode: "Markdown",
            disable_web_page_preview: true
          })
        });
      } catch (e) {
        console.error("sendTelegram error:", e);
      }
    }

// Worker 코드 최상단이나 checkChannel 함수 옆에 추가
async function searchChzzkChannels(keyword, cookieHeader, UA) {
  const encodedKeyword = encodeURIComponent(keyword);
  const SEARCH_API_URL = `https://api.chzzk.naver.com/service/v1/search/channels?keyword=${encodedKeyword}`;
  const CHZZK_BASE_URL = 'https://chzzk.naver.com/';
  let channelList = [];

  try {
      const res = await fetch(SEARCH_API_URL, {
           headers: {
              "User-Agent": UA,
              ...(cookieHeader ? { "Cookie": cookieHeader } : {})
          }
      });

      // 오류 처리 로직
      if (!res.ok) {
          return `*검색 오류*: ⚠️ API 응답 실패 (${res.status})`;
      }
      
      const jsonResponse = await res.json();
      
      // 응답 구조 오류 처리 로직

      if (jsonResponse.code !== 200 || !jsonResponse.content || !jsonResponse.content.data) {
           return `*검색 오류*: API 응답 구조 오류입니다.`;
      }

      const channels = jsonResponse.content.data;

      // 🎯 변경된 핵심 로직: 상위 2개 채널만 선택
      const topChannels = channels.slice(0, 3);
        
      if (topChannels.length === 0) {
          return `*'${keyword}'* 에 대한 치지직 채널 검색 결과가 없습니다.`;
      }
      
      // 2. 선택된 채널 각각에 대해 상세 상태 (checkChannel) 조회
      const detailedResults = [];
      for (const item of topChannels) {
          const channelId = item.channel.channelId;
          const channelName = item.channel.channelName;
          
          // 💡 기존의 상세 상태 조회 함수(checkChannel)를 재활용합니다.
          const statusLine = await checkChannel(channelId, channelName);
          detailedResults.push(statusLine);
      }

      // 3. 최종 메시지 포맷팅
      const totalCount = channels.length; // 전체 검색 결과 수
      const resultCountMessage = totalCount > 3 ? ` (총 ${totalCount}개 중 상위 3개 표시)` : ``;
      
      const header = `*'${keyword}' 검색 결과${resultCountMessage}*`;

      return `${header}\n${detailedResults.join('\n')}`;

  } catch (err) {
      console.error("searchChzzkChannels error:", err);
      return `*${keyword}* 검색 중 오류 발생 (${err.message || err})`;
  }
}

    // check chzzk-live-status
async function checkChannel(channelId, channelName) {
  const baseUrl = `https://api.chzzk.naver.com/service/v1/channels/${channelId}`;
  const liveDetailUrl = `https://api.chzzk.naver.com/service/v2/channels/${channelId}/live-detail`;
  const channelWebUrl = `https://chzzk.naver.com/live/${channelId}`;
  const channelStationUrl = `https://chzzk.naver.com/${channelId}`;

  try {
    const res = await fetch(baseUrl, {
      headers: {
        "User-Agent": UA,
        ...(cookieHeader ? { "Cookie": cookieHeader } : {})
      }
    });

    if (!res.ok) {
      return `*${channelName}*: ⚠️ API 응답 실패 (${res.status})`;
    }

    const data = await res.json();
    const openLive = data?.content?.openLive;

    if (!openLive) {
      return `*${channelName}*: ❌ 방송 중 아님! [채널](${channelStationUrl})`;
    }

    // call live-detail during live
    const detailRes = await fetch(liveDetailUrl, {
      headers: {
        "User-Agent": UA,
        ...(cookieHeader ? { "Cookie": cookieHeader } : {})
      }
    });

    if (!detailRes.ok) {
      return `*${channelName}*: ⚠️ 상세정보 불러오기 실패 (${detailRes.status})`;
    }

    const detailJson = await detailRes.json();
    const content = detailJson?.content;
    const title = content?.liveTitle || "제목 없음";
    const liveCategoryValue = content?.liveCategoryValue || "N/A";

    // Check HLS-Location (in api-address)
    let hlsPath = null;
    try {
      const livePlaybackJson = content?.livePlaybackJson;
      const playback = typeof livePlaybackJson === "string" ? JSON.parse(livePlaybackJson) : livePlaybackJson;
      const medias = playback?.media || [];
      for (const m of medias) {
        if (m?.mediaId === "HLS" && m?.path) {
          hlsPath = m.path;
          break;
        }
      }
    } catch (e) {
      console.warn("playback parse failed:", e);
    }

    const isAdult = !!content?.adult;

    // inLive Message toast
    let msg = `*${channelName}*: 📺 ${title} (_${liveCategoryValue}_) [Web](${channelWebUrl})`;
    if (hlsPath) msg += ` [HLS](${hlsPath})`;
    if (isAdult) msg = `*${channelName}*: 🔞 ${title} (_${liveCategoryValue}_) [Web](${channelWebUrl})`;

    return msg;
  } catch (err) {
    console.error("checkChannel error:", err);
    return `*${channelName}*: ⚠️ 오류 발생 (${err.message || err})`;
  }
}

    // Channel Map (RAW data)
    const COMMAND_MAP = {
      "/stelstatus": {
        channels: {
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
      },
      "/aesther_status": {
        channels: {
          '4de764d9dad3b25602284be6db3ac647': '아리사',
          '32fb866e323242b770cdc790f991a6f6': '카린',
          '17d8605fc37fb5ef49f5f67ae786fe4e': '에리스',
          '475313e6c26639d5763628313b4c130e': '엘리'
        }
      },
      "/stardream_status": {
        channels: {
          '7ca6c5f45a9b16f75970f54c309623c0': '하나빈',
          'e984779fd445e71bfd8c99106e432bf1': '이루네',
          '4f650f02bc4ab38a998d74e3abb1b68b': '유레이',
          '91caa53fc6cf5ee3cdbc802bd23bf155': '온하얀'
        }
      },
      "/acaxia_status": {
        channels: {
          '3e3781d3bd20dadc2f6f6d5d30091195': '포포포포',
          '5c897b3e639045ca6e314bbaff991f73': '모네',
          'dae2de8eaa005a59163f2e4c045e1aa1': '로즈',
          'b33c957eac9335d38e4043c3dca97675': '하시요',
          'f36320c432d9f06095ce2cfbbf681c26': '류시호'
        }
      },
      "/stardays_status": {
        channels: {
          'a54372e8197f6d241a43a318279860d6': '나츠키',
          '0a2020b09b8cc7f2285b7ae5de2ce4d3': '테리'
        }
      },
      "/honeyz_status": {
        channels: {
          'c0d9723cbb75dc223c6aa8a9d4f56002': '허니츄러스',
          'abe8aa82baf3d3ef54ad8468ee73e7fc': '아야',
          'b82e8bc2505e37156b2d1140ba1fc05c': '담유이',
          '798e100206987b59805cfb75f927e965': '디디디용',
          '65a53076fe1a39636082dd6dba8b8a4b': '오화요',
          'bd07973b6021d72512240c01a386d5c9': '망내'
        }
      }
    };

    // channel rotation
    // 메시지에서 커맨드만 추출
    const command = text.split(' ')[0].split('@')[0]; // /stelstatus@stelbot -> /stelstatus

    if (COMMAND_MAP[command]) {
      const mapping = COMMAND_MAP[command].channels;
      const results = [];

      for (const [id, name] of Object.entries(mapping)) {
        const statusLine = await checkChannel(id, name);
        results.push(statusLine);
      }

      const finalText = results.join("\n");
      await sendTelegram(chatId, finalText);
      return new Response("OK", { status: 200 });
    }

    // all-channel status check
    if (command === "/allstatus") {
      const allResults = [];
      for (const cmd of Object.values(COMMAND_MAP)) {
        for (const [id, name] of Object.entries(cmd.channels)) {
          const statusLine = await checkChannel(id, name);
          allResults.push(statusLine);
        }
      }
      await sendTelegram(chatId, allResults.join("\n"));
      return new Response("OK", { status: 200 });
    }    

    // New: Chzzk Channel Search Logic
    if (command === "/chzzk") {
      const parts = text.split(' ');
      // 1. 명령어 잘라내기
      const keyword = parts.slice(1).join(' ').trim(); 

      if (!keyword) {
           await sendTelegram(chatId, "검색어를 입력해주세요. 사용 예시: `/chzzk 패리`");
           return new Response("No keyword", { status: 200 });
      }
      
      const searchResults = await searchChzzkChannels(keyword, cookieHeader, UA);
      
      await sendTelegram(chatId, searchResults);
      return new Response("Search OK", { status: 200 });
    }

    // exception
    await sendTelegram(chatId, "알 수 없는 명령어예요. 사용 가능한 명령어:\n/stelstatus\n/aesther_status\n/stardream_status\n/acaxia_status\n/stardays_status\n/honeyz_status\n/allstatus");
    return new Response("Unknown command", { status: 200 });
  }
};
