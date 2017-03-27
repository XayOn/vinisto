# pylint: disable=invalid-name, missing-docstring


def test_get_knowledge_engine_returns_engine(config, test_feature):
    from unittest.mock import patch
    from vinisto import get_knowledge_engine
    from pyknow import KnowledgeEngine

    with patch("vinisto.config", return_value=config):
        assert isinstance(
            get_knowledge_engine(test_feature, {"rules": [],
                                                "final_rules": []}),
            KnowledgeEngine)


def test_get_rules_returns_two_ands(config, test_feature):
    """
    Given the two features in test_feature we receive two ands
    """
    from unittest.mock import patch
    from vinisto import get_rules
    from pyknow import AND, Rule

    with patch("vinisto.config", return_value=config):
        rules = list(get_rules(test_feature, {"rules": [], "final_rules": []}))
        assert isinstance(rules[0], Rule)
        assert all(isinstance(a, AND) for a in rules[0])
        assert isinstance(rules[1], Rule)
        assert all(isinstance(a, AND) for a in rules[1])
