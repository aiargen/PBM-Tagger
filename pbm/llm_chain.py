#We’ll use an LLM to choose labels from your controlled vocab (guardrail: must pick from list; return JSON). Works with OpenAI, Gemini, Claude, etc.

#6.1 Output Schema
from typing import List, Optional
from pydantic import BaseModel, Field

#6.2 Prompt Template
from langchain.prompts import ChatPromptTemplate
from .vocab import PRODUCTS, ISSUE_CATEGORIES, ACTION_CATEGORIES

#6.3 Chain Builder
from langchain_openai import ChatOpenAI  # or langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser

#6.1
class PBMClassification(BaseModel):
    product: Optional[str] = Field(description="One of controlled Product names.")
    issue_category: Optional[str] = Field(description="One of controlled Issue categories.")
    action_category: Optional[str] = Field(description="One of controlled Action categories.")
    resolution_comments: Optional[str] = Field(description="Short 1-line cause/fix summary (<=150 chars).")

#6.2
PBM_PROMPT = ChatPromptTemplate.from_template("""
You are a support-case triage assistant. Classify the case into controlled tags used for internal closure PBM comments.

**Allowed values**

Product: {products}
Issue Category: {issues}
Action Category: {actions}

Rules:
- Choose the single best match from each list. If unclear, choose the most likely; if totally unknown, output null.
- Base decision primarily on Case Summary; subject/description provide context.
- Keep resolution_comments as a short cause/fix phrase (no URLs, no customer names, no envs).

Case:
CASE_ID: {case_id}
SUBJECT: {subject}
DESCRIPTION: {description}
SUMMARY: {summary}

Return JSON that matches the expected schema.
""")

#6.3
def build_pbm_chain(llm=None):
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # choose your model
    
    parser = PydanticOutputParser(pydantic_object=PBMClassification)
    prompt = PBM_PROMPT.partial(
        products=", ".join(PRODUCTS),
        issues=", ".join(ISSUE_CATEGORIES),
        actions=", ".join(ACTION_CATEGORIES),
    ) + parser.get_format_instructions()  # important!
    
    chain = prompt | llm | parser
    return chain


