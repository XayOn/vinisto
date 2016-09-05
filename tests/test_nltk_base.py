def test_phrase_nltk():
    from vinisto.intent import Intent
    from vinisto.language import Phrase

    pra = Phrase("Butler, open the windows")
    assert len(pra.phrase) == 5
