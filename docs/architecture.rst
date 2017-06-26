Vinisto Architecture
---------------------


Vinisto is a microservice-oriented architecture with an operating base
around pyknow and rethinkdb.

That means:

- Rethinkdb handles changes notifications to other backends (such as
  mqtt)
- A specialized rethinkdb client listens on changes, upon detecting one
  requests all sensor status and runs the pyknow engine, wich has been
  previously configured by reading all feature requests in the features
  directory. The engine will make needed changes to sensor status on the
  database, wich may re-trigger an engine run if needed.
