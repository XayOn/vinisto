Vinisto - Your human-like intelligent home
-------------------------------------------


Vinisto is a rules engine applied to home automation in a more-human form.
This means it's a domotic engine that:

- Has human-readable rules
- Is able to interact with any kind of devices
- Has a comprehensible web interface


That is acomplished with the following:

- A library that converts a series of features in input for a KE.
  Also, it has an emitter and a receiver.
- Models for features and sensors
- A rest receiver
- An API that acts both as a rest receiver and features manager
- External data providers to receive and emit data to receiver/emitter
- Web interface

This means that given a series of features in the form::

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

And creates a knowledge engine with that rules,
acts upon them and, when the rules matches, sends the requested signal.

Note that the core only speaks HTTP, meaning you'll have to implement your own
connectors from REST to whatever-you-need and configure the sensors to point
to those. At least until I have a few important ones running (PRs implementing
those are welcome)

How to contribute
-----------------

Right now, the most useful contribution would probably be a ticket with information on a device
you want to support:

- Device model
- MQTT json info (if it's not json, the specific format)

Running infrared module
-----------------------

::

        python -m aiohttp.web -H localhost -P 8080 vinisto.services.infrared:run
