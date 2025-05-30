#!/usr/bin/env python3
"""
Jooke API 연동 테스트 스크립트
환경변수에서 API 키를 읽어서 연결 테스트
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

class JookeAPITester:
    def __init__(self):
        # .env 파일에서 API 키 로드
        load_dotenv()
        
        self.claude_key = os.getenv('CLAUDE_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.firecrawl_key = os.getenv('FIRECRAWL_API_KEY')
        
        print("🚀 Jooke API 연동 테스트 시작")
        print("=" * 50)
        print(f"테스트 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # API 키 존재 여부 확인
        self._check_api_keys()
        print()
    
    def _check_api_keys(self):
        """API 키 존재 여부 확인"""
        keys = {
            "Claude": self.claude_key,
            "OpenAI": self.openai_key,
            "Firecrawl": self.firecrawl_key
        }
        
        print("\n🔑 API 키 확인:")
        all_keys_present = True
        
        for name, key in keys.items():
            if key and len(key) > 10:
                print(f"✅ {name}: 키 존재 (길이: {len(key)})")
            else:
                print(f"❌ {name}: 키 없음 또는 잘못됨")
                all_keys_present = False
        
        if not all_keys_present:
            print("\n⚠️ .env 파일에 올바른 API 키를 설정해주세요!")
            return False
        return True
    
    def test_claude_api(self):
        """Claude API 연결 테스트"""
        print("🤖 Claude API 테스트 중...")
        
        if not self.claude_key:
            print("❌ Claude API 키가 없습니다.")
            return False, "No API key"
        
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.claude_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        data = {
            "model": "claude-3-sonnet-20241022",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "안녕하세요! '연결 성공'이라고 간단히 답해주세요."}
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                print(f"✅ Claude 연결 성공!")
                print(f"   응답: {content}")
                return True, content
            else:
                print(f"❌ Claude 연결 실패: {response.status_code}")
                print(f"   오류: {response.text[:200]}")
                return False, response.text
                
        except Exception as e:
            print(f"❌ Claude 연결 오류: {str(e)}")
            return False, str(e)
    
    def test_openai_api(self):
        """OpenAI API 연결 테스트"""
        print("\n🧠 OpenAI API 테스트 중...")
        
        if not self.openai_key:
            print("❌ OpenAI API 키가 없습니다.")
            return False, "No API key"
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "user", "content": "간단히 '연결 성공'이라고 답해주세요."}
            ],
            "max_tokens": 50
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"✅ OpenAI 연결 성공!")
                print(f"   응답: {content}")
                return True, content
            else:
                print(f"❌ OpenAI 연결 실패: {response.status_code}")
                print(f"   오류: {response.text[:200]}")
                return False, response.text
                
        except Exception as e:
            print(f"❌ OpenAI 연결 오류: {str(e)}")
            return False, str(e)
    
    def test_firecrawl_api(self):
        """Firecrawl API 연결 테스트"""
        print("\n🔥 Firecrawl API 테스트 중...")
        
        if not self.firecrawl_key:
            print("❌ Firecrawl API 키가 없습니다.")
            return False, "No API key"
        
        url = "https://api.firecrawl.dev/v1/scrape"
        headers = {
            "Authorization": f"Bearer {self.firecrawl_key}",
            "Content-Type": "application/json"
        }
        
        # 간단한 테스트 페이지
        data = {
            "url": "https://example.com",
            "formats": ["markdown"]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                markdown_content = result.get('markdown', '')[:100]
                print(f"✅ Firecrawl 연결 성공!")
                print(f"   크롤링 샘플: {markdown_content}...")
                return True, result
            else:
                print(f"❌ Firecrawl 연결 실패: {response.status_code}")
                print(f"   오류: {response.text[:200]}")
                return False, response.text
                
        except Exception as e:
            print(f"❌ Firecrawl 연결 오류: {str(e)}")
            return False, str(e)
    
    def test_pet_product_analysis(self):
        """실제 펫 제품 분석 테스트"""
        print("\n🐕 펫 제품 AI 분석 통합 테스트...")
        
        # 테스트용 제품 데이터
        test_product = {
            "name": "Omega Alpha Wild Fish Oil for Dogs & Cats",
            "price_cad": 32.99,
            "brand": "Omega Alpha", 
            "category": "펫 건강식품",
            "description": "Wild-caught fish oil supplement for joint health and shiny coat"
        }
        
        print(f"테스트 제품: {test_product['name']}")
        
        # Claude 분석 테스트
        claude_success, claude_result = self._test_claude_analysis(test_product)
        
        # OpenAI 분석 테스트  
        openai_success, openai_result = self._test_openai_analysis(test_product)
        
        if claude_success and openai_success:
            print("✅ 펫 제품 AI 분석 통합 테스트 성공!")
            print("   → 실제 Jooke 워크플로우 준비 완료!")
            return True
        else:
            print("❌ 펫 제품 AI 분석 테스트 실패")
            return False
    
    def _test_claude_analysis(self, product_data):
        """Claude 제품 분석 테스트"""
        prompt = f"""
        다음 캐나다 펫 제품을 한국 시장 진출 관점에서 분석해주세요:
        
        제품명: {product_data['name']}
        가격: ${product_data['price_cad']} CAD
        브랜드: {product_data['brand']}
        설명: {product_data['description']}
        
        1-10점 척도로 시장성을 평가하고, 간단한 추천 의견을 주세요.
        """
        
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": self.claude_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": "claude-3-sonnet-20241022",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                print(f"   Claude 분석 샘플: {content[:100]}...")
                return True, content
            else:
                return False, response.text
                
        except Exception as e:
            return False, str(e)
    
    def _test_openai_analysis(self, product_data):
        """OpenAI 마진 계산 테스트"""
        prompt = f"""
        캐나다 펫 제품의 한국 진출 마진을 계산해주세요:
        
        제품: {product_data['name']}
        원가: ${product_data['price_cad']} CAD
        환율: 1350원/CAD
        
        배송비, 관세 등을 고려한 총 원가와 적정 판매가를 제안해주세요.
        """
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.openai_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 300
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                print(f"   OpenAI 분석 샘플: {content[:100]}...")
                return True, content
            else:
                return False, response.text
                
        except Exception as e:
            return False, str(e)
    
    def run_all_tests(self):
        """모든 API 테스트 실행"""
        results = {}
        
        # 각 API 테스트
        results['claude'] = self.test_claude_api()
        results['openai'] = self.test_openai_api()
        results['firecrawl'] = self.test_firecrawl_api()
        
        # 통합 테스트 (모든 API가 성공한 경우에만)
        if all(result[0] for result in results.values()):
            results['integration'] = (self.test_pet_product_analysis(), "펫 제품 분석")
        else:
            print("\n⚠️ 일부 API 연결 실패로 통합 테스트 생략")
        
        # 결과 요약
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results):
        """테스트 결과 요약 출력"""
        print("\n" + "=" * 50)
        print("🏁 테스트 결과 요약")
        print("=" * 50)
        
        success_count = 0
        total_count = len(results)
        
        for api_name, (success, _) in results.items():
            status = "✅ 성공" if success else "❌ 실패"
            print(f"{api_name:15}: {status}")
            if success:
                success_count += 1
        
        print(f"\n총 {total_count}개 중 {success_count}개 성공")
        
        if success_count == total_count:
            print("🎉 모든 API 연결 성공! Jooke 시스템 준비 완료!")
            print("   → 다음 단계: Google Sheets 연동")
        elif success_count >= total_count * 0.7:
            print("⚠️ 대부분 성공! 일부 오류 해결 후 진행 가능")  
        else:
            print("🚨 다수 실패! API 키 및 설정 점검 필요")
            print("   → .env 파일의 API 키를 확인해주세요")

if __name__ == "__main__":
    print("🔧 API 연동 테스트를 위해 .env 파일에 다음 키들이 필요합니다:")
    print("   - CLAUDE_API_KEY")
    print("   - OPENAI_API_KEY") 
    print("   - FIRECRAWL_API_KEY")
    print("\n실행: python test_api_connections.py")
    print()
    
    tester = JookeAPITester()
    results = tester.run_all_tests()
