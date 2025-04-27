import asyncio
import base64
import json
from bs4 import BeautifulSoup

async def fetch_video_links(session, config, keyword, max_pages=3):
    """异步抓取单个网站的多页视频链接"""
    all_videos = []

    for page in range(1, max_pages + 1):
        if config.get("use_base64_keyword"):
            payload = {
                "kw": keyword,
                "tags": [],
                "cat": [],
                "paged": page,    # 每一页都改这里
                "cats": []
            }
            json_str = json.dumps(payload, separators=(',', ':'))
            b64_str = base64.b64encode(json_str.encode()).decode()
            url = config["search_url"].format(encoded_keyword=b64_str)
        else:
            url = config["search_url"].format(keyword=keyword, page=page)

        print(f"正在抓取网站: {config['name']} ({url})")

        try:
            async with session.get(url, timeout=30) as resp:
                if resp.status != 200:
                    print(f"❌ 请求失败: 状态码 {resp.status}")
                    continue

                text = await resp.text()
                soup = BeautifulSoup(text, 'html.parser')
                videos = []
                for el in soup.select(config["result_selector"]):
                    title = (el.text.strip() if config["title_attr"] == "text"
                             else el.get(config["title_attr"]))
                    link = el.get(config["link_attr"])
                    if title and link:
                        full = config.get("base_url", "").rstrip("/") + link
                        videos.append({"title": title, "link": full})

                if not videos:
                    print(f"⚠️ 第{page}页无数据，提前结束")
                    break

                all_videos.extend(videos)

        except asyncio.TimeoutError:
            print("❌ 请求超时")
            continue
        except Exception as e:
            print(f"❌ 抓取失败: {e}")
            continue

    return all_videos
