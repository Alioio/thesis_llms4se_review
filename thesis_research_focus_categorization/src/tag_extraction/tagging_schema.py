from enum import Enum
from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field

class ResearchFocusCategory(Enum):
    """
    This class defines the categories for classifying research papers based on their focus and intended goals in the context of utilizing LLMs for Software Engineering tasks.
    """
    DIRECT_SOLUTION = 'direct_solution', 'Papers proposing a solution Y for Problem(s) X related to SE-Task(s) X. Artifacts may include new frameworks, concepts, or modifications of existing solutions.'
    DATASET_BENCHMARK = 'dataset_benchmark', 'Papers creating new Datasets or Benchmarks Y\' related to Problem(s) X of SE-Task(s) X for assessing the quality of Solutions Y.'
    LLM_PROPERTY_INVESTIGATION = 'llm_property_investigation', 'Papers investigating properties of LLMs related to Problem(s) X of SE-Task(s) X, providing new findings about specific LLM attributes.'
    EXISTING_SOLUTION_EVALUATION = 'existing_solution_evaluation', 'Papers investigating existing Solution (e.g. ChatGPT or Codex) Y\'s quality for Problem(s) X related to SE-Task(s) X, evaluating performance of existing LLM-based solutions.'
    OTHER = 'other', 'Papers that do not clearly fit into the above categories.'

    def __new__(cls, value, description):
        member = object.__new__(cls)
        member._value_ = value
        member.description = description
        return member

class ResearchFocus(BaseModel):
    category: List[Optional[ResearchFocusCategory]] = Field(
        default=None,
        description="Classification of the paper's research focus and intended goal"
    )
    category_reasoning: List[Optional[str]] = Field(
        default=None,
        description="Reasoning for the classification. If classified as OTHER, provide a matching new category suggestion here."
    )

class ArticleMetadata(BaseModel):
    """Extract information from paper's title and abstract"""
    research_focus: Optional[ResearchFocus] = Field(
        default=None,
        description="Classification of the paper's research focus and intended goal"
    )
    