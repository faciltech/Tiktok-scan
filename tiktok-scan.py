#!/bin/python
import json
import argparse
import requests
from bs4 import BeautifulSoup as BSoup
import csv
import logging

ESC = '\x1b'
RED = ESC + '[31m'
GREEN = ESC + '[32m'
RESET = ESC + '[0m'

logging.basicConfig(
    filename='tikstalker.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)


def get_tiktoker(username: str, user_agent=None, proxy=None):
    headers = {
        'User-Agent': user_agent or
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    }

    proxies = {'http': proxy, 'https': proxy} if proxy else None
    url = f'https://www.tiktok.com/@{username}'

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request failed for {username}: {e}")
        print(f"{RED}Request failed: {e}{RESET}")
        return

    soup = BSoup(response.text, 'html.parser')
    script_tag = soup.find(
        'script',
        id='__UNIVERSAL_DATA_FOR_REHYDRATION__',
        type='application/json'
    )

    if not script_tag or not script_tag.string:
        print(f"{RED}Failed to locate TikTok JSON data (blocked / private / banned).{RESET}")
        logging.error("JSON script tag not found")
        return

    try:
        json_data = json.loads(script_tag.string)
        user_data = json_data.get('__DEFAULT_SCOPE__', {}).get('webapp.user-detail')

        if not user_data:
            raise ValueError("User data not present in JSON")

        save_user_data(username, user_data)
        parse_tiktoker_data(username, user_data)

    except Exception as e:
        logging.error(f"Parsing error for {username}: {e}")
        print(f"{RED}Parsing error: {e}{RESET}")


def save_user_data(username, data):
    filename = f"{username}_tiktok_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"{GREEN}User data saved to {filename}{RESET}")


def parse_tiktoker_data(username, field: dict):
    user_info = field.get("userInfo", {})
    user_data = user_info.get("user", {})
    user_stats = user_info.get("stats", {})
    share_meta = field.get("shareMeta", {})

    print('\n' + '-' * 15 + ' User Information ' + '-' * 15)

    print(f'{RED}Profile Picture URL:{GREEN} {user_data.get("avatarLarger", "N/A")}')
    print(f'{RED}Account ID:{GREEN}       {user_data.get("id", "N/A")}')
    print(f'{RED}Unique ID:{GREEN}        {user_data.get("uniqueId", "N/A")}')
    print(f'{RED}Nickname:{GREEN}         {user_data.get("nickname", "N/A")}')

    signature = user_data.get("signature", "").replace('\n', ' ')
    print(f'{RED}Bio:{GREEN}              {signature or "N/A"}')

    print(f'{RED}Private Account:{GREEN}  {user_data.get("privateAccount", "N/A")}')
    print(f'{RED}User Country:{GREEN}     {user_data.get("region", "Not available")}')
    print(f'{RED}Account Language:{GREEN} {user_data.get("language", "Not available")}')

    print(f'{RED}\nTotal Followers:{GREEN}  {user_stats.get("followerCount", 0)}')
    print(f'{RED}Total Following:{GREEN}  {user_stats.get("followingCount", 0)}')
    print(f'{RED}Total Hearts:{GREEN}     {user_stats.get("heartCount", 0)}')
    print(f'{RED}Total Posts:{GREEN}      {user_stats.get("videoCount", 0)}')

    print(f'{RED}\nTitle:{GREEN}            {share_meta.get("title", "N/A")}')
    print(f'{RED}Description:{GREEN}      {share_meta.get("desc", "N/A")}\n')

    print('\n' + '-' * 15 + ' Recent Videos ' + '-' * 15)

    recent_videos = field.get("itemList", [])
    video_data = []

    if not recent_videos:
        print(f'{RED}No recent videos found or access restricted.{RESET}')
        return

    for idx, video in enumerate(recent_videos, 1):
        stats = video.get("stats", {})
        desc = video.get("desc", "").replace('\n', ' ')
        video_id = video.get("id")

        if not video_id:
            continue

        video_url = f'https://www.tiktok.com/@{user_data.get("uniqueId")}/video/{video_id}'

        print(f'{RED}Video {idx}:{GREEN} {desc or "No description"}')
        print(f'{RED}URL:{GREEN} {video_url}')
        print(f'{RED}Views:{GREEN} {stats.get("playCount", 0)}')
        print(f'{RED}Likes:{GREEN} {stats.get("diggCount", 0)}')
        print(f'{RED}Comments:{GREEN} {stats.get("commentCount", 0)}')
        print(f'{RED}Shares:{GREEN} {stats.get("shareCount", 0)}\n')

        video_data.append({
            "Description": desc,
            "URL": video_url,
            "Views": stats.get("playCount", 0),
            "Likes": stats.get("diggCount", 0),
            "Comments": stats.get("commentCount", 0),
            "Shares": stats.get("shareCount", 0)
        })

    if video_data:
        save_videos_csv(username, video_data)


def save_videos_csv(username, video_data):
    filename = f"{username}_videos.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=video_data[0].keys())
        writer.writeheader()
        writer.writerows(video_data)

    print(f"{GREEN}Video data saved to {filename}{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="TikStalker - OSINT tool for extracting public TikTok profile data"
    )
    parser.add_argument('-u', '--user', dest='target', required=True, help='Target TikTok username')
    parser.add_argument('-a', '--user-agent', dest='uagent', help='Custom User-Agent')
    parser.add_argument('-p', '--proxy', dest='proxy', help='Proxy (http://ip:port)')
    args = parser.parse_args()

    get_tiktoker(args.target, args.uagent, args.proxy)


if __name__ == '__main__':
    main()
