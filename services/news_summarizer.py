"""
뉴스 요약 및 포맷팅 모듈
뉴스 본문을 요약하거나 마크다운 형식으로 변환합니다.
"""
from typing import List
from models import NewsArticle

def summarize_article(article: NewsArticle) -> str:
    """
    기사를 요약합니다. 
    (현재는 RSS 피드의 description을 활용하거나 제목을 활용하는 간단 버전)
    """
    if article.summary and len(article.summary) > 20:
        # 이미 요약(description)이 있는 경우 짧게 자름
        summary = article.summary.strip()
        if len(summary) > 200:
            summary = summary[:197] + "..."
        return summary
    else:
        # 요약이 없는 경우 제목을 기반으로 생성 (추후 AI 연동 가능)
        return f"'{article.title}'에 대한 상세 내용은 원문 링크를 참조하세요."

def format_as_markdown(articles: List[NewsArticle]) -> str:
    """뉴스 목록을 마크다운 형식으로 변환합니다."""
    from datetime import datetime
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"# 🚀 오늘의 Hot 뉴스 Top {len(articles)}\n\n"
    md += f"*생성 시간: {now} (KST)*\n\n"
    md += "---\n\n"
    
    for i, article in enumerate(articles, 1):
        summary = summarize_article(article)
        md += f"## {i}. [{article.title}]({article.url})\n"
        md += f"**출처**: {article.source} | **발행**: {article.published_at}\n\n"
        md += f"{summary}\n\n"
        md += "---\n\n"
    
    md += "*이 뉴스는 자동으로 수집 및 선별되었습니다.*\n"
    return md
