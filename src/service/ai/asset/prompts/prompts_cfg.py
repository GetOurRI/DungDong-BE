import service.ai.asset.prompts.dungdong_prompts as dungdong_prompts

# 시스템 프롬프트 
SYSTEM_PROMPTS = [
    dungdong_prompts.INITIAL_PROMPT   
]

# 게시글 변환 프롬프트
SURVEY_TEXT_PROMPTS  = [
    dungdong_prompts.INITIAL_PROMPT,
    dungdong_prompts.TEXT_TO_JSON_PROMPT,
    dungdong_prompts.JSON_OUTPUT_PROMPT
]