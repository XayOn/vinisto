Vinisto - Your human-like intelligent home
-------------------------------------------


Vinisto is a rules engine applied to home automation in a more-human form.
This means it's a domotic engine that:

- Has human-readable rules
- Is able to interact with MQTT devices


Right now, only our own mqtt device syntax with a generic mqtt branch to listen on is supported,
but in the not-so-far future we might support other device types (PRs and tickets welcome)


This means that given a series of files in the form::

   # language: en

    Feature: Heating stuff

   Scenario: If there is cold, turn the heat on
        When the sensor temperature_room has value 15
         And the sensor temperature_living has a value > 15
        Then set the sensor thermostat value to 1

   Scenario: If there is too hot, turn heat off
        When the sensor temperature_room has value 20
         And the sensor temperature_living has a value > 20
        Then set the sensor thermostat value to 0

And creates a knowledge engine with that rules, listening on MQTT changes,
that act upon them.

How to contribute
-----------------

Right now, the most useful contribution would probably be a ticket with information on a device
you want to support:

- Device model
- MQTT json info (if it's not json, the specific format)

