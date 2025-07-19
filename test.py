import requests

cookies = {
    '_ga': 'GA1.1.1855182800.1746830870',
    'FPID': 'FPID2.2.sS%2B7ynyR7tMpLFcvmXy4C4cnwaQ4gwD%2B9T1jF%2FbXtT4%3D.1746830870',
    'LC': '"co=US"',
    'CTK': '1is6v07e4pfab800',
    'CSRF': 'dAs5p5u5czyMuRqTSORzdeC65EPnOFKC',
    'INDEED_CSRF_TOKEN': 'HHDpsE0T5V85IYCJYumNhWGvFM2aGJL5',
    '_cfuvid': '9AJ7Ya0aIU4Kix8XV.F8kC09jSA4oymushlLr8fX0oA-1752940573437-0.0.1.1-604800000',
    'SURF': '4dYws0tSnCeH7up1cW9hbMSMIjjo77cu',
    'FPLC': 'O3yH18Bt2w%2FS23mOIMzo2s0yW01%2B%2FH2ZKQfs2%2B2BidCAb7nIke6KQojZE501eHd66Rn9VbxVe76Gcyo1mA2bJ32csK1AvlKyI9XgcfVC3VxOCf7in%2BuSnT9ct%2Fh04g%3D%3D',
    'MICRO_CONTENT_CSRF_TOKEN': 'y4sIO7qpcPSIMzcikisxYkbawdPhEpHh',
    'SHARED_INDEED_CSRF_TOKEN': 'HHDpsE0T5V85IYCJYumNhWGvFM2aGJL5',
    'ENC_CSRF': 'hyMk4kc7kgCObMbx0xz4Ad5xOfhtp5KO',
    'LOCALE': 'en',
    'indeed_rcc': 'LOCALE:PREF:LV:CTK:RQ',
    'WHERE_RQ': '-1970622650|1752945266094',
    'LOCALE': 'en_US',
    'PREF': '"TM=1752947903117:L="',
    'SOCK': '"NquCpCbYDzAX5H4EnLhWUEyxM28="',
    'SHOE': '"JZ7E8fm4NuEsGQ-k40Q_9yp4n6KVnwoGakMfZmcoFvP9GuNlo27BWwxjUDP7QzEzZc_MWrce7T3wE9z39YVyyN7u0LbZu19VwxrEOiYgFcUc2zMeGCoa6ftFfwaHZMnd5YYoZtAHF_QJFsmMSZmTtf5LhB0tKg=="',
    'CO': 'US',
    'indeed_rcc': 'CTK',
    'ROJC': '82a5951d939179d1:369869a4bd896e3a:18910d65a40daa46:bcf4bc0bdfa1a68c',
    '__cf_bm': 'QDKGWsDZ68qw6L_C5HoaOFGpZGFkrs7msIOzPP35tls-1752962590-1.0.1.1-GiPLPbfykcJG2AI2PxunwKKiDDQnn15fbhbWBNjs0ZlwU8.SNNPE5n3aXqHLFCSrnCO29ZZcFKqC0HM5FTVd8JMrHzI_KPGnKpn7CQGSbUQ',
    'LV': 'LA=1752962594:LV=1752952596:CV=1752962594:TS=1746830866',
    'cf_clearance': '9sFnlSmcZeb4jKTNlAJ3nEMPvQ7b_wlWCokqNl2wqGU-1752962595-1.2.1.1-jSH2j6BI7UEkSOqqIs76drYS67j1Rb4KgcAc9MVvkUZOrNoklBEgnb6CelpbPgVPJoQc9yeB.uv5WfU.MfBxfjdldba.YLA9mMza3XZ35PKTIEIFwz20BS0Ba5lPADwnMsYVWOUDiFEfSddV7hqXhXRQVfBkHVQ45nlfDG.8oRbE_AHvMjs.6J3vhu0mfnWKX4vVxPMW65PrBHURW2KG6UYWBXg.MTeP.1wr.U_v83j_DatqykQ9N_oOX5SQFh8T',
    'RSJC': '4a95f087c7a6037d:82d26a5a325b5ce4:dd496529f083fa80',
    'VJP': '"jk=4a95f087c7a6037d&q=python&tk=1j0ibctqk269q044&from=web&advn=7831672186689475"',
    'RQ': 'q=python&l=Provo%2C+UT&latLong=40.23384%2C-111.65853&ts=1752962606964&pts=1752953001305&locString=Provo%2C+UT:q=python&l=&ts=1752953001305&locString=Provo%2C+UT:q=programmer&l=Provo%2C+UT&latLong=40.23384%2C-111.65853&radius=35&ts=1752948246008&locString=Provo%2C+UT:q=python&l=Provo%2C+UT&radius=35&ts=1752947789884:q=&l=Provo%2C+UT&ts=1752940588877',
    'PPID': 'eyJraWQiOiI3OGFjNzFmNC04MDhjLTRjYTItOTI4NC0xYmRjNzIzMDliYzIiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiIxMDNmNzJhYzNkYzJjNWZhIiwibGFzdF9hdXRoX3RpbWUiOjE3NTI5NDgxNTIyMTMsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaG9uZV9zY29wZSI6W10sImF1dGgiOiJlbWFpbE90cCIsImNyZWF0ZWQiOjE3NTI5NDUxMjgwMDAsImlzcyI6Imh0dHBzOi8vc2VjdXJlLmluZGVlZC5jb20iLCJsYXN0X2F1dGhfbGV2ZWwiOiJXRUFLIiwibG9nX3RzIjoxNzUyOTQ4MTUyMjEzLCJhcmJfYWNwdCI6ZmFsc2UsImF1ZCI6ImMxYWI4ZjA0ZiIsInBob25lX3ZlcmlmaWVkIjp0cnVlLCJyZW1fbWUiOnRydWUsInBob25lX251bWJlciI6IisxNzA2Mzg5MDA2NyIsImV4cCI6MTc1Mjk2NDQwNywiaWF0IjoxNzUyOTYyNjA3LCJlbWFpbCI6ImluZGVlZEBteWszbGUuY29tIn0.qInt02-D7FXeUnswtpLxkpqe_jGigx5xiFje05AX3bxt_s2j9uprCKJuv-6GtnthPcMZXwUY3pdXCNSoUQSMIw',
    'JSESSIONID': 'node018rbfdtj5pzzsx1k7j5hrglvq783598.node0',
    '_ga_LYNT3BTHPG': 'GS2.1.s1752962604$o6$g1$t1752962616$j48$l0$h549703428',
    'radius': '1',
    'RCLK': '"jk=9d6f5aa1d9cf36e0&tk=1j0ibd9re24eo00k&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=undefined&ts=1752962733993&sal=1&onclick=1"',
    'CLK': '9d6f5aa1d9cf36e0',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"138.0.7204.96"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.96", "Google Chrome";v="138.0.7204.96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"19.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

params = {
    'jk': '949d894503e4fe26',
    'spa': '1',
}

response = requests.get('https://www.indeed.com/viewjob', params=params, cookies=cookies, headers=headers)

print(response.text)