# service/llm_api.py

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.responses import JSONResponse

import src.common.common_codes as codes
from src.service.ai.asset.prompts.prompts_cfg import (SYSTEM_PROMPTS, 
                                                      SURVEY_TEXT_PROMPTS)

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
        return JSONResponse(
            status_code=400,
            content={
                "status": codes.ResponseStatus.BAD_REQUEST
            }
        )
    try:
        resp_text = await ctx.llm_manager.generate(
            SURVEY_TEXT_PROMPTS,
            placeholders={"orig_text": orig_text},
            temperature=0.7,
        )

        parsed = ctx.llm_manager.parse_reports(resp_text)

        return JSONResponse(
            status_code=200,
            content={
                "status": codes.ResponseStatus.SUCCESS,
                "data": parsed
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "status": {
                    **codes.ResponseStatus.SERVER_ERROR,
                    "detail": str(e)
                },
            }
        )