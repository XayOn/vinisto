Vinisto - Your human-like intelligent home
-------------------------------------------


Vinisto is a domotic engine made with readability
(as in easy-to-configure) and flexibility in mind.

.. image:: http://68.media.tumblr.com/bc7f86261bd1d671577d51f82b2d0f6d/tumblr_njdb9pgaXv1sa11jco2_500.gif

This means, that you can specify rules for your home domotic system as

::

   Feature: If there is cold, turn the heater on
   Scenario:
     Given I have a sensor temperature_living
       And I have a button heater that reacts on "get" to "http://heater/?state={value}"
         And the sensor temperature_living has a value < 15
        Then turn on heater

   Feature: If there is too hot, turn the heater off
   Scenario:
       Given I have a sensor temperature_living
       And I have a button heater that reacts on "get" to "http://heater/?state={value}"
         And the sensor temperature_living has a value > 20
        Then turn off heater


Technical part
--------------

Vinisto uses all the power of an expert system combined with the syntax
of a great language for defining software features (gherkins).

That is acomplished with the following:

- A library that converts a series of features in input for a knowledge engine
  (http://github.com/buguroo/pyknow)
- A REST API with simple database models
- External data providers to receive and emit data to receiver/emitter
- An almost-real-time web interface

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
