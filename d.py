import requests
import json
import time
import random
import string
from datetime import datetime, timedelta

def get_data_from_file(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

def generate_user_agent():
    return f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 126)}.0.0.0 Safari/537.36 Edg/{random.randint(100, 126)}.0.0.0"

def send_event_request(data, user_agent):
    url = "https://plausible.io/api/event"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "text/plain",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": user_agent
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def send_login_request(data, user_agent):
    url = "https://api.onetime.dog/join"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": user_agent
    }
    response = requests.post(url, data=data, headers=headers)
    return response

def get_rewards_info(user_id, user_agent):
    url = f"https://api.onetime.dog/rewards?user_id={user_id}"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Origin": "https://onetime.dog",
        "Pragma": "no-cache",
        "Referer": "https://onetime.dog/",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": user_agent
    }
    response = requests.get(url, headers=headers)
    return response

def main():
    data_list = get_data_from_file('data.txt')
    user_agents = [generate_user_agent() for _ in data_list]

    print(f"Total accounts: {len(data_list)}")

    for index, data in enumerate(data_list):
        print(f"Processing account {index + 1}/{len(data_list)}")

        # Send event request
        event_data = {
            "n": "pageview",
            "u": f"https://onetime.dog/#tgWebAppData={data}&tgWebAppVersion=7.6&tgWebAppPlatform=tdesktop&tgWebAppThemeParams=%7B%22accent_text_color%22%3A%22%236ab2f2%22%2C%22bg_color%22%3A%22%2317212b%22%2C%22button_color%22%3A%22%235288c1%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22destructive_text_color%22%3A%22%23ec3942%22%2C%22header_bg_color%22%3A%22%2317212b%22%2C%22hint_color%22%3A%22%23708499%22%2C%22link_color%22%3A%22%236ab3f3%22%2C%22secondary_bg_color%22%3A%22%23232e3c%22%2C%22section_bg_color%22%3A%22%2317212b%22%2C%22section_header_text_color%22%3A%22%236ab3f3%22%2C%22section_separator_color%22%3A%22%23111921%22%2C%22subtitle_text_color%22%3A%22%23708499%22%2C%22text_color%22%3A%22%23f5f5f5%22%7D",
            "d": "onetime.dog",
            "r": None
        }
        event_response = send_event_request(event_data, user_agents[index])
        print(f"Event response status: {event_response.status_code}")
        
        if event_response.status_code != 202:
            print("Error in event request.")
            continue

        # Send login request
        login_response = send_login_request(data, user_agents[index])
        print(f"Login response status: {login_response.status_code}")

        if login_response.status_code != 200:
            print("Error in login request.")
            continue

        # Extract user ID from data
        user_id = data.split('%22id%22%3A')[1].split('%2C')[0]

        # Get rewards info
        rewards_response = get_rewards_info(user_id, user_agents[index])
        print(f"Rewards response status: {rewards_response.status_code}")

        if rewards_response.status_code != 200:
            print("Error in rewards request.")
            continue

        try:
            rewards_info = rewards_response.json()
            print(f"Rewards Info:\nTotal: {rewards_info['total']}\nAge: {rewards_info['age']}\nPremium: {rewards_info['premium']}\nFrens: {rewards_info['frens']}\nBoost: {rewards_info['boost']}\nConnect: {rewards_info['connect']}\nDaily: {rewards_info['daily']}")
        except json.JSONDecodeError:
            print("Error decoding rewards response.")
        
        # Wait 5 seconds before processing the next account
        time.sleep(5)

    # Countdown for next run
    next_run = datetime.now() + timedelta(days=1)
    while datetime.now() < next_run:
        remaining = next_run - datetime.now()
        print(f"Next run in: {remaining}", end='\r')
        time.sleep(1)

if __name__ == "__main__":
    main()
