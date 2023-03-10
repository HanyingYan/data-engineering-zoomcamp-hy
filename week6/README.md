# Week 6 Overview

[6.3 - What is kafka?](#63---what-is-kafka)<br />

## [6.3 - What is kafka?](https://www.youtube.com/watch?v=zPLZUDPi4AY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=60)

[**Apache Kafka**](https://kafka.apache.org/) is a **message broker** and **stream processor**. Kafka is used to handle **real-time data feeds**.
### **1. What is kafka?**
In a data project we can differentiate between consumers and producers:

* **Consumers** are those that consume the data: web pages, micro services, apps, etc.
* **Producers** are those who supply the data to consumers.
Connecting consumers to producers directly can lead to an amorphous and hard to maintain architecture in complex projects like the one in the first image. Kafka solves this issue by becoming an intermediary that all other components connect to.

Kafka works by allowing producers to send messages which are then pushed in real time by Kafka to consumers.

Kafka is hugely popular and most technology-related companies use it.

You can also check out this [animated comic](https://www.gentlydownthe.stream/) to learn more about Kafka.

### **2. Basic Kafka components**
**A. Message**<br />
The basic communication abstraction used by producers and consumers in order to share information in Kafka is called a **message**.

Messages have 3 main components:
* **Key**: used to identify the message and for additional Kafka stuff such as partitions (covered later).
* **Value**: the actual information that producers push and consumers are interested in.
* **Timestamp**: used for logging.

**B. Topic**<br />
A **topic** is an abstraction of a concept. Concepts can be anything that makes sense in the context of the project, such as "sales data", "new members", "clicks on banner", etc.

A producer pushes a message to a topic, which is then consumed by a consumer subscribed to that topic.

**C. Broker and Cluster**<br />
A **Kafka broker** is a machine (physical or virtualized) on which Kafka is running.

A **Kafka cluster** is a collection of brokers (nodes) working together.

**D. Logs**<br />
In Kafka, **logs** are data segments present on a storage disk. In other words, they're physical representations of data.

Logs store messages in an ordered fashion. Kafka assigns a sequence ID in order to each new message and then stores it in logs.

