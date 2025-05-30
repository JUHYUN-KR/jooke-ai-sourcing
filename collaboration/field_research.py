#!/usr/bin/env python3
"""
현지 조사 데이터 수집 시스템
- 재호의 현지 조사 결과 자동 입력
- 모바일 최적화 폼
- 실시간 동기화
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

class FieldResearch:
    def __init__(self):
        self.research_data = []
        
    def add_research_data(self, data):
        """
        현지 조사 데이터 추가
        """
        research_entry = {
            'timestamp': datetime.now().isoformat(),
            'product_name': data.get('product_name', ''),
            'store_location': data.get('store_location', ''),
            'price_cad': data.get('price_cad', 0),
            'discount_info': data.get('discount_info', ''),
            'stock_status': data.get('stock_status', ''),
            'photo_urls': data.get('photo_urls', []),
            'notes': data.get('notes', ''),
            'researcher': '재호',
            'quality_score': data.get('quality_score', 0),  # 1-5점
            'recommendation': data.get('recommendation', '')  # 추천/보류/비추천
        }
        
        self.research_data.append(research_entry)
        
        return {
            'status': 'success',
            'entry_id': len(self.research_data),
            'timestamp': research_entry['timestamp']
        }
    
    def get_research_summary(self, days=7):
        """
        최근 조사 결과 요약
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_data = [entry for entry in self.research_data 
                      if datetime.fromisoformat(entry['timestamp']) > cutoff_date]
        
        summary = {
            'total_products': len(recent_data),
            'recommended': len([d for d in recent_data if d['recommendation'] == '추천']),
            'average_quality': sum([d['quality_score'] for d in recent_data]) / len(recent_data) if recent_data else 0,
            'stores_visited': len(set([d['store_location'] for d in recent_data])),
            'latest_research': recent_data[-5:] if recent_data else []
        }
        
        return summary
    
    def export_to_sheets(self):
        """
        Google Sheets로 데이터 내보내기
        """
        # automation/google_sheets_sync.py와 연동
        pass

if __name__ == "__main__":
    research = FieldResearch()
    
    # 테스트 데이터
    test_data = {
        'product_name': 'Nature\'s Bounty Omega-3',
        'store_location': 'Shoppers Drug Mart, Toronto',
        'price_cad': 24.99,
        'discount_info': '30% off regular price',
        'stock_status': '재고 충분',
        'quality_score': 4,
        'recommendation': '추천',
        'notes': '인기 상품으로 보임. 현지 고객들이 많이 구매'
    }
    
    result = research.add_research_data(test_data)
    summary = research.get_research_summary()
    
    print("Research Result:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("\nSummary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))