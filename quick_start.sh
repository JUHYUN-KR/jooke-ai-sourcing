#!/bin/bash

# Jooke 프로젝트 원클릭 실행 스크립트

echo "🚀 Jooke AI Sourcing 원클릭 실행 시작!"
echo "=================================="

# 1. 필수 라이브러리 설치
echo "📦 필수 라이브러리 설치 중..."
pip install anthropic openai python-dotenv requests

# 2. .env 파일 체크
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. 생성 중..."
    cp .env.example .env
    echo "✅ .env 파일 생성 완료"
    echo ""
    echo "🔑 다음 API 키들을 .env 파일에 입력해주세요:"
    echo "- CLAUDE_API_KEY"
    echo "- OPENAI_API_KEY"
    echo "- FIRECRAWL_API_KEY"
    echo ""
    echo "편집: nano .env"
    exit 1
fi

# 3. 기본 테스트 실행
echo "🧪 기본 설정 테스트 중..."
python scripts/basic_test.py

echo ""
echo "🎉 설정이 완료되면 다음 명령어로 시작:"
echo "python main.py demo"