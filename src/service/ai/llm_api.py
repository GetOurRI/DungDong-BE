# v1 기본 예제
# service/v1/analyze_api.py

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Dict, Iterable, Any

import httpx
from fastapi import APIRouter, HTTPException, Request

import src.common.common_codes as codes
from src.service.ai.asset.prompts.prompts_cfg import (SYSTEM_PROMPTS, 
                                                      SURVEY_PROMPTS)

# 라우터 등록은 여기서 하고 실제 로직은 service에서 관리
# http://localhost:8000/

router = APIRouter(prefix="/v1/generate", tags=["generate"])

# POST /v1/generate/survey
@router.post("/survey")
async def generate_survey(request: Request, data: Dict[str, Any] = Body(...)):
    """
    프론트엔드에서 전달받은 orig_text를 기반으로 LLM 호출 수행
    """
    ctx = request.app.state.ctx
    orig_text = data.get("orig_text")

    if not orig_text:
        raise HTTPException(status_code=400, detail="Missing field: orig_text")

    try:
        # LLM 호출
        resp_text = await ctx.llm_manager.generate(
            SURVEY_PROMPTS,
            placeholders={"orig_text": orig_text},
            temperature=0.7,
        )

        # 결과 파싱 후 반환
        return ctx.llm_manager.parse_reports(resp_text)

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM generation failed: {e}")