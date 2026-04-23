from datetime import timedelta

from powermem.intelligence.ebbinghaus_algorithm import EbbinghausAlgorithm
from powermem.intelligence.plugin import EbbinghausIntelligencePlugin
from powermem.utils.utils import get_current_datetime


def _plugin_config() -> dict:
    return {
        "enabled": True,
        "decay_rate": 0.1,
        "working_threshold": 0.3,
        "short_term_threshold": 0.6,
        "long_term_threshold": 0.8,
    }


def test_should_forget_uses_last_reviewed_before_created_at():
    algo = EbbinghausAlgorithm(_plugin_config())
    now = get_current_datetime()
    stale_created_at = (now - timedelta(days=30)).isoformat()
    recent_review = (now - timedelta(minutes=5)).isoformat()

    memory = {
        "created_at": stale_created_at,
        "updated_at": recent_review,
        "intelligence": {"last_reviewed": recent_review},
        "access_count": 0,
    }

    assert algo.should_forget(memory) is False


def test_on_get_promotes_recently_accessed_memory_before_forgetting():
    plugin = EbbinghausIntelligencePlugin(_plugin_config())
    now = get_current_datetime()

    memory = {
        "content": "Remember this launch checklist",
        "created_at": (now - timedelta(days=30)).isoformat(),
        "updated_at": (now - timedelta(days=2)).isoformat(),
        "memory_type": "working",
        "importance_score": 0.1,
        "access_count": 2,
        "intelligence": {
            "last_reviewed": (now - timedelta(minutes=5)).isoformat(),
            "review_count": 2,
            "access_count": 2,
        },
        "metadata": {},
    }

    updates, delete_flag = plugin.on_get(memory)

    assert delete_flag is False
    assert updates is not None
    assert updates["memory_type"] == "short_term"
    assert updates["access_count"] == 3
    assert updates["intelligence"]["review_count"] == 3
