"""
뉴스 처리 모듈
뉴스 중복 제거 및 Hot 뉴스 선별 로직을 담당합니다.
"""
from typing import List
from models import NewsArticle
from difflib import SequenceMatcher

def calculate_similarity(a: str, b: str) -> float:
    """두 문자열의 유사도를 계산합니다."""
    return SequenceMatcher(None, a, b).ratio()

def remove_duplicates(articles: List[NewsArticle], threshold: float = 0.8) -> List[NewsArticle]:
    """
    중복된 뉴스를 제거합니다. 제목 유사도가 threshold 이상인 경우 중복으로 간주합니다.
    """
    unique_articles = []
    
    for article in articles:
        is_duplicate = False
        for unique in unique_articles:
            # 제목 유사도 체크
            if calculate_similarity(article.title, unique.title) > threshold:
                is_duplicate = True
                # 기사가 중복될 경우, 정보를 병합하거나 점수를 높일 수 있음
                unique.hotness_score = (unique.hotness_score or 0.0) + 5.0
                break
        
        if not is_duplicate:
            unique_articles.append(article)
            
    return unique_articles

def score_articles(articles: List[NewsArticle]) -> List[NewsArticle]:
    """뉴스 기사의 Hot 점수를 계산하고 정렬합니다."""
    for article in articles:
        # 기본 점수 설정 (fetcher에서 설정한 점수가 있으면 사용)
        base_score = article.hotness_score or 0.0
        
        # 소스별 가중치 (임의 설정)
        if "메인" in article.source:
            base_score += 10.0
        elif "RSS" in article.source:
            base_score += 5.0
            
        # 최신성 가중치 (발행일이 오늘이면 가점)
        # 생략 (간단하게 유지)
        
        article.hotness_score = base_score
        
    # 점수 높은 순으로 정렬
    sorted_articles = sorted(articles, key=lambda x: x.hotness_score, reverse=True)
    return sorted_articles

def get_top_n_news(articles: List[NewsArticle], n: int = 5) -> List[NewsArticle]:
    """중복 제거 및 점수 계산 후 상위 n개의 뉴스를 반환합니다."""
    # 1. 중복 제거
    unique_articles = remove_duplicates(articles)
    
    # 2. 점수 계산 및 정렬
    scored_articles = score_articles(unique_articles)
    
    # 3. 상위 N개 추출
    return scored_articles[:n]
