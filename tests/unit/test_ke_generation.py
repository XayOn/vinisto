# pylint: disable=invalid-name, missing-docstring


def test_get_knowledge_engine_returns_engine():
    from vinisto import get_knowledge_engine
    from pyknow import KnowledgeEngine

    assert isinstance(get_knowledge_engine("../rules/test_rule.feature"),
                      KnowledgeEngine)


def test_get_rules_returns_two_ands():
    """
    Given the two features in test_rule we receive two ands
    """
    from vinisto import get_rules
    from pyknow import AND, Rule
    import os

    rules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    rules = list(get_rules("{}/rules/test_rule.feature".format(rules_dir)))
    print(rules)
    assert isinstance(rules[0], Rule)
    assert all(isinstance(a, AND) for a in rules[0])
    assert isinstance(rules[1], Rule)
    assert all(isinstance(a, AND) for a in rules[1])
