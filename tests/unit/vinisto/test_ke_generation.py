# pylint: disable=invalid-name, missing-docstring


def test_get_knowledge_engine_returns_engine(config, test_feature):
    from vinisto.engine import VinistoEngine
    from pyknow import KnowledgeEngine

    assert isinstance(
        VinistoEngine(features_list=test_feature, base_context={
            "rules": [], "final_rules": []}),
        KnowledgeEngine)


def test_get_rules_returns_two_ands(config, test_feature):
    """
    Given the two features in test_feature we receive two ands
    """
    from vinisto.engine import VinistoEngine
    from pyknow import AND, Rule

    rules = list(VinistoEngine.get_rules(
        features_list=test_feature,
        base_context={"rules": [], "final_rules": []}))
    assert isinstance(rules[0], Rule)
    assert all(isinstance(a, AND) for a in rules[0])
    assert isinstance(rules[1], Rule)
    assert all(isinstance(a, AND) for a in rules[1])
