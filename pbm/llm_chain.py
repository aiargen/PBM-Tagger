# llm_chain.py
from typing import Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser
from langchain_openai import ChatOpenAI
from .vocab import PRODUCTS, ISSUE_CATEGORIES, ACTION_CATEGORIES


# 6.1 Output Schema
class PBMClassification(BaseModel):
    product: Optional[str] = Field(description="One of controlled Product names.")
    issue_category: Optional[str] = Field(description="One of controlled Issue categories.")
    action_category: Optional[str] = Field(description="One of controlled Action categories.")
    resolution_comments: Optional[str] = Field(description="Short 1-line cause/fix summary (<=150 chars).")


# 6.2 Prompt Template
PBM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a support-case triage assistant. Classify the case into controlled tags used for internal closure PBM comments."),
    ("human", """
**Allowed values**

Product: {products}
Issue Category: {issues}
Action Category: {actions}

Rules:
- Choose the single best match from each list. If unclear, choose the most likely; if totally unknown, return null.
- Base decision primarily on Case Summary; subject/description provide context.
- Keep resolution_comments as a short cause/fix phrase (no URLs, no customer names, no envs).

Case:
CASE_ID: {case_id}
SUBJECT: {subject}
DESCRIPTION: {description}
SUMMARY: {summary}

Return a JSON object in this format:
{format_instructions}
""")
])


# 6.3 Chain Builder
def build_pbm_chain(llm=None):
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Output parser with auto-fix for formatting issues
    base_parser = PydanticOutputParser(pydantic_object=PBMClassification)
    parser = OutputFixingParser.from_llm(parser=base_parser, llm=llm)

    # Fill in controlled vocab and format instructions
    format_instructions = parser.get_format_instructions()
    prompt = PBM_PROMPT.partial(
        products=", ".join(PRODUCTS),
        issues=", ".join(ISSUE_CATEGORIES),
        actions=", ".join(ACTION_CATEGORIES),
        format_instructions=format_instructions
    )

    # Build the chain
    return prompt | llm | parser
