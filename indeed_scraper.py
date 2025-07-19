from functions import *

class IndeedScraper:
    def __init__(self):
        try:
            with open("cookies.pkl", 'rb') as file:
                self.cookies = pickle.load(file)
        except:
            self.get_new_cookies()

    def get_new_cookies(self):
        input("Copy CURL to clipboard then press enter...")
        cookies = extract_cookies_from_curl(read_clipboard_text())
        with open("cookies.pkl", 'wb') as file:
            pickle.dump(cookies, file)
        self.cookies = cookies

    def make_request(self, params, cookies, headers):
        while True:
            response = requests.get('https://www.indeed.com/jobs', params=params, cookies=cookies, headers=headers)
            if response.status_code != 200:
                print("BAD COOKIES!!!")
                self.get_new_cookies()
            else:
                break
        return response

if __name__ == "__main__":
    indeed = IndeedScraper()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"138.0.7204.96"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.96", "Google Chrome";v="138.0.7204.96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    params = {
        'q': 'python',
        'l': 'Provo, UT',
        'radius': '50',
        'start': '10',
    }

    response = indeed.make_request(params, indeed.cookies, headers)
    data = extract_jobcards_data(response.text)

    print(data)