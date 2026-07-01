# ai-service/explainability/csv_reasoning_builder.py

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Tier Boundaries
# ---------------------------------------------------------------------------

TIER_BOUNDARIES: List[Tuple[float, str]] = [
    (0.90, "Elite Match"),
    (0.80, "Strong Match"),
    (0.70, "Good Match"),
    (0.60, "Moderate Match"),
    (0.50, "Partial Match"),
    (0.00, "Weak Match"),
]

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

SIMILARITY_HIGH:   float = 0.65
SIMILARITY_MEDIUM: float = 0.50
EXPERIENCE_HIGH:   float = 0.75
EXPERIENCE_MEDIUM: float = 0.50
SKILL_HIGH:        float = 0.75
SKILL_MEDIUM:      float = 0.50
BEHAVIOR_HIGH:     float = 0.70
TRUST_HIGH:        float = 0.70
PROFILE_HIGH:      float = 0.70
BOOST_SIGNIFICANT: float = 0.05
PENALTY_NOTABLE:   float = 0.05
RECRUITER_HIGH:    float = 0.75
RECRUITER_MEDIUM:  float = 0.50


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def classify_tier(final_score: float) -> str:
    for threshold, label in TIER_BOUNDARIES:
        if final_score >= threshold:
            return label
    return "Weak Match"


def _safe_float(value, default: float = 0.0) -> float:
    try:
        result = float(value)
        return default if result != result else result
    except (TypeError, ValueError):
        return default


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_bool(value, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return bool(value)
    return default


def _safe_str(value, default: str = "") -> str:
    if isinstance(value, str):
        return value.strip()
    return default


def _days_since(date_str) -> int:
    if not date_str:
        return 9999
    try:
        parsed = datetime.strptime(str(date_str), "%Y-%m-%d")
        return (datetime.now() - parsed).days
    except Exception:
        return 9999


# ---------------------------------------------------------------------------
# Signal Extractors
# ---------------------------------------------------------------------------

def _extract_profile_signals(candidate: dict) -> Dict:
    profile = candidate.get("profile", {}) or {}

    current_title = _safe_str(
        profile.get("current_title", ""),
        default="Professional",
    ) or "Professional"

    return {
        "current_title":   current_title,
        "years":           _safe_float(
            profile.get("years_of_experience", 0)
        ),
        "location":        _safe_str(profile.get("location", "")),
        "headline":        _safe_str(profile.get("headline", "")),
        "skill_count":     len([
            s for s in candidate.get("skills", [])
            if isinstance(s, dict)
        ]),
        "career_count":    len([
            r for r in candidate.get("career_history", [])
            if isinstance(r, dict)
        ]),
        "education_count": len([
            e for e in candidate.get("education", [])
            if isinstance(e, dict)
        ]),
        "cert_count":      len([
            c for c in candidate.get("certifications", [])
            if isinstance(c, dict)
        ]),
    }


def _extract_redrob_signals(candidate: dict) -> Dict:
    signals = candidate.get("redrob_signals", {}) or {}

    offer_rate = _safe_float(signals.get("offer_acceptance_rate", -1))
    if offer_rate < 0:
        offer_rate = 0.5

    assessment_scores = signals.get("skill_assessment_scores", {}) or {}
    ai_scores = [
        float(v) for v in assessment_scores.values()
        if isinstance(v, (int, float)) and v >= 0
    ]
    avg_assessment = sum(ai_scores) / len(ai_scores) if ai_scores else 0.0

    github_score = _safe_float(
        signals.get("github_activity_score", -1)
    )

    days_active = _days_since(signals.get("last_active_date"))

    return {
        "profile_completeness_score":  _safe_float(
            signals.get("profile_completeness_score", 0)
        ),
        "recruiter_response_rate":     _safe_float(
            signals.get("recruiter_response_rate", 0)
        ),
        "verified_email":              _safe_bool(
            signals.get("verified_email", False)
        ),
        "verified_phone":              _safe_bool(
            signals.get("verified_phone", False)
        ),
        "linkedin_connected":          _safe_bool(
            signals.get("linkedin_connected", False)
        ),
        "application_success_rate":    _safe_float(
            signals.get("offer_acceptance_rate", 0)
        ),
        "profile_views_last_30_days":  _safe_int(
            signals.get("profile_views_received_30d", 0)
        ),
        "open_to_work":                _safe_bool(
            signals.get("open_to_work_flag", False)
        ),
        "interview_completion_rate":   _safe_float(
            signals.get("interview_completion_rate", 0)
        ),
        "endorsement_count":           _safe_int(
            signals.get("endorsements_received", 0)
        ),
        "github_activity_score":       max(0.0, github_score),
        "github_linked":               github_score >= 0,
        "avg_assessment_score":        avg_assessment,
        "assessment_count":            len(ai_scores),
        "saved_by_recruiters_30d":     _safe_int(
            signals.get("saved_by_recruiters_30d", 0)
        ),
        "search_appearance_30d":       _safe_int(
            signals.get("search_appearance_30d", 0)
        ),
        "willing_to_relocate":         _safe_bool(
            signals.get("willing_to_relocate", False)
        ),
        "notice_period_days":          _safe_int(
            signals.get("notice_period_days", 90)
        ),
        "days_since_active":           days_active,
        "connection_count":            _safe_int(
            signals.get("connection_count", 0)
        ),
        "preferred_work_mode":         _safe_str(
            signals.get("preferred_work_mode", "")
        ),
    }


# ---------------------------------------------------------------------------
# Reason Builders
# ---------------------------------------------------------------------------

def _build_core_reasons(profile: Dict) -> List[str]:
    reasons: List[str] = []

    reasons.append(profile["current_title"])

    years = profile["years"]
    if years >= 1:
        reasons.append(f"{years:.1f} yrs experience")
    else:
        reasons.append("entry level")

    skill_count = profile["skill_count"]
    if skill_count >= 10:
        reasons.append(f"{skill_count} skills (extensive)")
    elif skill_count >= 5:
        reasons.append(f"{skill_count} skills")
    elif skill_count >= 2:
        reasons.append(f"{skill_count} skills listed")

    career_count = profile["career_count"]
    if career_count >= 5:
        reasons.append(f"{career_count} roles (deep career)")
    elif career_count >= 3:
        reasons.append(f"{career_count} roles")

    if profile["cert_count"] >= 2:
        reasons.append(f"{profile['cert_count']} certifications")

    return reasons


def _build_score_driven_reasons(
    breakdown: Dict[str, float],
) -> List[str]:
    reasons: List[str] = []

    similarity = breakdown.get("similarity_score", 0.0)
    experience = breakdown.get("experience_score", 0.0)
    skill      = breakdown.get("skill_score", 0.0)
    behavior   = breakdown.get("behavior_score", 0.0)
    trust      = breakdown.get("trust_score", 0.0)
    profile_s  = breakdown.get("profile_score", 0.0)
    boost      = breakdown.get("boost_score", 0.0)
    penalty    = breakdown.get("penalty_score", 0.0)

    if similarity >= SIMILARITY_HIGH:
        reasons.append("high semantic match")
    elif similarity >= SIMILARITY_MEDIUM:
        reasons.append("good semantic match")

    if experience >= EXPERIENCE_HIGH:
        reasons.append("strong experience signal")
    elif experience >= EXPERIENCE_MEDIUM:
        reasons.append("solid experience")

    if skill >= SKILL_HIGH:
        reasons.append("strong skill alignment")
    elif skill >= SKILL_MEDIUM:
        reasons.append("relevant skills")

    if behavior >= BEHAVIOR_HIGH:
        reasons.append("strong behavioral signal")

    if trust >= TRUST_HIGH:
        reasons.append("high trust score")

    if profile_s >= PROFILE_HIGH:
        reasons.append("complete profile")

    if boost >= BOOST_SIGNIFICANT:
        reasons.append(f"boosted +{boost:.2f}")

    if penalty >= PENALTY_NOTABLE:
        reasons.append(f"penalized -{penalty:.2f}")

    return reasons


def _build_behavioral_reasons(signals: Dict) -> List[str]:
    reasons: List[str] = []

    # GitHub activity — strongest technical signal
    github = signals["github_activity_score"]
    if signals["github_linked"]:
        if github >= 70:
            reasons.append(f"GitHub score {github:.0f}/100")
        elif github >= 40:
            reasons.append(f"GitHub active ({github:.0f})")

    # Skill assessments
    avg_assessment = signals["avg_assessment_score"]
    count = signals["assessment_count"]
    if count > 0 and avg_assessment >= 70:
        reasons.append(
            f"assessment avg {avg_assessment:.0f}/100"
        )
    elif count > 0 and avg_assessment >= 50:
        reasons.append(f"{count} skill assessments")

    # Recruiter demand
    saved = signals["saved_by_recruiters_30d"]
    if saved >= 10:
        reasons.append(f"saved by {saved} recruiters")
    elif saved >= 5:
        reasons.append("high recruiter saves")

    # Recruiter response rate
    rr = signals["recruiter_response_rate"]
    if rr >= RECRUITER_HIGH:
        reasons.append("high recruiter engagement")
    elif rr >= RECRUITER_MEDIUM:
        reasons.append("good recruiter engagement")

    # Verification
    if signals["verified_email"] and signals["verified_phone"]:
        reasons.append("fully verified")
    elif signals["verified_email"]:
        reasons.append("email verified")
    elif signals["verified_phone"]:
        reasons.append("phone verified")

    if signals["linkedin_connected"]:
        reasons.append("LinkedIn connected")

    # Activity recency
    days = signals["days_since_active"]
    if days <= 7:
        reasons.append("active this week")
    elif days <= 30:
        reasons.append("recently active")

    # Availability
    if signals["open_to_work"]:
        reasons.append("open to work")

    notice = signals["notice_period_days"]
    if notice <= 15:
        reasons.append(f"{notice}d notice period")
    elif notice <= 30:
        reasons.append("short notice period")

    # Interview reliability
    icr = signals["interview_completion_rate"]
    if icr >= 0.90:
        reasons.append("high interview reliability")
    elif icr >= 0.70:
        reasons.append("strong interview completion")

    # Endorsements
    endorsements = signals["endorsement_count"]
    if endorsements >= 50:
        reasons.append(f"{endorsements} endorsements")
    elif endorsements >= 20:
        reasons.append(f"{endorsements} endorsements")

    return reasons


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def build_csv_reasoning(
    candidate: dict,
    breakdown: Optional[Dict[str, float]] = None,
    final_score: Optional[float] = None,
) -> str:
    """
    Generate signal-rich explanation for HireSense_AI.csv.
    Uses all 23 redrob_signals schema fields.
    """
    reasons: List[str] = []

    try:
        profile = _extract_profile_signals(candidate)
        signals = _extract_redrob_signals(candidate)
    except Exception as e:
        logger.error("Signal extraction failed: %s", e)
        return "Signal extraction failed"

    # Tier
    score = None
    if final_score is not None:
        score = _safe_float(final_score)
    elif breakdown and "final_score" in breakdown:
        score = _safe_float(breakdown["final_score"])

    if score is not None:
        reasons.append(classify_tier(score))

    # Core
    try:
        reasons.extend(_build_core_reasons(profile))
    except Exception as e:
        logger.warning("Core reasons failed: %s", e)

    # Score-driven
    if breakdown and isinstance(breakdown, dict):
        try:
            reasons.extend(_build_score_driven_reasons(breakdown))
        except Exception as e:
            logger.warning("Score reasons failed: %s", e)

    # Behavioral
    try:
        reasons.extend(_build_behavioral_reasons(signals))
    except Exception as e:
        logger.warning("Behavioral reasons failed: %s", e)

    # Deduplicate
    seen   = set()
    deduped: List[str] = []
    for reason in reasons:
        key = reason.lower().strip()
        if key not in seen:
            seen.add(key)
            deduped.append(reason)

    deduped = deduped[:12]

    if not deduped:
        return f"{profile.get('current_title', 'Candidate')} | insufficient signals"

    return ", ".join(deduped)


def build_csv_reasoning_batch(
    ranked_candidates: List[Dict],
) -> List[str]:
    results: List[str] = []
    for item in ranked_candidates:
        if not isinstance(item, dict):
            results.append("Invalid candidate record")
            continue
        try:
            reasoning = build_csv_reasoning(
                candidate=item.get("candidate", {}),
                breakdown=item.get("breakdown", None),
                final_score=item.get("final_score", None),
            )
        except Exception as e:
            logger.error("Batch reasoning failed: %s", e)
            reasoning = "Reasoning generation failed"
        results.append(reasoning)
    return results