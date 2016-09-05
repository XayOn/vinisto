def test_intent_matches_phrase():
    """
        Check that:
            - We've got a class Phrase
            - We've got a class Intent
            - Our class Intent, initialized with a list of possible phrases
              matches a class Phrase

        In a future, I've got to make phrases comparable between them apart
        from standard comparision, implementing there the language
        ccomprehension part there
    """

    from vinisto.intent import Intent
    from vinisto.language import Phrase

    pra = Phrase("OK")
    yap = Phrase("Do it")

    intent = Intent(phrases=[pra])

    assert pra in intent
    assert yap not in intent
