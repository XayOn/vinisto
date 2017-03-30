Feature: Heating stuff

    Scenario: If there is cold, turn the heat on
        Given I have a sensor temperature_room
          And I have a sensor temperature_living
          And I have a sensor thermostat
         When sensor temperature_room has value 15
          And sensor temperature_living has a value > 15
         Then set thermostat to 1

    Scenario: If there is too hot, turn heat off
        Given I have a sensor temperature_room
          And I have a sensor temperature_living
          And I have a sensor thermostat
         When sensor temperature_room has value 20
          And sensor temperature_living has a value > 20
         Then set thermostat to 0
