<h1>StelChzzkStatus</h1>
<p>내가 원하는 채널의 라이브 현황과 채널 바로가기를 제공하는 Telegram Bot 입니다.</p>

<h2>선행 작업</h2>
<p>텔레그램 봇과 네이버 성인 인증을 위하여 토큰이 필요합니다.</p>
<p>실행 파일과 동일한 경로에 파일 두 개를 만들어주세요.</p>

| 이름 | 설명 |
| ----| ---- |
| chzzk_cookies.json| 네이버 로그인 토큰이 저장됩니다. |
| telegram_token | 텔레그램에서 사용하는 봇 토큰입니다. |

<p>telegram_token 파일은 봇의 토큰을 한 줄로 넣어주시면 됩니다.</p>
<pre><code>1234567890:AAAAAAAxBBBBBB_ABX  
</code></pre>

<p>chzzk_cookies.json은 본인의 네이버 로그인 토큰이 필요합니다.</p>
<p>PC 브라우저에 로그인 된 상태에서 DevTools를 실행하여 응용 프로그램 > 쿠키에 있는 NID_AUT, NID_SES 항목을 찾아서 아래와 같이 만들어주세요.</p>
<pre><code>{
"NID_AUT": ["XXXXXXXXXXXXXXXXXXXX"],
"NID_SES": ["YYYYYYYYYYYYYYYYYYYY"]
}</code></pre>
<p>네이버 토큰이 없어도 작동은 하나, 연령 제한 방송이 표시되지 않을 수 있습니다.</p>

<p>SOOP 라이브 부분에서 사용되는 ChromeDriver는 절대 경로로 지정이 되어 있습니다.</p>
<p>해당 코드 제거 후 사용하지 않는 것을 권장하지만 사용하는 경우 서버에 ChromeDriver를 수동으로 설치해주세요.</p>
<p>그 다음 설치 경로를 본인이 설치한 경로로 변경하여 사용하시기 바랍니다.</p>

<h2>목적</h2>
<p>Python과 Telegram Bot이 어떤 식으로 동작하나 궁금해서 여러 자료를 참고하여 학습용으로 만든 봇입니다.</p>
