#!/usr/bin/env python3
"""
고객 응대 자동화 시스템
- FAQ 자동 응답
- 알림톡 발송
- DM 자동 분류
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CustomerService:
    def __init__(self):
        self.faq_data = self.load_faq_templates()
        
    def load_faq_templates(self):
        """
        FAQ 템플릿 로드
        """
        return {
            '배송': {
                'keywords': ['배송', '언제', '얼마나', '기간', '도착'],
                'response': '일반적으로 캐나다에서 한국까지 7-15일 소요됩니다. 통관 절차에 따라 다소 지연될 수 있으며, 배송 현황은 실시간으로 안내드립니다.'
            },
            '환불': {
                'keywords': ['환불', '취소', '반품', '교환'],
                'response': '미개봉 제품에 한해 수령 후 7일 이내 환불 가능합니다. 상품 하자나 오배송의 경우 배송비는 저희가 부담합니다.'
            },
            '성분': {
                'keywords': ['성분', '원료', '안전', '부작용', '알레르기'],
                'response': '모든 제품은 캐나다 Health Canada 승인을 받은 안전한 제품입니다. 알레르기가 있으시다면 성분표를 꼭 확인해주세요.'
            },
            '가격': {
                'keywords': ['가격', '할인', '쿠폰', '이벤트', '세일'],
                'response': '현재 신규 고객 10% 할인 이벤트를 진행 중입니다. 정기 구독 시 추가 할인 혜택이 있습니다.'
            }
        }
    
    def classify_inquiry(self, message):
        """
        문의 자동 분류
        """
        message_lower = message.lower()
        
        for category, data in self.faq_data.items():
            for keyword in data['keywords']:
                if keyword in message_lower:
                    return {
                        'category': category,
                        'confidence': 0.8,
                        'auto_response': data['response'],
                        'requires_human': False
                    }
        
        return {
            'category': '기타',
            'confidence': 0.3,
            'auto_response': '문의사항을 확인하고 빠른 시간 내에 답변드리겠습니다.',
            'requires_human': True
        }
    
    def send_notification(self, phone_number, message_type, order_data=None):
        """
        알림톡 발송
        """
        templates = {
            'order_confirmed': '주문이 확인되었습니다. 주문번호: {order_id}\n상품: {product_name}\n예상 배송: 7-15일',
            'shipped': '상품이 발송되었습니다. 추적번호: {tracking_number}\n배송조회: jooke.shop/tracking',
            'delivered': '상품이 배송완료되었습니다.\n만족하셨다면 리뷰 작성 부탁드립니다.\n혜택: 다음 구매 시 5% 할인'
        }
        
        if message_type in templates and order_data:
            message = templates[message_type].format(**order_data)
            
            # 실제 알림톡 API 호출 (Kakao Business API)
            # 현재는 로그만 출력
            print(f"알림톡 발송: {phone_number}")
            print(f"메시지: {message}")
            
            return {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'recipient': phone_number,
                'message_type': message_type
            }
        
        return {'status': 'failed', 'error': 'Invalid template or data'}

if __name__ == "__main__":
    cs = CustomerService()
    
    # 테스트
    test_inquiry = "배송은 언제 되나요?"
    result = cs.classify_inquiry(test_inquiry)
    print(json.dumps(result, ensure_ascii=False, indent=2))