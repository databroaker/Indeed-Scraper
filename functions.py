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