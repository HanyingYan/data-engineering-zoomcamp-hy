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



