# ai-service/features/feature_vector_builder.py

from features.skill_features import (
    extract_skill_features
)

from features.experience_features import (
    extract_experience_features
)

from features.behavior_features import (
    extract_behavior_features
)

from features.trust_features import (
    extract_trust_features
)

from features.profile_features import (
    extract_profile_features
)

from features.boost_features import (
    calculate_boost_score
)

from features.penalty_features import (
    calculate_penalty_score
)

from features.career_features import (
    extract_career_features
)

def build_feature_vector(candidate: dict) -> dict:

    feature_vector = {}

    feature_vector.update(
        extract_skill_features(candidate)
    )

    feature_vector.update(
        extract_experience_features(candidate)
    )

    feature_vector.update(
        extract_behavior_features(candidate)
    )

    feature_vector.update(
        extract_trust_features(candidate)
    )

    feature_vector.update(
        extract_profile_features(candidate)
    )

    feature_vector["boost_score"] = (
        calculate_boost_score(candidate)
    )

    feature_vector["penalty_score"] = (
        calculate_penalty_score(candidate)
    )

    feature_vector.update(

    extract_career_features(
        candidate
    )

)

    return feature_vector