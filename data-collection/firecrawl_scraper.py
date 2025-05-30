#!/usr/bin/env python3
"""
Firecrawl 기반 캐나다 사이트 크롤링
"""

import os
import json
from datetime import datetime
from firecrawl import FirecrawlApp
from dotenv import load_dotenv

load_dotenv()

class FirecrawlScraper:
    def __init__(self):
        self.app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        
    def scrape_product_page(self, url):
        """
        제품 페이지 크롤링
        """
        try:
            # 제품 정보 추출을 위한 스키마
            extract_schema = {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string"},
                    "price": {"type": "string"},
                    "brand": {"type": "string"},
                    "description": {"type": "string"},
                    "ingredients": {"type": "array"},
                    "reviews_count": {"type": "number"},
                    "rating": {"type": "number"}
                },
                "required": ["product_name", "price"]
            }
            
            result = self.app.scrape_url(
                url, 
                {
                    'formats': ['markdown', 'extract'],
                    'extract': {
                        'schema': extract_schema
                    }
                }
            )
            
            return {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'failed'
            }
            
    def scrape_category(self, base_url, max_pages=5):
        """
        카테고리 페이지 크롤링
        """
        try:
            result = self.app.crawl_url(
                base_url,
                {
                    'crawlerOptions': {
                        'maxDepth': 2,
                        'limit': max_pages
                    },
                    'pageOptions': {
                        'formats': ['markdown']
                    }
                }
            )
            
            return {
                'base_url': base_url,
                'timestamp': datetime.now().isoformat(),
                'pages_crawled': len(result.get('data', [])),
                'data': result,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'base_url': base_url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'failed'
            }

if __name__ == "__main__":
    scraper = FirecrawlScraper()
    
    # 테스트 URL
    test_url = "https://well.ca/categories/vitamins-supplements_3.html"
    
    result = scraper.scrape_category(test_url, max_pages=3)
    print(json.dumps(result, ensure_ascii=False, indent=2))