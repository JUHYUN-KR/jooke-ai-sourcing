#!/usr/bin/env python3
"""
간단한 API 테스트 스크립트 (API 키 없이)
"""

def test_api_keys():
    """API 키 검증 테스트"""
    import os
    
    print("🔑 API 키 확인 중...")
    
    # 환경변수에서 키 확인
    keys = {
        "Claude": os.getenv('CLAUDE_API_KEY', ''),
        "OpenAI": os.getenv('OPENAI_API_KEY', ''), 
        "Firecrawl": os.getenv('FIRECRAWL_API_KEY', '')
    }
    
    for name, key in keys.items():
        if key and len(key) > 10:
            print(f"✅ {name}: 키 존재 (길이: {len(key)})")
        else:
            print(f"❌ {name}: 키 없음")
    
    return all(len(key) > 10 for key in keys.values())

def test_imports():
    """필수 라이브러리 import 테스트"""
    print("\n📦 라이브러리 확인 중...")
    
    try:
        import anthropic
        print("✅ anthropic 설치됨")
    except ImportError:
        print("❌ anthropic 설치 필요: pip install anthropic")
    
    try:
        import openai
        print("✅ openai 설치됨")
    except ImportError:
        print("❌ openai 설치 필요: pip install openai")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv 설치됨")
    except ImportError:
        print("❌ python-dotenv 설치 필요: pip install python-dotenv")

if __name__ == "__main__":
    print("🚀 Jooke 프로젝트 기본 테스트")
    print("=" * 40)
    
    # .env 파일 로드 시도
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env 파일 로드 성공")
    except:
        print("❌ .env 파일 또는 python-dotenv 없음")
    
    test_imports()
    api_ok = test_api_keys()
    
    print("\n" + "=" * 40)
    if api_ok:
        print("🎉 기본 설정 완료! 다음 단계 진행 가능")
    else:
        print("⚠️ API 키 설정 필요")
