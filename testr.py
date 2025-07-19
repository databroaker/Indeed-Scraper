from CloudFlareBypasser import *
from DrissionPage import ChromiumPage
import pickle
from functions import *
import time
import os

from discord_webhook import DiscordWebhook, DiscordEmbed

def send_discord_webhook(webhook_url, title, description, fields=None, color="03b2f8"):
    webhook = DiscordWebhook(url=webhook_url, username="Job Scraper Bot")
    embed = DiscordEmbed(title=title, description=description, color=color)

    # Add fields if provided
    if fields:
        for field in fields:
            embed.add_embed_field(name=field['name'], value=field['value'], inline=False)

    # Optional: Add author, footer, timestamp
    embed.set_author(name="Indeed Scraper", url="https://www.indeed.com")
    embed.set_footer(text="Scraped on July 19, 2025")
    embed.set_timestamp()

    webhook.add_embed(embed)
    try:
        response = webhook.execute()
        print(f"Webhook sent successfully: {response.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"Error sending webhook: {e}", file=sys.stderr)

def read_pickle_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            return data
        except (pickle.PicklingError, EOFError, FileNotFoundError) as e:
            print(f"Error reading pickle file '{file_path}': {e}", file=sys.stderr)
            return None
    else:
        print(f"Pickle file '{file_path}' does not exist.", file=sys.stderr)
        return None

webhook_url = "https://discordapp.com/api/webhooks/1396233755592626359/03m_JSuuaaUxfVAs84qlXPEGc6Rnsh7yBmHqOPfd59XUsADDWc8u8cPgL91wCKvAYA6j"

data = read_pickle_file("data.pkl")

driver = ChromiumPage()
driver.get('https://indeed.com')

input("If you aren't logged in. Please log in then press enter here...")

first_link = "https://www.indeed.com/jobs?q=python&latLong=40.23384%2C-111.65853&locString=Provo%2C+UT&radius=50&from=searchOnDesktopSerp&vjk=4a95f087c7a6037d"
driver.get(first_link)
time.sleep(10)

while True:
    driver.run_js('''document.querySelector('a[data-testid="pagination-page-next"]').click()''')
    time.sleep(5)

    html = driver.html
    data = extract_jobcards_data(html)
    print("+++++\n\n{}\n\n+++++".format(str(data)))
    results = data["metaData"]["mosaicProviderJobCardsModel"]["results"]
    for r in results:
        print(r)
        print ("===\n\n{}\n\n===".format(r))

