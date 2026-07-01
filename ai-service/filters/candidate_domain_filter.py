# ai-service/filters/candidate_domain_filter.py

import re
import math
import logging
from collections import Counter
from typing import Dict, List, Set, Tuple


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

MIN_JD_OVERLAP_RATIO:       float = 0.04
MIN_DOMAIN_SCORE:           float = 5
MIN_UNIQUE_OVERLAP_TOKENS:  int   = 3
MIN_SKILL_COUNT:            int   = 2
MIN_CAREER_ENTRIES:         int   = 1


# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

TITLE_WEIGHT:     int = 5
HEADLINE_WEIGHT:  int = 4
SKILL_WEIGHT:     int = 4
CAREER_WEIGHT:    int = 3
SUMMARY_WEIGHT:   int = 2
EDUCATION_WEIGHT: int = 1

CAREER_RECENCY_DECAY: float = 0.80

SKILL_PROFICIENCY_MULTIPLIERS: Dict[str, float] = {
    "expert":       2.0,
    "advanced":     1.75,
    "senior":       1.75,
    "proficient":   1.5,
    "intermediate": 1.25,
    "familiar":     1.0,
    "beginner":     0.75,
    "learning":     0.75,
}

DEFAULT_PROFICIENCY_MULTIPLIER: float = 1.25


# ---------------------------------------------------------------------------
# Text Processing
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    return text.lower().strip()


def tokenize_unigrams(text: str) -> Set[str]:
    if not text:
        return set()
    return {
        token
        for token in re.findall(
            r"[a-zA-Z][a-zA-Z0-9\-\+\.#]*",
            text.lower()
        )
        if len(token) >= 2
    }


def tokenize_bigrams(text: str) -> Set[str]:
    if not text:
        return set()
    tokens = re.findall(
        r"[a-zA-Z][a-zA-Z0-9\-]*",
        text.lower()
    )
    tokens = [t for t in tokens if len(t) >= 2]
    bigrams = set()
    for i in range(len(tokens) - 1):
        bigrams.add(f"{tokens[i]}_{tokens[i+1]}")
    return bigrams


def tokenize_all(text: str) -> Set[str]:
    return tokenize_unigrams(text) | tokenize_bigrams(text)


def safe_get_str(
    obj: dict,
    key: str,
    default: str = "",
) -> str:
    if not isinstance(obj, dict):
        return default
    value = obj.get(key, default)
    if not isinstance(value, str):
        return default
    return value


# ---------------------------------------------------------------------------
# Profile Signal Validation
# ---------------------------------------------------------------------------

def has_profile_signals(candidate: dict) -> bool:
    if not isinstance(candidate, dict):
        return False

    profile        = candidate.get("profile", {}) or {}
    skills         = candidate.get("skills", []) or []
    career_history = candidate.get("career_history", []) or []

    title    = safe_get_str(profile, "current_title").strip()
    headline = safe_get_str(profile, "headline").strip()
    summary  = safe_get_str(profile, "summary").strip()

    if not title:
        return False
    if not headline and not summary:
        return False

    valid_skills = [s for s in skills if isinstance(s, dict)]
    if len(valid_skills) < MIN_SKILL_COUNT:
        return False

    valid_career = [r for r in career_history if isinstance(r, dict)]
    if len(valid_career) < MIN_CAREER_ENTRIES:
        return False

    return True


# ---------------------------------------------------------------------------
# Vocabulary Builder
# ---------------------------------------------------------------------------

def get_skill_proficiency_multiplier(skill: dict) -> float:
    level = normalize_text(
        skill.get("proficiency", "")
        or skill.get("level", "")
    )
    for keyword, multiplier in SKILL_PROFICIENCY_MULTIPLIERS.items():
        if keyword in level:
            return multiplier

    skill_months = skill.get("duration_months", None)
    if isinstance(skill_months, (int, float)) and skill_months > 0:
        years = skill_months / 12.0
        if years >= 5:
            return 1.75
        elif years >= 3:
            return 1.5
        elif years >= 1:
            return 1.25

    return DEFAULT_PROFICIENCY_MULTIPLIER


def _parse_date_score(date_value) -> int:
    if not date_value:
        return 0
    if isinstance(date_value, int):
        return date_value
    if isinstance(date_value, str):
        match = re.search(r"\b(19|20)\d{2}\b", date_value)
        if match:
            return int(match.group())
    return 0


def _sort_career_by_recency(career_history: list) -> list:
    def recency_key(role: dict) -> Tuple:
        is_current = role.get("is_current", False)
        end_date   = role.get("end_date", None)
        start_date = role.get("start_date", None)
        if is_current or end_date is None or (
            isinstance(end_date, str)
            and end_date.lower() in (
                "present", "current", "now", ""
            )
        ):
            return (1, _parse_date_score(start_date))
        return (0, _parse_date_score(end_date))

    try:
        return sorted(
            career_history,
            key=recency_key,
            reverse=True,
        )
    except Exception:
        return career_history


def build_candidate_vocabulary(candidate: dict) -> Counter:
    """
    Build weighted term frequency Counter.
    Uses all profile fields with appropriate weights.
    Uses duration_months from skills schema for proficiency.
    Uses is_current from career schema for recency.
    """
    profile        = candidate.get("profile", {}) or {}
    skills         = candidate.get("skills", []) or []
    career_history = candidate.get("career_history", []) or []
    education      = candidate.get("education", []) or []
    certifications = candidate.get("certifications", []) or []

    title    = normalize_text(safe_get_str(profile, "current_title"))
    headline = normalize_text(safe_get_str(profile, "headline"))
    summary  = normalize_text(safe_get_str(profile, "summary"))
    industry = normalize_text(safe_get_str(profile, "current_industry"))

    weighted_terms: List[str] = []

    # Title
    for token in tokenize_all(title):
        weighted_terms.extend([token] * TITLE_WEIGHT)

    # Headline
    for token in tokenize_all(headline):
        weighted_terms.extend([token] * HEADLINE_WEIGHT)

    # Summary
    for token in tokenize_all(summary):
        weighted_terms.extend([token] * SUMMARY_WEIGHT)

    # Industry
    for token in tokenize_all(industry):
        weighted_terms.extend([token] * 1)

    # Skills with proficiency and duration_months multiplier
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        skill_name = normalize_text(safe_get_str(skill, "name"))
        if not skill_name:
            continue
        multiplier = get_skill_proficiency_multiplier(skill)
        # Also boost by endorsements
        endorsements = skill.get("endorsements", 0) or 0
        if endorsements >= 30:
            multiplier = min(multiplier * 1.2, 2.5)
        effective_weight = max(
            1,
            int(math.ceil(SKILL_WEIGHT * multiplier))
        )
        for token in tokenize_all(skill_name):
            weighted_terms.extend([token] * effective_weight)

    # Career with recency decay and description
    sorted_career = _sort_career_by_recency(career_history)
    for idx, role in enumerate(sorted_career):
        if not isinstance(role, dict):
            continue
        role_title = normalize_text(safe_get_str(role, "title"))
        role_desc  = normalize_text(
            safe_get_str(role, "description", "")
        )
        role_industry = normalize_text(
            safe_get_str(role, "industry", "")
        )
        if not role_title:
            continue
        decay_factor     = CAREER_RECENCY_DECAY ** idx
        effective_weight = max(
            1,
            int(math.ceil(CAREER_WEIGHT * decay_factor))
        )
        for token in tokenize_all(role_title):
            weighted_terms.extend([token] * effective_weight)
        for token in tokenize_all(role_desc):
            weighted_terms.extend(
                [token] * max(1, effective_weight - 1)
            )
        for token in tokenize_all(role_industry):
            weighted_terms.extend([token] * 1)

    # Education
    for edu in education:
        if not isinstance(edu, dict):
            continue
        field  = normalize_text(
            safe_get_str(edu, "field_of_study", "")
        )
        degree = normalize_text(
            safe_get_str(edu, "degree", "")
        )
        for token in tokenize_all(field):
            weighted_terms.extend([token] * EDUCATION_WEIGHT)
        for token in tokenize_all(degree):
            weighted_terms.extend([token] * EDUCATION_WEIGHT)

    # Certifications
    for cert in certifications:
        if not isinstance(cert, dict):
            continue
        cert_name = normalize_text(
            safe_get_str(cert, "name", "")
        )
        for token in tokenize_all(cert_name):
            weighted_terms.extend([token] * 2)

    return Counter(weighted_terms)


# ---------------------------------------------------------------------------
# Score Calculation
# ---------------------------------------------------------------------------

def calculate_domain_score(
    candidate: dict,
    job_description: str,
) -> float:
    jd_tokens = tokenize_all(normalize_text(job_description))
    if not jd_tokens:
        return 0.0

    candidate_terms = build_candidate_vocabulary(candidate)

    score = 0.0
    for token in jd_tokens:
        score += candidate_terms.get(token, 0)

    return score


def calculate_overlap_ratio(
    candidate: dict,
    job_description: str,
) -> Tuple[float, int]:
    profile        = candidate.get("profile", {}) or {}
    skills         = candidate.get("skills", []) or []
    career_history = candidate.get("career_history", []) or []
    education      = candidate.get("education", []) or []
    certifications = candidate.get("certifications", []) or []

    title    = safe_get_str(profile, "current_title")
    headline = safe_get_str(profile, "headline")
    summary  = safe_get_str(profile, "summary")
    industry = safe_get_str(profile, "current_industry")

    skill_text = " ".join(
        safe_get_str(s, "name")
        for s in skills
        if isinstance(s, dict)
    )
    career_text = " ".join(
        safe_get_str(r, "title")
        + " "
        + safe_get_str(r, "description", "")
        + " "
        + safe_get_str(r, "industry", "")
        for r in career_history
        if isinstance(r, dict)
    )
    education_text = " ".join(
        safe_get_str(e, "field_of_study", "")
        + " "
        + safe_get_str(e, "degree", "")
        for e in education
        if isinstance(e, dict)
    )
    cert_text = " ".join(
        safe_get_str(c, "name", "")
        for c in certifications
        if isinstance(c, dict)
    )

    candidate_text = " ".join([
        title, headline, summary, industry,
        skill_text, career_text,
        education_text, cert_text,
    ])

    candidate_tokens = tokenize_all(normalize_text(candidate_text))
    jd_tokens        = tokenize_all(normalize_text(job_description))

    if not jd_tokens:
        return 0.0, 0

    overlap = candidate_tokens & jd_tokens
    count   = len(overlap)
    ratio   = count / len(jd_tokens)

    return ratio, count


# ---------------------------------------------------------------------------
# Main Filter
# ---------------------------------------------------------------------------

def is_relevant_candidate(
    candidate: dict,
    job_description: str,
) -> bool:
    """
    Semantic domain filter.
    Thresholds calibrated to pass 100-200 AI/ML candidates
    from 30K retrieved while blocking non-IT profiles.
    No hardcoded blacklists. Fully JD-vocabulary driven.
    """
    try:
        if not has_profile_signals(candidate):
            return False

        overlap_ratio, unique_overlap_count = calculate_overlap_ratio(
            candidate, job_description
        )
        if overlap_ratio < MIN_JD_OVERLAP_RATIO:
            return False
        if unique_overlap_count < MIN_UNIQUE_OVERLAP_TOKENS:
            return False

        domain_score = calculate_domain_score(
            candidate, job_description
        )
        if domain_score < MIN_DOMAIN_SCORE:
            return False

        return True

    except Exception as e:
        logger.warning("Filter error: %s", e)
        return False


def explain_filter_decision(
    candidate: dict,
    job_description: str,
) -> Dict:
    profile_ok = has_profile_signals(candidate)
    overlap_ratio, unique_overlap_count = calculate_overlap_ratio(
        candidate, job_description
    )
    domain_score = calculate_domain_score(
        candidate, job_description
    )
    passed = is_relevant_candidate(candidate, job_description)

    return {
        "passed":                    passed,
        "has_profile_signals":       profile_ok,
        "overlap_ratio":             round(overlap_ratio, 4),
        "unique_overlap_count":      unique_overlap_count,
        "domain_score":              round(domain_score, 4),
        "thresholds": {
            "MIN_JD_OVERLAP_RATIO":      MIN_JD_OVERLAP_RATIO,
            "MIN_UNIQUE_OVERLAP_TOKENS": MIN_UNIQUE_OVERLAP_TOKENS,
            "MIN_DOMAIN_SCORE":          MIN_DOMAIN_SCORE,
        },
    }