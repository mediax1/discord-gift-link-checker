import requests
import json
import threading
import random
import os
from datetime import datetime, timezone
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    ORANGE = "\033[38;5;208m"
    CYAN = "\033[96m"

ASCII_ART = r"""
 ____             _    _____
|  _ \  __ _ _ __| | _| ____|   _  ___  ___ 
| | | |/ _` | '__| |/ /  _|| | | |/ _ \/ __|
| |_| | (_| | |  |   <| |__| |_| |  __/\__ \
|____/ \__,_|_|  |_|\_\_____\__, |\___||___/
                            |___/  
                                  by @mediax1 | discord.gg/darkeyes
"""

def config():
    try:
        with open('config.json', 'r', encoding='utf-8') as setting:
            return json.load(setting)
    except Exception as e:
        print(f"{Colors.RED}Failed loading 'config.json': {e}{Colors.RESET}")
        exit()

def load_links(file_path='gift.txt'):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{Colors.RED}File not found: {file_path}{Colors.RESET}")
        exit()

def load_proxies(file_path='proxies.txt'):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                return None
            return proxies
    except FileNotFoundError:
        return None

def format_remaining_time(remaining_time):
    total_seconds = int(remaining_time.total_seconds())
    hours = total_seconds // 3600
    return f"{hours} hour{'s' if hours != 1 else ''}"

def check_link(link, headers, proxy=None):
    url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{link.split('/')[-1]}?with_application=false&with_subscription_plan=true"
    retries = 3
    retry_delay = 60

    for attempt in range(retries):
        try:
            if proxy:
                response = requests.get(url, headers=headers, timeout=config['timeout'], proxies=proxy)
            else:
                response = requests.get(url, headers=headers, timeout=config['timeout'])

            if response.status_code == 429:
                print(f"{Colors.YELLOW}{link} - Rate limited, retrying in {retry_delay} seconds...{Colors.RESET}")
                time.sleep(retry_delay)
                continue

            data = json.loads(response.text)
            uses = data.get("uses", 0)
            max_uses = data.get("max_uses", 1)

            if uses >= max_uses:
                print(f"{Colors.ORANGE}{link} - Already claimed{Colors.RESET}")
                return "already_claimed"

            if "subscription_plan" in response.text.lower():
                expiration_timestamp = data.get("expires_at")
                user_info = data.get("user")
                creator_username = user_info.get("username") if user_info else "Unknown"
                creator_userid = user_info.get("id") if user_info else "Unknown"

                if expiration_timestamp:
                    if expiration_timestamp.endswith('Z'):
                        expiration_timestamp = expiration_timestamp[:-1] + '+00:00'
                    elif len(expiration_timestamp) > 26 and expiration_timestamp[-3] != ':':
                        expiration_timestamp = expiration_timestamp[:-2] + ':' + expiration_timestamp[-2:]

                    expiration_time = datetime.fromisoformat(expiration_timestamp)
                    remaining_time = expiration_time - datetime.now(timezone.utc)
                    formatted_time = format_remaining_time(remaining_time)
                    subscription_plan = data.get("subscription_plan")
                    if isinstance(subscription_plan, dict) and subscription_plan.get("name", "").lower() == "nitro monthly":
                        gift_type = "Boost"
                    else:
                        gift_type = "Basic"
                    folder_name = os.path.join("output", gift_type)
                    os.makedirs(folder_name, exist_ok=True)
                    with open(f"{folder_name}/valid.txt", "a") as valid_file:
                        valid_file.write(f"{link} - Expires in: {formatted_time} - Created by: {creator_username} (UserID: {creator_userid}) - Gift Type: {gift_type}\n")
                    print(f"{Colors.GREEN}{link} - Valid (Expires in: {formatted_time}, Created by: {creator_username} - {creator_userid}, Gift Type: {gift_type}){Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}{link} - Valid (No expiration info, Created by: {creator_username} - {creator_userid}, Gift Type: {gift_type}){Colors.RESET}")
                return "valid"
            elif data.get("message") == "Unknown Gift Code":
                print(f"{Colors.RED}{link} - Invalid{Colors.RESET}")
                return "invalid"
            else:
                print(f"{Colors.RED}{link} - Unknown response: {data}{Colors.RESET}")
                return "invalid"
        except requests.exceptions.RequestException as e:
            print(f"{Colors.YELLOW}{link} - Proxy error: {e}{Colors.RESET}")
            return "error"

    print(f"{Colors.RED}{link} - Failed after {retries} attempts.{Colors.RESET}")
    return "error"

def worker(link, headers, proxies, valid_links, invalid_links, already_claimed_links):
    proxy = None
    if proxies:
        proxy_info = random.choice(proxies).split(':')
        proxy = {
            'http': f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}",
            'https': f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}"
        }

    result = check_link(link, headers, proxy)
    
    if result == "valid":
        valid_links.append(link)
    elif result == "invalid":
        invalid_links.append(link)
    elif result == "already_claimed":
        already_claimed_links.append(link)

if __name__ == '__main__':
    print(Style.BRIGHT + Fore.MAGENTA + ASCII_ART + Style.RESET_ALL)

    config = config()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    gift_links = load_links()
    proxies = load_proxies()

    if proxies is None or len(proxies) == 0:
        continue_without_proxies = input(f"{Colors.YELLOW}Warning: No proxies found. Do you want to continue without proxies? (y/n): {Colors.RESET}")
        if continue_without_proxies.lower() != 'y':
            print(f"{Colors.RED}Exiting the program.{Colors.RESET}")
            exit()

    max_threads = 5
    valid_links = []
    invalid_links = []
    already_claimed_links = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(worker, link, headers, proxies, valid_links, invalid_links, already_claimed_links) for link in gift_links]
        for future in futures:
            future.result()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/invalid.txt", "w") as invalid_file:
        invalid_file.write("\n".join(invalid_links))

    with open(f"{output_dir}/already_claimed.txt", "w") as already_claimed_file:
        already_claimed_file.write("\n".join(already_claimed_links))

    total_links = len(valid_links) + len(invalid_links) + len(already_claimed_links)
    print(f"{Colors.CYAN}Total links checked: {total_links}{Colors.RESET}")
    print(f"{Colors.GREEN}Valid links: {len(valid_links)}{Colors.RESET}")
    print(f"{Colors.RED}Invalid links: {len(invalid_links)}{Colors.RESET}")
    print(f"{Colors.ORANGE}Already claimed links: {len(already_claimed_links)}{Colors.RESET}")
    print(f"{Colors.CYAN}Valid links saved to respective folders.{Colors.RESET}")
    print(f"{Colors.CYAN}Invalid links saved to: {output_dir}/invalid.txt{Colors.RESET}")
    print(f"{Colors.CYAN}Already claimed links saved to: {output_dir}/already_claimed.txt{Colors.RESET}")