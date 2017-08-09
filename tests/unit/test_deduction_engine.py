def test_vinisto_accepts_connector_and_arguments():
    """Vinisto call must have a connector argument for specifying
    wich input/ouptut connector to use for both feature files
    and sensor data i/o.
    """
    import vinisto
    from unittest.mock import MagicMock
    assert vinisto.DeductionEngine(connector=MagicMock())

def test_vinisto_accepts_connector_argument():
    """Check that execution flow is correct

        - Parse features and load them onto a KE
        - Run the KE with the input data
        - Get KE output and call output() method with it.
    """
    import vinisto
    from pyknow import KnowledgeEngine
    from vinisto.deduction import SensorFact
    from unittest.mock import MagicMock
    # pylint: disable=missing-docstring, no-self-use

    fake_connector = MagicMock()
    fake_connector.features.side_effect = ['Sample Feature'],
    fake_connector.input.side_effect = [{"fake_input": 3}],

    parser = vinisto.DeductionEngine(connector=fake_connector)

    assert isinstance(parser.get_engine([]), KnowledgeEngine)

    parser.get_engine = MagicMock()
    parser.get_engine().results.side_effect = {"fake_input": 4},
    parser.run()

    parser.get_engine().declare.assert_called_with(
        SensorFact(**{"fake_input": 3}))
    parser.get_engine().run.assert_any_call()
    fake_connector.output.assert_called_with(parser.get_engine().results)
