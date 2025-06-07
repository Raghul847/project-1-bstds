import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def scrape_discourse(url, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    posts = []
    page = 1

    while True:
        response = requests.get(f"{url}/page/{page}")
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        for post in soup.find_all("div", class_="topic-post"):
            post_date_str = post.find("time")["datetime"].split("T")[0]
            post_date = datetime.strptime(post_date_str, "%Y-%m-%d")

            if start <= post_date <= end:
                post_content = post.find("div", class_="post").text.strip()
                post_url = post.find("a", class_="post-anchor")["href"]
                posts.append({
                    "date": post_date_str,
                    "content": post_content,
                    "url": post_url
                })

        page += 1

    with open("discourse_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "content", "url"])
        writer.writeheader()
        writer.writerows(posts)

if __name__ == "__main__":
    discourse_url = "https://discourse.onlinedegree.iitm.ac.in/c/tds"
    scrape_discourse(discourse_url, "2025-01-01", "2025-04-14")
