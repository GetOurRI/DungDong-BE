# src/service/ai/llm_schemas.py
from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, field_validator
import re

# ---------- Request ----------

class SurveyTextReq(BaseModel):
    """
    설문 JSON 생성을 위한 요청 스키마
    """
    tid: Annotated[
        str, Field(..., min_length=8, max_length=40, description="Client-generated transaction id used for tracing")
    ]
    orig_text: Annotated[
        str, Field(..., min_length=1, max_length=10000, description="Original roommate recruitment post text")
    ]

# ---------- Response ----------

class SurveyReports(BaseModel):
    # 필요 필드만 우선 정의하고, 나머지는 Optional로 둠
    dorm: Optional[int] = None
    birth: Optional[str] = None
    studentId: Optional[str] = None
    college: Optional[int] = 0
    mbti: Optional[str] = ""
    smoke: Optional[int] = None
    drink: Optional[str] = ""
    sdEtc: Optional[str] = ""
    wakeUp: Optional[str] = ""
    lightOff: Optional[str] = ""
    bedTime: Optional[str] = ""
    sleepHabit: Optional[int] = 0
    clean: Optional[int] = 1
    bug: Optional[int] = 0
    eatIn: Optional[int] = 0
    noise: Optional[int] = 0
    share: Optional[int] = 0
    home: Optional[int] = 0
    selectTag: Optional[List[str]] = None
    notes: Optional[str] = None

    @field_validator(
        "dorm", "college", "smoke", "sleepHabit", "clean", "bug",
        "eatIn", "noise", "share", "home", mode="before"
    )
    @classmethod
    def _coerce_to_int(cls, v):
        if v is None:
            return None
        if isinstance(v, bool):
            return int(v)
        if isinstance(v, (int, float)):
            return int(v)
        if isinstance(v, str):
            s = v.strip()
            if s == "" or s.lower() == "null":
                return None
            m = re.search(r"-?\d+", s)
            if m:
                return int(m.group())
        raise TypeError("Expected a number-compatible value")
    
    class Config:
        extra = "forbid"
        schema_extra = {
            "example": {
                "college": 0,
                "clean": 1,
                "noise": 0,
                "selectTag": ["조용한", "깔끔한", "규칙적인"],
                "notes": "조용히 공부, 주말 산책, 요리 선호"
            }
        }
