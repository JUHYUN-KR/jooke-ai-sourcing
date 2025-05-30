#!/usr/bin/env python3
"""
GPT-4o 보조 분석 모듈
- 마진 계산
- 마케팅 분석
- 실용적 계산 처리
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GPTAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def calculate_margins(self, product_data, exchange_rate=1350):
        """
        마진 계산 및 마케팅 분석
        """
        prompt = f"""
        캐나다 제품의 한국 진출 마진 계산을 해주세요:
        
        제품: {json.dumps(product_data, ensure_ascii=False)}
        환율: {exchange_rate} 원/CAD
        
        계산 항목:
        1. 한국 예상 판매가 (원)
        2. 순마진 (%)
        3. 배송비 포함 총비용
        4. 경쟁 제품 가격대
        5. 마케팅 포인트 3가지
        6. 인스타그램 해시태그 10개
        7. 제품 설명문 (50자 이내)
        
        JSON 형태로 정확한 숫자와 함께 응답해주세요.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            return {
                'timestamp': datetime.now().isoformat(),
                'analysis': response.choices[0].message.content,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'status': 'failed'
            }

if __name__ == "__main__":
    analyzer = GPTAnalyzer()
    
    # 테스트 데이터
    test_product = {
        'name': 'Canadian Omega-3 Fish Oil',
        'price_cad': 29.99,
        'brand': 'NaturePath',
        'category': '건강식품'
    }
    
    result = analyzer.calculate_margins(test_product)
    print(json.dumps(result, ensure_ascii=False, indent=2))