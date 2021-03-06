Vinisto - Your human-like intelligent home
-------------------------------------------

.. image:: https://badge.fury.io/py/vinisto.svg
    :target: https://badge.fury.io/py/vinisto

.. image:: https://travis-ci.org/XayOn/vinisto.svg?branch=master
    :target: https://travis-ci.org/XayOn/vinisto

Vinisto is a Work-In-Progress domotic assistant.

Right now, its intentions are:

- Be human in each part of the process.
- Have access to as many resources as possible, as less intrusive as possible
- Be flexible.
- Be smart.
- Suggest, don't force.

.. image:: http://68.media.tumblr.com/bc7f86261bd1d671577d51f82b2d0f6d/tumblr_njdb9pgaXv1sa11jco2_500.gif

Base Ideas
----------

In order to acomplish that, we have an expert system with rules that are both
human readable and machine readable, like::

   Feature: If there is cold, turn the heater on
   Scenario:
        Given the sensor temperature_living has a value < 15
        And winter is coming
        Then turn on heater

   Feature: If there is too hot, turn the heater off
   Scenario:
        Given the sensor temperature_living has a value > 20
        And winter is coming
        Then turn off heater


Then, we need an external system that feeds the user with automated rules, guessed
by its own logic (that's a black box for now), that the user must accept or decline.

Technical part
--------------

Vinisto uses all the power of an expert system combined with the syntax
of a great language for defining software features (cucumber).

That is acomplished with the following:

- A library that converts a series of features to pyknow
  (http://github.com/buguroo/pyknow)
- An interface from-to rethinkdb for sensor data keeping and changes streaming
- Microservices (TODO) that read on those rethinkdb changes and propagate them
  to more standard IOT services (like MQTT) as well as web services.

Rethinkdb only marks updates if the value changed, wich helps with some
usual IoT problems.


TODO
----

We need connectors:

- Rethinkdb
- MQTT
- Disk

Future ideas
------------

This is actually a pure-domotic engine, that is, sensors/activators handling
based on a predefined ruleset.

It'd be nice to either:
- Integrate with other intent-hadndling systems
- Have an intent-handling system of our own with plugins, like mycroft.ai

Another ideas:
- Add a classification engine that finds out behavioural patterns and suggests them
  to the user.
