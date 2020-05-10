# Ganjine - DataBase Library
As Albert Einstein said, "No problem can be solved from the same level of consciousness that created it." So in big data era, we can't solve data persistent problem with old concept like RDBMS! A lot of people say "We want a scalable relational database", But they don't exactly know what they want and we almost can say they don't want that at all! that's only because they were trying to treat "Big Data" the same way they treated data with an RDBMS: "by conflating data and views and relying on incremental algorithms".

Ganjine build on this concept: "No one can go back in time to change the truthfulness of a piece of data"

Ganjine is not standalone application instead it is highly customizable embedded library to make multi model database application by acquire stream data model in three layer architecture or even use in one layer architecture! It doesn't know anything about data structure and work like a key/value data store engine with support transaction, secondary index and subscribe (notifications about a record or index)!

Like other SabzCity projects this project will also develope in automatic manner not admin rule!! In this case not just automate by increase or decrease amount of data but also automate if data store cluster need more or less computing power to handle requests!

Ganjine need PersiaOS as standalone OS or transition version for storage engine and networks! So it can't run and throw panic if it can't connect to PersiaOS! We rule this because exiting storage engines even newest one have some fundamental problem like they build in top of exiting FileSystems as defaults or don't respect cluster size of storage devices that need more logic handle by processors!!

If you check any databases you can feel that all of them want to do all thing about data by itself and by this choice it is so hard to [scale out](https://en.wikipedia.org/wiki/Scalability#Horizontal_or_Scale_Out) data layer of a platform! So we decide some rules to take many logic part form database app except store and [retrieve](https://en.wikipedia.org/wiki/Information_retrieval) data and handle in logic layer of platform. So Ganjine can scale with your app scalability architecture!

Ganjine can use for any purpose like Multi Model DataStore, Data Mining, Machine Learning & AI (Artificial intelligence)

## Architecture
- Ganjine has fully distributed architecture not decentralized one!!
- Architect with minimum layer and logic to gain max performance!
- Ganjine doesn't use coordinator(cassandra, ...) or lease(cockroachdb, ...) architecture! These types of architectures use unneeded computing and network capacity! Ganjine SDK in business logic layer app of platform indicate exact node to read or write records!!
- Unlike other distributed DB, Ganjine doesn't use follower(cockroachdb, yugabyte, ...) or slave() architecture everywhere! Choose a leader from a cluster replication drop efficency that can get from connect business logic layer app to closest data layer app. Almost always first class data centers use for data stores have very stabile physical connection to other same class DC other than ISP servers. So each node in each cluster is master||leader for given ranges primary index!
- Just in transaction find and write service, closest node to business logic layer app get read||write and  coordinated with master secondary index range and do request! if master not response, by type of error situation, all or at least 2/3 related range nodes agreeing to choose new master node. This decide is intelligence choose by many factors like daily get read or write request for that range not a random choose!!
- In normal write request, when write to disk finished and record async send to replicated nodes, business logic layer get response that write record have been successfully done!
- See simple architecture [Diagram here](https://app.diagrams.net?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1#R7V1tc5s4EP41%2FtiMkJDAHxMn7b2kc5lrZ67tN8XINlcMPsBJ3F9%2FIqDYCNkYA0J22860ZhGyePTsrnb14hGaLF8%2BxHS1%2BBh5LBhB4L2M0O0IQpe4%2FN9MsMkFGIJcMI99LxftCD75P1gutIR07XssKWS5KI2iIPVXZeE0CkM2TUsyGsfRc7nYLAq8kmBF56wi%2BDSlQVX6j%2B%2Bli%2BK1oLOV%2F8b8%2BUJ8s0XG%2BZ0lFYWLN0kW1Iued0ToboQmcRSl%2Bafly4QFGXZlXN7vufvWsJiF6TEPfAfut9TB1np%2Bv%2FzD%2BXb98fEZv4NF9zzRYF28cdHadCMgiKN16LGsFmuEbp4Xfso%2Breg0u%2FvM%2B5zLFukyKG7PY%2Br5vEWTKIhiLgujkBe8mflBIEQjiO5I9pfLqy9RvNcTi1P2siMqXuoDi5YsjTe8iLiL8yc2ZeI8b3vLGdu5bLHTUw4onqMFQ%2BZvNW9B5B8KHJtg6pw%2FpuMSpg6CClBRFVQL2X2BSpqACupBldDzKHNnUy5P0jj6znbukKnLHmfd4GqDEq7QwRVcLQIUuApWd48rvghczQN2fAm4YlKC1a7aVoS0oioq3kGRedxhF5dRnC6ieRTS4G4rvSnjvC1zH0WrAt1%2FWZpuitEHXadRGXv24qdfssevuLrkl1%2BL2rLPty%2B7FxtxEfIX3n0qu%2F4qaswuts%2B9XokHk5TG6XU2duGCaUCTxJ8K8Xs%2FEI3a271JtI6n7JDO5%2BV4fXOWHiiHiwozhA%2ByJWYBTf2n8pBJ1ffFow%2BRz9v8xrJxWXktKLEnb2jxkESgt1a04JQ1LKec4zl1JDVOpp4GTgE9nIJkWFLBjs1%2FB8ZcQgSBqjV%2FQ2nXmpPejHnXIBkx9jDASaJfTlLNiBmgCFAVI25uHQDamUARiNbaQNvVYwPtoR2rfWmOtTmddgiuyRMfT8OxHhqSE2nIu4NudoqtsgLJ%2Fu%2FBWAoCsZQQq2mXVJ5%2FyFvQ7bhgWNu8qxBbO11jm60mxD1NkwDAgM1UmgSAdXsz0aMRuganCOrRCNuShnwFEvs0Qi4vUib7yiP7YPmeNGhYr1LSIOdIDRIlfwol0pQ1sLAmJQKSEtk1SiSVt5zDSmTZ%2BFD5fpTI6jrtu5dYDQIp8wLU8bAD2C4CKdCLqfEwcz1bZWpc%2BIjIwWmoWlMjBqbG%2BGsiMVMmXP5GFUtTm5SS6%2BnIYhFStijwsMGCB4v3ZH%2FcYTXrJMVyNCgWw5YNgDKkhKBthkIkHozx4XKG4lTFqqmmqwBTGrYj0sixl4v3o1dIeN2zTqkSsYxAIIec6khA73QuGjin2iCXpTnq6DWnKhaeGJPMck4M3TtT8IFzqqcMSTXkjwwhoabEvpzp7Cv0JW7ZDteFstg5GPr25PJgxy6vCweGJQdGYNWBaQ1l0UWs84JSgtKAdV5iaHJOBrnhXFTvC5KKkbE5cYmlKUEvJwRgTcJdbhfUkXBHA2fBThv69sFwRV69dUx%2BPPd1rZzSNF0rT4LVcV9ulx7ud73svAsniKQ0xOB5cjENWEKJBGmmMisaluAi%2F62zHS85Tu%2BSHKhrXiSM4iUNtgX4p3n2%2Fy1N6YSjxeJEVMobmdebl6j0CAcyLcNOA38eZrr9WhEXZHD7UxpcFzeWvuflhosl%2Fg%2F6%2BFpV1p8FjXm9%2BGaEb7O6uK1KcrPVVY%2BS8nDRda1Kj7qKDpU1s7sOvYg0EoT1sNpaYW0Uqpi5M8gyDVPUo%2B358nCpJseStna4bjVCFXuuSoGU21c%2F2uZ5WoRNI3s1ir%2BP5nysCsE93XCWcbhY%2FPTqKtUE7ZGVAX1kwQOXpH6k%2FIp7qcDbV3XRVeP6rlIOivrrqyOGjsmCrrKPKWcv%2BxFl9d2sWOzzFmTIbeUPW2FDV0s81yHKmXp0jW30%2BkS09SBZLvX1Tzfdgo1zF9XNudkAU6VAueF%2FjIXN98NpsPZY9UaSRnG2jZzHZuHc5x4YTqqFPsc0TOj0lfrZ7vCQP8FvTq6urs7emWD7COVTdXN%2FEckR%2B9ovXvlsKR1PFMlSoOgV3FuvHLEp9uJ7hdiG9QpWRe9n1SuZXKQjFediNA8cjeuiI%2BJxs7uog14Z0JrB%2BeavDzNnBv78PfA%2Bf%2F2W%2Fv1l%2Fs6UHEkFQQXO%2B31EGVRHeHItE2pKWBvlSI6OA1uBJM3SOOKMHx0JVyVGqpzH2VEPisVq5nCvnxxEO5SwhNLg5DNlJUE7uydOaTKHfP1MNbVDyZZQGpx8jc7WMpV8RLTaHPI1OgdOk9e1JZQGJ58pZzq1glU%2B00kxjkaWo%2BDe2OkJVgWMGheYiM%2FDH1axfy%2FVvt1XOW7SipDadSjqaKZQmiNXWrdYdtKOKwOvfzZnGf55sCWPvtsuUmq8tgiUB802cHeZVy0vHSIqlW%2B9tugghueb1FHk3TqNdWzFpLTmHM%2FA%2BxRPWt3bzNjs22bYaNVvN0bFOtaodLLysalRsYBkJIrpjH1GRcpXSsX7sSlvh02f01rdi%2BdrPhupna9Y4muRb9t7cIVM2HL5npzghcxstPJ7rgT88G7vHEfZjQbZ8rZ7i4%2BSHVX%2Fj4mDKBnGvsCqfTmgREOFZNbAO6BO2x%2FSLIK%2FLLoMEpNZ0iwaLvZE7t3v4ZBD5XtyR7DeHenOg0puGav2PGpNg4pg%2BZd3GFTdkS51b0cWMixZTtsf2yxjd1l0GSS4hk459YOLmce9O2Gl4EYq35N36HrdRQfeAdoScIO7h2a%2Ff2TsNJl0BhFW%2FAaS7pVRZ3gcYensl1272vHkh0ceCVZMfvAYHU6n3ZpSqDhGzaCBNpZObcGWhskMNHDisT01fy5mDuLkibQbCAMNTrvZTxzqcdpY2liIseKAO70rSq0KKMb7Fl3LMBwHgMmkqsGUArCTAu5Gg3UpcDu2VFXIdGuvaxWGkWTpKQPAL7e%2FX5vb6%2B2PAKO7%2FwE%3D)

### CRUD
There is no update data, just set, get and delete in storage engine layer. any Secondary hash index belong to the time series record can be used as version control of that record, So each record in each time(version) have unique hash as RecordID. With this rule in every layer we can cache a record by its RecordID and it is guaranty that always be same data!

### Transaction
Due to transaction has many different scenario in each situation in distributed computing, Developer can send multi request in one connection but failed process must handle in logic layer.

## Secondary Index
Many number of secondary index can implement, But some consideration exist due to Ganjine is distributed database! Simplest secondary index like primary one is hash index that must implement without any question! It is base of transaction feature!

## Considerations
Considerations are about choose between available solutions. we discuss here about logic behind each decision!

### Replication Strategy
If more than one replication zone exist that we strongly suggest have three replication, Replicate a record can do 
- In business logic app! But in this layer we lost performance due app must connect to all replicated nodes in all zones! Due to first class data-centers that use for data-stores usually have stable connection rather than ISP data-centers!
- In each data layer nodes to replicate node to nodes!

We implement first choose in Ganjine!

### Partition or sharding selection
Select right shard node to send get or set request can implement in three way:
- Client side! Client SDK select related node to ID range!
- Proxy assisted! A third party app select related node to ID range!
- Server side partitioning! Any DB get request and select related node to ID range!

We implement first choose in Ganjine!

### Add new node
When exiting nodes reach capacity and need new node on each replication, we can choose between
- Split data range from node with capacity problem and copy all record with desire range to new node. Due to this we have 2 node with more capacity in both two new nodes!
- Split data range from node with capacity problem and Add node to node list, but hold range responser node with old node! in this situation on each get and set record on out of real range of node, two more network roundtrip needed!

We implement first choose in Ganjine!

### Secondary Index Records
We have two decision for these type of records:
- When making cluster, make max number of record for secondary index that take a lot of space!
- In node splitting, Make two empty secondary index record and read entirely exiting record and transfer each index to proper new record!

We implement second choose in Ganjine!

### RecordID
RecordID can be one of below situation that have some drawbacks.
- real 128bit universal unique ID with random algorithm
    - Add new node to some ranges force database engine move some record to new node!
- make by 64bit as time in second format plus 64bit hash of record data!
    - All write go to just one node even in petabyte platforms with billion users!

We implement both choose in Ganjine and developer can choose it!

### Limiting transaction number per index
Due to network latency and transaction architecture that let just one action at a time, If every transaction just get 100ms so in each minute 600, each hour 36,000 and in each day just 864,000 transaction can be done on each specific record like user financial ballance! To beat this limitation devs must change thinking way to solve problems e.g. just make transaction on decreasing operation of financial not increasing! and check ballance healthy in UI app or croon jobs and have a service that can use to recalculate user balance if some thing wrong exist!

## Not Goals
You can always do what you want to do in your app level but we don't support all needed in engine but some of them might be supported in Ganjine SDK!

### SQL - Structured Query Language
We don't support [SQL](https://en.wikipedia.org/wiki/SQL) due to it is a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) that means developers need to learn lot of new things for almost nothing that simple RPC give them! Also we believe SQL is not good language in term to respect DevOps culture! But for those developers that don't agree with us we plan to add some SQL parser & convertor to SDK for those developers!

### Schema Changing
It is so huge work when you don't write data structure with data unlike JSON! It is not our goals to handle in this engine to let you easy old data schema changing! We think to support this in SDK!

### B-Tree index
Due to have distributed high performance index engine and Ganjine don't know anything about data in a record, we decide to not support range query like notEquals(!=, \<>), BETWEEN, LARGER, ORDER, ... so don't support b-tree index! We suggest change data model and transfer range query to UI not here!
We believe language need search engines that understand languages not just simple equal bytes!!

### Table, Namespace, Sets, ...
We don't offer any splitting data to logical block as named! Developers can achieve this usage by make multi subdomain app for each desire usages e.g. db1.sabz.city, db2.sabz.city, ... or even have better name like big.db.sabz.city for big data like videos and archive.db.sabz.city for any old data not use daily anymore like dead people data for 100 year ago!

## Implementations
- [Go](https://github.com/SabzCity/libgo/Ganjine)

## Inspired of
- [Aerospike](https://www.aerospike.com/docs/architecture/index.html)
- [Cockroach](https://github.com/cockroachdb/cockroach)
- [Yugabyte] (https://yugabyte.com/)
- [TiKV](https://tikv.org/)
- [TiDB](https://pingcap.com/)
- [Arangodb](https://github.com/arangodb/arangodb)
- [Elassandra](https://github.com/strapdata/elassandra)
- [LevelDB](https://github.com/google/leveldb)
- [RocksDB](https://github.com/facebook/rocksdb)
- [Google Spanner](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf)
- [Google MillWheel](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41378.pdf)
- [Google Percolator](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36726.pdf)
- [Paxos Protocol](https://www.google.com/search?q=paxos+protocol)
- [Raft Consensus Algorithm](https://raft.github.io/)
- [Data stream management system](https://en.wikipedia.org/wiki/Data_stream_management_system)
- [Microsoft Tango](https://www.microsoft.com/en-us/research/publication/tango-distributed-data-structures-over-a-shared-log/)

### Articles
- http://nathanmarz.com/blog/how-to-beat-the-cap-theorem.html
- https://www.cockroachlabs.com/blog/vectorized-hash-joiner/

## Ganjine word meaning
["Ganjine"](https://en.wikipedia.org/wiki/Hoard) (Persian: گنجینه) is an archaeological term for a collection of valuable objects or artifacts, sometimes purposely buried in the ground, in which case it is sometimes also known as a cache.
