import asyncio
import aiohttp
from pachong.scraper.fetcher import fetch_video_links
from scraper.config_loader import load_all_configs
from scraper.display import display
from scraper.display import choose_sites_and_pages

# 全局请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers",
    "Referer": "https://18comic.vip/",  # 可以改为实际访问页面的Referer
    "Origin": "https://18comic.vip/",
}




async def run_all(keyword):
    websites = load_all_configs()
    if not websites:
        print("没有加载到任何网站配置。")
        return

    # 选择要抓取的网站和抓取的页数
    selected_sites, page_count = choose_sites_and_pages(websites)
    if not selected_sites:
        print("❌ 没有正确选择网站。")
        return

    async with aiohttp.ClientSession(
        headers=HEADERS,
        trust_env=True,
    ) as session:
        tasks = []
        for config in selected_sites:
            # 根据 page_count 来循环页数，传递 max_pages
            tasks.append(fetch_video_links(session, config, keyword, max_pages=page_count))

        results = await asyncio.gather(*tasks)

    # 合并所有抓取的结果并展示
    all_videos = [v for sublist in results for v in sublist]
    display(all_videos)


def main():
    kw = input("请输入关键字：")
    asyncio.run(run_all(kw))


if __name__ == "__main__":
    main()
