# src/service/ai/llm_api.py

from typing import Any, Dict
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError  

import src.common.common_codes as codes
from src.service.ai.asset.prompts.prompts_cfg import (
    SYSTEM_PROMPTS,
    SURVEY_TEXT_PROMPTS,
)
from src.service.ai.llm_schemas import SurveyTextReq, SurveyReports

router = APIRouter(prefix="/v1/generate", tags=["generate"])


@router.post("/survey")
async def generate_survey(request: Request, body: SurveyTextReq):
    """
    프론트엔드에서 전달받은 tid, orig_text를 기반으로 LLM 호출 수행 후
    파싱 결과(reports) 반환
    """
    ctx = request.app.state.ctx
    tid = body.tid
    orig_text = body.orig_text

    try:
        resp_text = await ctx.llm_manager.generate(
            SURVEY_TEXT_PROMPTS,
            placeholders={"orig_text": orig_text},
            temperature=0.7,
        )
        # print(resp_text)
        parsed: Dict[str, Any] = ctx.llm_manager.parse_result(resp_text)

        # reports 스키마 검증
        reports_valid = SurveyReports(**parsed).model_dump()

        # 성공 응답
        return JSONResponse(
            status_code=200,
            content={
                "tid": tid,
                "status": codes.ResponseStatus.SUCCESS,
                "data": reports_valid
            },
        )
    
    # 스키마 위반
    except ValidationError as ve:
        
        return JSONResponse(
            status_code=502,
            content={
                "tid": tid,
                "status": {
                    **codes.ResponseStatus.SERVER_ERROR,
                    "detail": f"Schema validation failed: {ve.errors()}",
                },
                "data": None,
            },
        )

    # 일반 예외 
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "tid": tid,
                "status": {
                    **codes.ResponseStatus.SERVER_ERROR,
                    "detail": str(e),
                },
                "data": None,
            },
        )
