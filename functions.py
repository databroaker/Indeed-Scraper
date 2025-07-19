import re
import pyperclip
import requests
import pickle
import json
import sys

def read_clipboard_text():
    try:
        text = pyperclip.paste()
        return text if text else None
    except Exception as e:
        print(f"Error reading clipboard: {e}")
        return None

def extract_cookies_from_curl(curl_command):
    cookie_match = re.search(r'-b\s*([\'"])(.*?)\1', curl_command, re.DOTALL)
    if not cookie_match:
        print("No cookies found in the cURL command.")
        return {}

    cookie_string = cookie_match.group(2)
    cookie_pairs = [pair.strip() for pair in cookie_string.split(';') if pair.strip()]

    cookie_dict = {}
    for pair in cookie_pairs:
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookie_dict[key.strip()] = value.strip()

    return cookie_dict


def extract_jobcards_data(html):
    start_marker = 'window.mosaic.providerData["mosaic-provider-jobcards"]='
    end_marker = 'window.mosaic.providerData["mosaic-provider-passport-intercept"]'
    json_str = html.split(start_marker)[1].split(end_marker)[0][:-6]
    print(json_str)
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        print(f"Problematic JSON string (first 1000 chars): {json_str[:1000]}...", file=sys.stderr)
        return None

def get_job_info(session, jobKey):
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
        'jk': str(jobKey),
        'spa': '1',
    }

    response = session.get('https://www.indeed.com/viewjob', params=params, headers=headers)
    data = json.loads(response.text)
    return data