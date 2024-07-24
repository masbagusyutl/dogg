import requests
import time
import random
from datetime import datetime, timedelta
import json
import urllib.parse

def generate_user_agent():
    browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
    os = ["Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7", "Linux; Android 10"]
    return f"Mozilla/5.0 ({random.choice(os)}) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(browsers)}/{random.randint(70, 99)}.0.0.0 Safari/537.36"

def read_data(filename):
    with open(filename, 'r') as file:
        data = [line.strip() for line in file.readlines()]
    return data

def parse_user_id(payload):
    user_data = urllib.parse.parse_qs(payload)
    user_json = user_data['user'][0]
    user_dict = json.loads(user_json)
    return user_dict['id']

def send_event_request(tg_web_app_data, user_agent):
    url = "https://plausible.io/api/event"
    payload = {
        "n": "pageview",
        "u": f"https://onetime.dog/#tgWebAppData={tg_web_app_data}",
        "tgWebAppVersion": "7.6",
        "tgWebAppPlatform": "tdesktop",
        "tgWebAppThemeParams": {
            "accent_text_color": "#6ab2f2",
            "bg_color": "#17212b",
            "button_color": "#5288c1",
            "button_text_color": "#ffffff",
            "destructive_text_color": "#ec3942",
            "header_bg_color": "#17212b",
            "hint_color": "#708499",
            "link_color": "#6ab3f3",
            "secondary_bg_color": "#232e3c",
            "section_bg_color": "#17212b",
            "section_header_text_color": "#6ab3f3",
            "section_separator_color": "#111921",
            "subtitle_text_color": "#708499",
            "text_color": "#f5f5f5"
        },
        "d": "onetime.dog",
        "r": None
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "text/plain",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": user_agent
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response

def send_login_request(payload, user_agent):
    url = "https://api.onetime.dog/join"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": str(len(payload)),
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": user_agent
    }
    response = requests.post(url, data=payload, headers=headers)
    return response

def fetch_rewards(user_id, user_agent):
    url = f"https://api.onetime.dog/rewards?user_id={user_id}"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Priority": "u=1, i",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers)
    return response

def print_rewards_info(rewards):
    print("Info Hadiah:")
    print(f"Total: {rewards['total']}")
    print(f"Age: {rewards['age']}")
    print(f"Premium: {rewards['premium']}")
    print(f"Frens: {rewards['frens']}")
    print(f"Boost: {rewards['boost']}")
    print(f"Connect: {rewards['connect']}")
    print(f"Daily: {rewards['daily']}")

def countdown_timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        hours, mins = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"Countdown: {timeformat}", end='\r')
        time.sleep(1)
        duration -= 1

def main():
    data = read_data('data.txt')
    num_accounts = len(data)
    user_agents = [generate_user_agent() for _ in range(num_accounts)]

    print(f"Total accounts: {num_accounts}")

    for index, payload in enumerate(data):
        user_agent = user_agents[index]
        user_id = parse_user_id(payload)
        
        print(f"Processing event for account {index + 1}/{num_accounts}")
        event_response = send_event_request(payload, user_agent)
        if event_response.status_code == 202:
            print(f"Event for account {index + 1} processed successfully.")
        else:
            print(f"Event for account {index + 1} failed with status code: {event_response.status_code}")

        print(f"Processing login for account {index + 1}/{num_accounts}")
        login_response = send_login_request(payload, user_agent)
        if login_response.status_code == 200:
            print(f"Login for account {index + 1} processed successfully.")
        else:
            print(f"Login for account {index + 1} failed with status code: {login_response.status_code}")
        
        print(f"Fetching rewards for account {index + 1}/{num_accounts}")
        rewards_response = fetch_rewards(user_id, user_agent)
        if rewards_response.status_code == 200:
            rewards_info = rewards_response.json()
            print_rewards_info(rewards_info)
        else:
            print(f"Failed to fetch rewards for account {index + 1} with status code: {rewards_response.status_code}")

        time.sleep(5)  # Wait for 5 seconds before switching to the next account

    print("All accounts processed. Starting 1-day countdown...")
    next_process_time = datetime.now() + timedelta(days=1)
    while True:
        remaining_time = (next_process_time - datetime.now()).total_seconds()
        if remaining_time <= 0:
            break
        countdown_timer(int(remaining_time))
        print(f"Next process will start on: {next_process_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("Restarting the process...")
        main()

if __name__ == "__main__":
    main()
