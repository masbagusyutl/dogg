import requests
import time
import random
from datetime import datetime, timedelta
import json

def generate_user_agent():
    browsers = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
    os = ["Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7", "Linux; Android 10"]
    return f"Mozilla/5.0 ({random.choice(os)}) AppleWebKit/537.36 (KHTML, like Gecko) {random.choice(browsers)}/{random.randint(70, 99)}.0.0.0 Safari/537.36"

def read_accounts(filename):
    with open(filename, 'r') as file:
        accounts = [line.strip() for line in file.readlines()]
    return accounts

def read_tg_web_app_data(filename):
    with open(filename, 'r') as file:
        tg_web_app_data = [line.strip() for line in file.readlines()]
    return tg_web_app_data

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

def send_login_request(query_id, user_agent):
    url = "https://api.onetime.dog/join"
    payload = f"query_id={query_id}&user=%7B%22id%22%3A1039578077%2C%22first_name%22%3A%22masbagus%20yutl%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22masbagusyutl%22%2C%22language_code%22%3A%22en%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1721706187&hash=88a6653691de79731582158f59744488a6af0a9c52cc9adcc0205889b3f3d6ec"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "358",
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

def countdown_timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        hours, mins = divmod(mins, 60)
        timeformat = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(f"Countdown: {timeformat}", end='\r')
        time.sleep(1)
        duration -= 1

def main():
    accounts = read_accounts('data.txt')
    tg_web_app_data_list = read_tg_web_app_data('data.txt')
    num_accounts = len(accounts)
    user_agents = [generate_user_agent() for _ in range(num_accounts)]

    print(f"Total accounts: {num_accounts}")

    for index, (query_id, tg_web_app_data, user_agent) in enumerate(zip(accounts, tg_web_app_data_list, user_agents)):
        print(f"Processing event for account {index + 1}/{num_accounts}")
        event_response = send_event_request(tg_web_app_data, user_agent)
        if event_response.status_code == 202:
            print(f"Event for account {index + 1} processed successfully.")
        else:
            print(f"Event for account {index + 1} failed with status code: {event_response.status_code}")

        print(f"Processing login for account {index + 1}/{num_accounts}")
        login_response = send_login_request(query_id, user_agent)
        if login_response.status_code == 200:
            print(f"Login for account {index + 1} processed successfully.")
        else:
            print(f"Login for account {index + 1} failed with status code: {login_response.status_code}")

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
