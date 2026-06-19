import json
import re
from datetime import datetime

SITE_DATA = {
    "name": "乐鱼体育",
    "url": "https://mzh-leyu.com.cn",
    "keywords": ["乐鱼体育", "运动资讯", "赛事报道", "体育动态"],
    "tags": ["体育", "资讯", "娱乐"],
    "description": "提供专业体育新闻、赛事分析和运动社区互动服务的在线平台。"
}

def sanitize_text(raw: str) -> str:
    cleaned = re.sub(r'<[^>]+>', '', raw)
    return cleaned.strip()

def format_keywords(keyword_list: list) -> str:
    return ", ".join([kw.strip() for kw in keyword_list if kw.strip()])

def build_summary(data: dict) -> str:
    name = sanitize_text(data.get("name", "未知站点"))
    url = sanitize_text(data.get("url", ""))
    keywords = format_keywords(data.get("keywords", []))
    tags = format_keywords(data.get("tags", []))
    desc = sanitize_text(data.get("description", "暂无描述"))

    summary_lines = [
        f"站点名称：{name}",
        f"访问地址：{url}",
        f"核心关键词：{keywords}",
        f"内容标签：{tags}",
        f"站点简介：{desc}"
    ]
    return "\n".join(summary_lines)

def generate_summary_report(site: dict) -> str:
    base = build_summary(site)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"【站点摘要报告】\n生成时间：{timestamp}\n{base}"
    return report

def store_summary_to_file(filepath: str, content: str) -> bool:
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except OSError:
        return False

def load_site_from_json(json_str: str) -> dict:
    try:
        data = json.loads(json_str)
        required = ["name", "url", "keywords", "tags", "description"]
        if not all(k in data for k in required):
            raise ValueError("缺少必要字段")
        return data
    except (json.JSONDecodeError, ValueError):
        return SITE_DATA.copy()

def display_summary(summary: str) -> None:
    print(summary)
    print("=" * 48)

def main():
    site_info = SITE_DATA
    summary = build_summary(site_info)
    report = generate_summary_report(site_info)

    display_summary(summary)
    print("\n完整报告：")
    display_summary(report)

    filepath = "site_summary_output.txt"
    success = store_summary_to_file(filepath, report)
    if success:
        print(f"摘要已保存至：{filepath}")
    else:
        print("文件写入失败，请检查路径权限。")

if __name__ == "__main__":
    main()