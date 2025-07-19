from DrissionPage import ChromiumPage
from functions import *
import time
import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup

blacklist_file = "blacklist.pkl"

def send_discord_webhook(webhook_url, title, description, url, fields=None, color="03b2f8"):
    webhook = DiscordWebhook(url=webhook_url, username="Job Scraper Bot")
    embed = DiscordEmbed(title=title, description=description, color=color, url=url)

    # Add fields if provided
    if fields:
        for field in fields:
            embed.add_embed_field(name=field['name'], value=field['value'], inline=False)

    # Optional: Add author, footer, timestamp
    embed.set_author(name="Indeed Scraper", url=url)
    embed.set_timestamp()

    webhook.add_embed(embed)
    try:
        response = webhook.execute()
        print(f"Webhook sent successfully: {response.status_code}", file=sys.stderr)
    except Exception as e:
        print(f"Error sending webhook: {e}", file=sys.stderr)

def send_chunked_webhooks(webhook_url, title, plaintext, url):
    max_length = 4096
    if len(plaintext) <= max_length:
        # Send directly if under or equal to limit
        send_discord_webhook(webhook_url, title, plaintext, url)
    else:
        # Split plaintext into chunks
        chunks = []
        current_pos = 0

        while current_pos < len(plaintext):
            # Find the end of the chunk (up to max_length)
            end_pos = min(current_pos + max_length, len(plaintext))

            # Adjust end_pos to avoid splitting mid-word
            if end_pos < len(plaintext):
                while end_pos > current_pos and plaintext[end_pos - 1] not in (' ', '\n'):
                    end_pos -= 1
                if end_pos == current_pos:  # No space found, force split
                    end_pos = current_pos + max_length

            # Add the chunk
            chunks.append(plaintext[current_pos:end_pos])
            current_pos = end_pos

        # Send each chunk with the appropriate title
        for i, chunk in enumerate(chunks):
            chunk_title = title if i == 0 else f"{title} (Part {i + 1})"
            send_discord_webhook(webhook_url, chunk_title, chunk.strip(), url)

def read_pickle_file(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            return data
        except (pickle.PicklingError, EOFError, FileNotFoundError) as e:
            print(f"Error reading pickle file '{file_path}': {e}", file=sys.stderr)
            return dict()
    else:
        print(f"Pickle file '{file_path}' does not exist.", file=sys.stderr)
        return dict()

def save_list_to_pickle(data_list, file_path):
    """
    Save a list to a pickle file.

    Args:
        data_list (list): The list to save.
        file_path (str): The path to the pickle file (e.g., 'mylist.pkl').

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True) if os.path.dirname(file_path) else None

        # Open the file in binary write mode and save the list
        with open(file_path, 'wb') as file:
            pickle.dump(data_list, file)
        print(f"List successfully saved to {file_path}")
        return True
    except (OSError, pickle.PicklingError) as e:
        print(f"Error saving list to {file_path}: {e}")
        return False

def html_to_discord_markdown(html_content):
    """
    Convert HTML content to Discord-compatible Markdown, preserving structure and ensuring clean formatting.

    Args:
        html_content (str): The HTML content to process.

    Returns:
        str: Formatted Markdown text suitable for Discord.
    """
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize output list
    output = []

    # Function to clean text while preserving natural spacing
    def clean_text(text):
        # Normalize multiple spaces to a single space
        text = re.sub(r'\s+', ' ', text.strip())
        # Ensure single space after punctuation
        text = re.sub(r'([.,:;!?])([^\s])', r'\1 \2', text)
        return text

    # Track last element type to manage spacing
    last_element_type = None

    # Process each relevant HTML element
    for element in soup.find_all(
            ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span', 'b', 'strong', 'i', 'em']):
        # Handle bold and italic inline elements
        if element.name in ['b', 'strong']:
            text = element.get_text(strip=True)
            if not text:
                continue
            cleaned_text = f"**{clean_text(text)}**"
            # Append inline bold to the last line if it’s part of a paragraph
            if output and last_element_type == 'paragraph' and not output[-1].startswith(('-', '#', '**')):
                output[-1] += f" {cleaned_text}"
            else:
                output.append(cleaned_text)
            last_element_type = 'inline'
            continue
        elif element.name in ['i', 'em']:
            text = element.get_text(strip=True)
            if not text:
                continue
            cleaned_text = f"*{clean_text(text)}*"
            if output and last_element_type == 'paragraph' and not output[-1].startswith(('-', '#', '**')):
                output[-1] += f" {cleaned_text}"
            else:
                output.append(cleaned_text)
            last_element_type = 'inline'
            continue

        # Handle other elements
        text = element.get_text(strip=True)
        if not text:
            continue  # Skip empty elements

        cleaned_text = clean_text(text)

        # Format based on element type
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # Use ## for headings (Discord supports # and ## reliably)
            if last_element_type != 'heading':
                output.append('')
            output.append(f"## {cleaned_text}")
            output.append('')
            last_element_type = 'heading'
        elif element.name == 'li':
            # Format list items with a dash
            output.append(f"- {cleaned_text}")
            last_element_type = 'list'
        else:
            # Treat div, p, span as paragraphs or section headers
            if (element.find('b') or element.find('strong') or
                    cleaned_text in ['Compensation:', 'Location:', 'Travel:', 'Why You Belong at Pickle']):
                if last_element_type != 'heading':
                    output.append('')
                output.append(f"**{cleaned_text}**")
                output.append('')
                last_element_type = 'heading'
            else:
                output.append(cleaned_text)
                last_element_type = 'paragraph'

    # Join lines and clean up spacing
    markdown = '\n'.join(line for line in output if line or line == '')
    # Replace multiple consecutive newlines with exactly two newlines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown.strip())
    # Remove trailing spaces
    markdown = '\n'.join(line.rstrip() for line in markdown.split('\n'))

    return markdown

webhook_url = "https://discordapp.com/api/webhooks/1396275185514057788/3oyqTqzIqCbZ9qkHdd8fYKYEhg1qBjUoyymPrPXOjJ0f1WghHCtztF59qAktuGHxOSEV"

blacklist = read_pickle_file(blacklist_file)

driver = ChromiumPage()
driver.get('https://indeed.com')

input("If you aren't logged in. Please log in then press enter here...")

first_link = "https://www.indeed.com/jobs?q=python&latLong=40.23384%2C-111.65853&locString=Provo%2C+UT&radius=50&from=searchOnDesktopSerp&vjk=4a95f087c7a6037d"
driver.get(first_link)
time.sleep(10)

cookies = driver.cookies(as_dict=False)
session = requests.Session()
for cookie in cookies:
    session.cookies.set(
        name=cookie['name'],
        value=cookie['value'],
        domain=cookie.get('domain', ''),
        path=cookie.get('path', '/')
    )

while True:
    driver.run_js('''document.querySelector('a[data-testid="pagination-page-next"]').click()''')
    time.sleep(5)

    html = driver.html
    data = extract_jobcards_data(html)
    print("+++++\n\n{}\n\n+++++".format(str(data)))
    results = data["metaData"]["mosaicProviderJobCardsModel"]["results"]
    for r in results:
        if "adBlob" in str(r):
            continue
        jobKey = r["jobkey"]
        jobInfo = get_job_info(session, jobKey)
        description = jobInfo["body"]["jobInfoWrapperModel"]["jobInfoModel"]["sanitizedJobDescription"]
        title = jobInfo["body"]["jobInfoWrapperModel"]["jobInfoModel"]["jobInfoHeaderModel"]["jobTitle"]
        soup = BeautifulSoup(description, 'html.parser')
        plaintext = soup.get_text(separator=' ', strip=True)
        print(plaintext)
        print("+++")

        lnk = "https://www.indeed.com/viewjob?jk={}&from=shareddesktop_copy".format(jobKey)

        if jobKey not in blacklist.keys():
            send_chunked_webhooks(webhook_url, title, plaintext, lnk)
            blacklist[jobKey] = {"title": title, "desecription": plaintext}
            save_list_to_pickle(blacklist, blacklist_file)
            print("Sleeping for 10...")
            time.sleep(10)
