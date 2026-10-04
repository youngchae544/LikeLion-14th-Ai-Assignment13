import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("GEMINI_API_KEY가 없습니다. .env 파일에 키를 입력했는지 확인하세요.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"

IMAGE_PATH = "images/content.jpg"


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"이미지를 찾을 수 없습니다: {IMAGE_PATH}")
        print("images 폴더에 content.jpg를 넣어주세요")
        sys.exit(1)

    # 사용자에게 원하는 콘텐츠 입력받기
    user_input = input(
        "현재 기분이나 원하는 콘텐츠를 입력해주세요: "
    )

    with open(IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg",
    )

    # 이미지 + 텍스트를 함께 사용하는 멀티모달 프롬프트
    prompt = f"""
당신은 영화와 드라마를 추천해주는 AI 콘텐츠 추천 서비스 MoodPick입니다.

사용자가 입력한 내용:
"{user_input}"

첨부된 콘텐츠 이미지를 분석하고 사용자의 입력을 함께 고려하여
가장 적합한 콘텐츠를 추천해주세요.

다음 형식으로 답변해주세요.

- 추천 콘텐츠
- 장르
- 분위기
- 추천 이유
- 비슷한 콘텐츠

이미지에서 확인할 수 없는 정보나 근거가 없는 내용은 만들어내지 마세요.
"""

    print("\nGemini API 호출 중...")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[image_part, prompt],
        )
    except Exception as e:
        print("API 호출 중 오류가 발생했습니다:", e)
        sys.exit(1)

    print("\n=== MoodPick 추천 결과 ===\n")
    print(response.text)


if __name__ == "__main__":
    main()