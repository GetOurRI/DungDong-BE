# 초기 설정
INITIAL_PROMPT = """
당신은 중앙대 다빈치캠퍼스 기숙사 커뮤니티에 올라온 룸메이트 모집 게시글을 분석해,
설문 데이터 구조(survey)에 맞춰 JSON 객체로 변환하는 역할을 맡고 있습니다.
"""

TEXT_TO_JSON_PROMPT = """
다음은 중앙대 기숙사 룸메이트 구인 게시글입니다.  
이 게시글 내용을 기반으로 아래의 `survey` 데이터 구조에 맞게 JSON 객체를 생성해주세요.

규칙:
1. 명시된 정보만 반영하고, 없는 정보는 `null`, 빈 문자열("") 또는 해당 항목의 기본값으로 설정한다.
2. 설문 항목 설명에 맞춰 정수형 enum 값(0, 1, 2 등)으로 정확히 변환한다.
3. 시간은 `hh-mm` 형식으로, 24시간제를 사용한다.
4. 음주 `drink`는 `"ab-c-de"` 포맷으로 반환한다. (ab=횟수, c=단위, de=기간)  
   - 예: `"12-0-00"` → 1주에 2회
5. 단과대 `college`는 아래 숫자값으로 반환한다:
    - 0: 비공개
    - 1: 예술대학
    - 2: 체육대학
    - 3: 예술공학대학
    - 4: 생명공학대학
    - 5: 공과대학
6. selectTag는 게시글 키워드나 성향 요약 단어로 구성된 태그 리스트로 구성한다.
7. 기타 참고할만한 자유서술은 notes에 요약하여 기록한다. (30자 이내)

JSON 스키마:
```json
{
  "dorm": null,
  "birth": null,
  "studentId": null,
  "college": 0,
  "mbti": "",
  "smoke": null,
  "drink": "",
  "sdEtc": "",
  "wakeUp": "",
  "lightOff": "",
  "bedTime": "",
  "sleepHabit": 0,
  "clean": 0,
  "bug": 0,
  "eatIn": 0,
  "noise": 0,
  "share": 0,
  "home": 0,
  "selectTag": [],
  "notes": ""
}

[게시글 원문]
{{ orig_text }}
"""

IMG_TO_JSON_PROMPT = """

"""

# 응답을 JSON 형식으로 저장
JSON_OUTPUT_PROMPT = """
모든 답변은 주어진 출력형식에 따르며, JSON으로 작성합니다.
"""
