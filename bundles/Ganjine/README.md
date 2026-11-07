# Ganjine
Ganjine bundle some modules to act as [database engine or storage engine](https://en.wikipedia.org/wiki/Database_engine) and [database management system (DBMS)](https://en.wikipedia.org/wiki/Database_management_system). The term "database engine" is frequently used interchangeably with "database server" or "database management system". A "database instance" refers to the processes and memory structures of the running database engine. Storage engine uses to create, read, update and delete (CRUD) data from a database. Most database management systems include their own application programming interface (API) that allows the user to interact with their underlying engine without going through the user interface of the DBMS.

## Functionality
The functionality provided can vary enormously. The core functionality is the storage, retrieval and update of data. The following functions and services a fully-fledged general purpose should provide:
- Data storage, retrieval and update
- User accessible catalog or data dictionary describing the metadata
- Support for transactions and concurrency
- Facilities for recovering the database should it become damaged
- Support for authorization of access and update of data
- Access support from remote locations
- Enforcing constraints to ensure data in the database abides by certain rules

## Commands
- memar:ganjine --ShardConsistency=strict
