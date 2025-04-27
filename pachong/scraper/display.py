def display(video_list):
    for video in video_list:
        print(f"视频标题: {video['title']}")
        print(f"视频链接: {video['link']}")
        print("-" * 60)

def choose_sites_and_pages(site_list):
    print("\n可选网站:")
    for idx, site in enumerate(site_list, 1):
        print(f"{idx}. {site['name']}")
    print(f"{len(site_list)+1}. 全部抓取")

    try:
        choice = input("\n请输入要抓取的网站编号（用逗号分隔多个，如1,3）：").strip()
        if str(len(site_list)+1) in choice:
            selected_sites = site_list  # 全选
        else:
            selected_indices = [int(i) - 1 for i in choice.split(",") if i.strip().isdigit()]
            selected_sites = [site_list[i] for i in selected_indices if 0 <= i < len(site_list)]

        page_count = int(input("\n请输入每个网站要抓取的页数（默认1页）：").strip() or "1")
        return selected_sites, page_count

    except Exception as e:
        print(f"❌ 输入错误: {e}")
        return [], 1
