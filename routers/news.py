"""
뉴스 관련 API 라우터
"""
from fastapi import APIRouter, Query, HTTPException
from typing import List, Union, Optional
from models import NewsArticle
from services import news_fetcher, news_processor, news_summarizer

router = APIRouter(prefix="/api/news", tags=["News"])

@router.get("/top", summary="Top 5 뉴스 조회")
def get_top_news(
    n: int = Query(5, description="추출할 뉴스 개수", ge=1, le=20),
    format: str = Query("json", description="응답 형식 (json, markdown)")
) -> Union[List[NewsArticle], dict]:
    """
    현재 시간 기준으로 주요 뉴스 소스에서 Top 5 뉴스를 수집, 중복 제거 및 선별하여 반환합니다.
    """
    try:
        # 1. 모든 소스에서 뉴스 수집
        all_articles = news_fetcher.fetch_all_news()
        
        if not all_articles:
            raise HTTPException(status_code=500, detail="뉴스를 수집할 수 없습니다.")
        
        # 2. 중복 제거 및 상위 N개 선별
        top_news = news_processor.get_top_n_news(all_articles, n=n)
        
        # 3. 형식에 맞게 응답
        if format.lower() == "markdown":
            markdown_content = news_summarizer.format_as_markdown(top_news)
            return {"markdown": markdown_content}
        
        # JSON 형식인 경우 요약 추가
        for article in top_news:
            article.summary = news_summarizer.summarize_article(article)
            
        return top_news
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-fetch", summary="뉴스 수집 테스트")
def test_fetch():
    """뉴스 수집이 정상적으로 작동하는지 테스트합니다."""
    rss = news_fetcher.fetch_naver_rss_news(1)
    main = news_fetcher.fetch_naver_main_hot_news(1)
    return {
        "rss_sample": rss,
        "main_sample": main,
        "total_fetched": len(rss) + len(main)
    }
