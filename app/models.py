from dataclasses import dataclass

@dataclass
class Features:
    has_code: bool = False
    is_deep_dive: bool = False
    is_tutorial: bool = False

@dataclass
class Article:
    title: str
    link: str
    summary: str = ""
    why_it_matters: str = ""
    level: str = ""
    interest: str = ""
    features: Features = None

