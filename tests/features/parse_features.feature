Feature: Vinisto can parse feature files and produce rules
   Scenario: Direct vinisto execution against a feature file and a sensor input data file produces a new sensor input data file in stdout
   Given I have a feature file /tmp/feature.feature saying
    """
    Feature: Main room
        Scenario: It's cold, turn heating on
              When sensor temperature has a value of 10
              Then turn on heating
    """
    And I have an input file /tmp/sensors.json with '{"temperature": 10, "heating": 0}'
    When I start vinisto with "--connector=json_filesystem --feature_files /tmp/feature.feature --output /tmp/output.feature"
    Then I can read '{"temperature": 10, "heating": 1}' on /tmp/output.feature
