# Unify row handling + model predictions + final tag.

import pandas as pd
import re

from dataclasses import dataclass, field
from typing import Optional

from .sanitize import sanitize_text
from .heuristics import heuristic_product, heuristic_issue, heuristic_action
from .llm_chain import build_pbm_chain

@dataclass
class CaseRecord:
    case_id: str
    subject: str
    description: str
    summary: str
    
    clean_summary: str = field(default="", init=False)
    
    product: Optional[str] = None
    issue_category: Optional[str] = None
    action_category: Optional[str] = None
    
    # free text resolution/comments we’ll auto-derive
    resolution_comments: Optional[str] = None
    
    pbm_tag: Optional[str] = None

#Row Processing Pipeline
def build_pbm_tag(product, issue, resolution, action):
    # fail-safe placeholders
    product = product or "NA"
    issue = issue or "NA"
    resolution = (resolution or "").strip() or "NA"
    action = action or "NA"
    return f"#PBM:{product}:{issue}:{resolution}:{action}"

def process_dataframe(df: pd.DataFrame, chain=None, use_llm=True) -> pd.DataFrame:
    if chain is None and use_llm:
        chain = build_pbm_chain()

    # Print LLM model info if using LLM
    if use_llm:
        llm_model_name = None
        try:
            # The chain is a RunnableSequence: steps = [prompt, llm, parser]
            llm = chain.steps[1]  # 0=prompt, 1=llm, 2=parser
            if hasattr(llm, 'model'):
                llm_model_name = getattr(llm, 'model', None)
            elif hasattr(llm, 'model_name'):
                llm_model_name = getattr(llm, 'model_name', None)
            else:
                llm_model_name = str(type(llm))
        except Exception as e:
            llm_model_name = f"Unknown (error: {e})"
        print(f"Using LLM model: {llm_model_name}")
    
    results = []
    for _, row in df.iterrows():
        rec = CaseRecord(
            case_id=str(row.get("Case ID", "")),
            subject=str(row.get("Subject", "")),
            description=str(row.get("Description", "")),
            summary=str(row.get("Case summary", "")),
        )
        
        rec.clean_summary = sanitize_text(rec.summary)
        
        # heuristics
        h_prod = heuristic_product(rec.clean_summary + " " + rec.subject + " " + rec.description)
        h_issue = heuristic_issue(rec.clean_summary)
        h_action = heuristic_action(h_issue)
        
        prod = h_prod
        issue = h_issue
        action = h_action
        resolution = None
        
        if use_llm:
            print(f"Calling LLM for case {rec.case_id}...")
            try:
                resp = chain.invoke({
                    "case_id": rec.case_id,
                    "subject": rec.subject,
                    "description": rec.description,
                    "summary": rec.clean_summary,
                })
                # resp is PBMClassification object
                prod = getattr(resp, "product", prod) or prod
                issue = getattr(resp, "issue_category", issue) or issue
                action = getattr(resp, "action_category", action) or action
                resolution = getattr(resp, "resolution_comments", resolution) or resolution
            except Exception as e:
                print(f"Call to LLM failed for case {rec.case_id}: {e}")
                resolution = resolution or "See case notes"
        
        # derive resolution if still missing: short trimmed summary
        if not resolution:
            resolution = derive_resolution_from_text(rec.description, rec.clean_summary)
        
        rec.product = prod
        rec.issue_category = issue
        rec.action_category = action
        rec.resolution_comments = resolution
        rec.pbm_tag = build_pbm_tag(prod, issue, resolution, action)
        
        results.append(rec.pbm_tag)
    
    df["PBM_Tag"] = results
    return df

def derive_resolution_from_text(description: str, summary: str, max_len=150):
    # crude heuristic: look for phrases like "resolved after", "fixed by", etc.
    text = description or summary
    text = sanitize_text(text)
    # attempt cause extraction
    m = re.search(r'(resolved|fixed|worked)\s+(after|by)\s+([^\.]+)', text, re.IGNORECASE)
    if m:
        return m.group(0)[:max_len].strip()
    return text[:max_len].strip()


