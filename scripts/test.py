#!/usr/bin/env python3
"""
Jooke Project 테스트 스크립트
주요 기능들에 대한 단위 테스트
"""

import sys
import os
import json
import unittest
from unittest.mock import Mock, patch

# 프로젝트 루트 디렉토리 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_analysis.claude_analysis import ClaudeAnalyzer
from ai_analysis.gpt_analysis import GPTAnalyzer
from ai_analysis.cross_validation import CrossValidator
from automation.customer_service import CustomerService
from collaboration.field_research import FieldResearch
from dashboard.performance_tracker import PerformanceTracker

class TestJookeSystem(unittest.TestCase):
    """
    Jooke 시스템 메인 기능 테스트
    """
    
    def setUp(self):
        """
        테스트 설정
        """
        self.test_product_data = {
            'name': 'Test Omega-3 Fish Oil',
            'price_cad': 29.99,
            'brand': 'Test Brand',
            'category': '건강식품',
            'description': 'High quality omega-3 supplement'
        }
        
        self.test_claude_result = {
            'timestamp': '2025-05-30T15:30:00',
            'analysis': 'Market potential: 8/10, Competition: 6/10',
            'status': 'success'
        }
        
        self.test_gpt_result = {
            'timestamp': '2025-05-30T15:35:00',
            'analysis': 'Expected margin: 65%, Korean price: 42000',
            'status': 'success'
        }
    
    @patch('ai_analysis.claude_analysis.Anthropic')
    def test_claude_analyzer(self, mock_anthropic):
        """
        Claude 분석기 테스트
        """
        # Mock Claude API 응답
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text='{
  "market_potential": 8,
  "competition_level": 6,
  "entry_score": 75
}')]
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        analyzer = ClaudeAnalyzer()
        result = analyzer.analyze_product(self.test_product_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('analysis', result)
        self.assertIn('timestamp', result)
    
    @patch('ai_analysis.gpt_analysis.OpenAI')
    def test_gpt_analyzer(self, mock_openai):
        """
        GPT 분석기 테스트
        """
        # Mock GPT API 응답
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{
  "expected_margin": 65,
  "korean_price": 42000
}'))]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        analyzer = GPTAnalyzer()
        result = analyzer.calculate_margins(self.test_product_data)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('analysis', result)
        self.assertIn('timestamp', result)
    
    def test_cross_validator(self):
        """
        교차 검증기 테스트
        """
        validator = CrossValidator()
        result = validator.validate_analysis(
            self.test_claude_result, 
            self.test_gpt_result
        )
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('consistency_score', result)
        self.assertIn('final_score', result)
        self.assertIn('final_recommendation', result)
        
        # 일치도 점수는 0-1 사이
        self.assertGreaterEqual(result['consistency_score'], 0)
        self.assertLessEqual(result['consistency_score'], 1)
        
        # 최종 점수는 0-100 사이
        self.assertGreaterEqual(result['final_score'], 0)
        self.assertLessEqual(result['final_score'], 100)
    
    def test_customer_service(self):
        """
        고객 서비스 자동화 테스트
        """
        cs = CustomerService()
        
        # 배송 문의 테스트
        result = cs.classify_inquiry("배송은 언제 되나요?")
        self.assertEqual(result['category'], '배송')
        self.assertFalse(result['requires_human'])
        
        # 환불 문의 테스트
        result = cs.classify_inquiry("환불 받고 싶어요")
        self.assertEqual(result['category'], '환불')
        
        # 기타 문의 테스트
        result = cs.classify_inquiry("이상한 질문입니다")
        self.assertEqual(result['category'], '기타')
        self.assertTrue(result['requires_human'])
    
    def test_field_research(self):
        """
        현지 조사 시스템 테스트
        """
        research = FieldResearch()
        
        test_data = {
            'product_name': 'Test Product',
            'store_location': 'Test Store, Toronto',
            'price_cad': 24.99,
            'quality_score': 4,
            'recommendation': '추천'
        }
        
        result = research.add_research_data(test_data)
        self.assertEqual(result['status'], 'success')
        self.assertIn('entry_id', result)
        
        # 요약 생성 테스트
        summary = research.get_research_summary()
        self.assertIn('total_products', summary)
        self.assertIn('recommended', summary)
        self.assertEqual(summary['total_products'], 1)
    
    def test_performance_tracker(self):
        """
        성과 추적기 테스트
        """
        tracker = PerformanceTracker()
        
        test_data = [
            {
                'timestamp': '2025-05-30T10:00:00',
                'product_name': 'Product 1',
                'category': '건강식품',
                'margin_percent': 65,
                'recommendation': '추천',
                'jaeho_opinion': '좋음'
            },
            {
                'timestamp': '2025-05-30T11:00:00',
                'product_name': 'Product 2',
                'category': '펫용품',
                'margin_percent': 45,
                'recommendation': '보류',
                'jaeho_opinion': ''
            }
        ]
        
        # KPI 계산 테스트
        kpis = tracker.calculate_kpis(test_data)
        self.assertEqual(kpis['analysis_count'], 2)
        self.assertEqual(kpis['success_rate'], 50.0)  # 1/2 = 50%
        self.assertEqual(kpis['avg_margin'], 55.0)    # (65+45)/2 = 55%
        
        # 주간 리포트 테스트
        report = tracker.generate_weekly_report(test_data)
        self.assertIn('summary', report)
        self.assertIn('top_products', report)
        self.assertIn('insights', report)

class TestIntegration(unittest.TestCase):
    """
    통합 테스트
    """
    
    def test_full_pipeline_mock(self):
        """
        전체 파이프라인 목 테스트
        """
        # 목 데이터
        product_data = {
            'name': 'Test Product',
            'price_cad': 29.99,
            'category': '건강식품'
        }
        
        claude_result = {
            'status': 'success',
            'analysis': 'Good product',
            'timestamp': '2025-05-30T15:30:00'
        }
        
        gpt_result = {
            'status': 'success', 
            'analysis': 'High margin',
            'timestamp': '2025-05-30T15:35:00'
        }
        
        # 교차 검증
        validator = CrossValidator()
        validation_result = validator.validate_analysis(claude_result, gpt_result)
        
        # 결과 검증
        self.assertEqual(validation_result['status'], 'success')
        self.assertIn('final_recommendation', validation_result)
        
        recommendation = validation_result['final_recommendation']
        self.assertIn('decision', recommendation)
        self.assertIn('confidence', recommendation)
        self.assertIn('next_steps', recommendation)

def run_tests():
    """
    모든 테스트 실행
    """
    print("🧪 Jooke AI Sourcing 테스트 실행 중...")
    print("="*50)
    
    # 테스트 실행
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 테스트 케이스 추가
    suite.addTests(loader.loadTestsFromTestCase(TestJookeSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 결과 요약
    print("\n" + "="*50)
    print("📊 테스트 결과 요약")
    print("="*50)
    print(f"📝 전체 테스트: {result.testsRun}개")
    print(f"✅ 성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"❌ 실패: {len(result.failures)}개")
    print(f"💥 오류: {len(result.errors)}개")
    
    if result.failures:
        print("\n🔴 실패한 테스트:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 오류가 발생한 테스트:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # 전체 성공 여부
    if result.wasSuccessful():
        print("\n🎉 모든 테스트 통과!")
        return True
    else:
        print("\n😨 일부 테스트 실패")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)