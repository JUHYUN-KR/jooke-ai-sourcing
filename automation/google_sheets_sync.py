#!/usr/bin/env python3
"""
Google Sheets 연동 모듈
- AI 분석 결과 자동 입력
- 실시간 데이터 동기화
"""

import os
import json
from datetime import datetime
import gspread
from google.auth import default
from dotenv import load_dotenv

load_dotenv()

class GoogleSheetsSync:
    def __init__(self):
        # Google Sheets 인증
        self.gc = gspread.service_account(filename=os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
        self.sheet_id = os.getenv('SHEET_ID')
        
    def update_analysis_result(self, product_data, claude_result, gpt_result):
        """
        분석 결과를 Google Sheets에 업데이트
        """
        try:
            workbook = self.gc.open_by_key(self.sheet_id)
            worksheet = workbook.worksheet('분석결과')
            
            # 새 행 데이터 준비
            row_data = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 수집일자
                product_data.get('source_url', ''),            # 출처사이트
                product_data.get('name', ''),                  # 제품명
                product_data.get('brand', ''),                 # 브랜드
                product_data.get('price_cad', ''),             # 캐나다가격
                product_data.get('category', ''),              # 카테고리
                product_data.get('ingredients', ''),           # 주요성분
                product_data.get('rating', ''),                # 평점
                product_data.get('description', ''),           # 제품설명
                '',  # 핵심키워드 (AI가 채움)
                '',  # 타겟키워드 (AI가 채움)
                '',  # 검색량추정
                '',  # 경쟁강도
                '',  # 마진예상
                '',  # 진출점수
                '',  # 상태
                json.dumps(claude_result, ensure_ascii=False),  # Claude분석
                json.dumps(gpt_result, ensure_ascii=False),     # ChatGPT분석
                '',  # 교차검증
                '',  # 최종결론
                '',  # 재호의견
                ''   # 최종합의
            ]
            
            worksheet.append_row(row_data)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'message': 'Data updated successfully'
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e)
            }
    
    def create_analysis_sheet(self):
        """
        분석용 시트 헤더 생성
        """
        headers = [
            '수집일자', '출처사이트', '제품명', '브랜드', '캐나다가격', '카테고리',
            '주요성분', '평점', '제품설명', '핵심키워드', '타겟키워드',
            '검색량추정', '경쟁강도', '마진예상', '진출점수', '상태',
            'Claude분석', 'ChatGPT분석', '교차검증', '최종결론',
            '재호의견', '최종합의'
        ]
        
        try:
            workbook = self.gc.open_by_key(self.sheet_id)
            worksheet = workbook.add_worksheet(title='분석결과', rows=1000, cols=len(headers))
            worksheet.append_row(headers)
            
            return {'status': 'success', 'message': 'Analysis sheet created'}
            
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}

if __name__ == "__main__":
    sync = GoogleSheetsSync()
    result = sync.create_analysis_sheet()
    print(json.dumps(result, ensure_ascii=False, indent=2))