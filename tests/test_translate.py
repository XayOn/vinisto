import pytest


@pytest.mark.manual
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

    from vinisto.language import Phrase

    assert Phrase("open the window") == Phrase("abre la ventana", "es")


def test_samelang_comparision():
    """
        If the language is the same in both phrases, don't try
        to translate any
    """
    from vinisto.language import Phrase

    p1a = Phrase("open the window", "en_US")
    p1b = Phrase("open the window", "en_US")

    assert p1b == p1a

    p2a = Phrase("abre la ventana", "es_ES")
    p2b = Phrase("abre la ventana", "es_ES")

    assert p2a == p2b
