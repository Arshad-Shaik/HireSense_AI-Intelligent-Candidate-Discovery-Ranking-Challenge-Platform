# ai-service/features/trust_features.py


def extract_trust_features(candidate: dict) -> dict:
    """
    Extract trust and verification signals.

    Uses from redrob_signals schema:
        verified_email
        verified_phone
        linkedin_connected
        github_activity_score
        profile_completeness_score
        last_active_date
    """
    signals = candidate.get("redrob_signals", {}) or {}

    verified_email    = bool(signals.get("verified_email", False))
    verified_phone    = bool(signals.get("verified_phone", False))
    linkedin_connected = bool(signals.get("linkedin_connected", False))

    github_score = float(
        signals.get("github_activity_score", -1) or -1
    )
    # -1 means no GitHub linked
    github_linked = github_score >= 0

    profile_completeness = float(
        signals.get("profile_completeness_score", 0) or 0
    )

    return {
        "verified_email":             verified_email,
        "verified_phone":             verified_phone,
        "linkedin_connected":         linkedin_connected,
        "github_activity_score":      max(0.0, github_score),
        "github_linked":              github_linked,
        "profile_completeness_score": profile_completeness,
    }