#!/usr/bin/env python3
"""
Claude 구조적 분석 모듈
- 제품 데이터 구조화
- 한국 시장 분석
- 경쟁력 평가
"""

import os
import json
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeAnalyzer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
        
    def analyze_product(self, product_data):
        """
        제품 구조적 분석
        """
        prompt = f"""
        다음 캐나다 제품을 한국 시장 진출 관점에서 분석해주세요:
        
        제품 정보: {json.dumps(product_data, ensure_ascii=False, indent=2)}
        
        분석 항목:
        1. 시장성 (1-10점)
        2. 경쟁강도 (1-10점)
        3. 마진 예상 (%)
        4. 진출 점수 (1-100점)
        5. 핵심 키워드 (5개)
        6. 타겟 고객
        7. 리스크 요소
        8. 추천 여부 (예/아니오)
        
        JSON 형태로 응답해주세요.
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'analysis': response.content[0].text,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'failed'
            }

if __name__ == "__main__":
    analyzer = ClaudeAnalyzer()
    
    # 테스트 데이터
    test_product = {
        'name': 'Canadian Omega-3 Fish Oil',
        'price_cad': 29.99,
        'brand': 'NaturePath',
        'category': '건강식품',
        'description': 'Wild-caught salmon oil supplement'
    }
    
    result = analyzer.analyze_product(test_product)
    print(json.dumps(result, ensure_ascii=False, indent=2))