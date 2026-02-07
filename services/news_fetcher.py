"""
뉴스 수집 모듈
RSS 피드 및 웹 크롤링을 통해 뉴스를 수집합니다.
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from models import NewsArticle
import dateutil.parser
import urllib.parse

def fetch_rss_news(rss_url: str, source_name: str, limit: int = 5) -> List[NewsArticle]:
    """주어진 RSS URL에서 최신 뉴스를 가져옵니다."""
    try:
        feed = feedparser.parse(rss_url)
        articles = []
        for entry in feed.entries[:limit]:
            # 날짜 파싱
            try:
                dt = dateutil.parser.parse(entry.published)
                published_at = dt.isoformat()
            except:
                published_at = datetime.now().isoformat()
                
            articles.append(NewsArticle(
                title=entry.title,
                url=entry.link,
                source=source_name,
                published_at=published_at,
                summary=entry.description if hasattr(entry, 'description') else ""
            ))
        return articles
    except Exception as e:
        print(f"Error fetching RSS from {source_name}: {e}")
        return []

def fetch_naver_main_hot_news(limit: int = 5) -> List[NewsArticle]:
    """네이버 뉴스 메인에서 Hot 뉴스를 크롤링합니다."""
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100" # 정치 섹션
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # 네이버 뉴스 메인 기사 영역 (2025년 초 기준 추정 또는 구조 기반)
        # 1. 썸네일/헤드라인 뉴스
        news_list = soup.select('div.sa_text') or soup.select('.cluster_text') or soup.select('.nmain_news_list_group')
        
        if not news_list:
            # Fallback for different structure
            news_items = soup.find_all('a', href=True)
            candidate_links = []
            for a in news_items:
                href = a['href']
                if '/mnews/article/' in href:
                    title = a.get_text().strip()
                    if len(title) > 10 and not any(c['url'] == href for c in candidate_links):
                        candidate_links.append({'title': title, 'url': href})
            
            for item in candidate_links[:limit]:
                articles.append(NewsArticle(
                    title=item['title'],
                    url=item['url'],
                    source="네이버 뉴스 메인",
                    published_at=datetime.now().isoformat(),
                    summary="",
                    hotness_score=15.0
                ))
            return articles

        for item in news_list[:limit]:
            title_tag = item.select_one('a.sa_text_title') or item.select_one('a')
            source_tag = item.select_one('.sa_text_press')
            
            if title_tag:
                title = title_tag.get_text().strip()
                link = title_tag['href']
                if not link.startswith('http'):
                    link = "https://news.naver.com" + link
                
                source = source_tag.get_text().strip() if source_tag else "네이버 뉴스"
                
                articles.append(NewsArticle(
                    title=title,
                    url=link,
                    source=f"네이버 ({source})",
                    published_at=datetime.now().isoformat(),
                    summary="",
                    hotness_score=15.0
                ))
        return articles
    except Exception as e:
        print(f"Error fetching naver main news: {e}")
        return []

def fetch_all_news() -> List[NewsArticle]:
    """모든 소스에서 뉴스를 수집합니다."""
    all_articles = []
    
    # RSS 소스
    all_articles.extend(fetch_rss_news("https://news.sbs.co.kr/news/rss.do?section=01", "SBS 뉴스", 5))
    all_articles.extend(fetch_rss_news("https://www.yna.co.kr/rss/politics.xml", "연합뉴스", 5))
    
    # 네이버 크롤링
    all_articles.extend(fetch_naver_main_hot_news(10))
    
    return all_articles
