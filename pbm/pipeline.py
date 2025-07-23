# Unify row handling + model predictions + final tag.
from dataclasses import dataclass, field
from typing import Optional

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
