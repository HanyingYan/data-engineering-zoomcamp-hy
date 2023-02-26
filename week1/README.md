# Week 1 Overview

[1.1.1 - Introduction to Google Cloud Platform](#111---introduction-to-google-cloud-platform)<br />
[1.2.1 - Introduction to Docker](#121---introduction-to-docker)<br />


## [1.1.1 - Introduction to Google Cloud Platform](https://www.youtube.com/watch?v=18jIzE41fJ4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=3)
### **What is GCP**
* Cloud computing services offered by google<br />
* Includes a range of hosted service for compute, storage and application development that run on google hardware<br />
* Same hardware on which google runs its service<br />
![gcp_services.png](./img/gcp_services.png)


## [1.2.1 - Introduction to Docker](https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4)
### **1. What is Docker**
**Docker** is a tool that use OS-level vitualization to delivers software in packages called **containers**, which are isolated from each other, and contain all code and dependencies required to run some service or task (e.g., data pipeline). <br/>
This containerization software that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

A **data pipeline** is a service that receives data as input and outputs more data.

A **Docker image** is a *snapshot* of a container that we can define to run our software (or data pipelines). By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can also run our containers there.

Note: Docker containers are **stateless**: any changes done inside a container will **NOT** be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner, but you will have to store data elsewhere if you need to do so; a common way to do so is with **volumes**.

### **2. Why we need to care about docker**
* We can run local experiments and local tests, such as integration tests.
* It is easy to reproduce data pipelines in different environments.
* It is useful to perform integration tests under CI/CD.
* We can deploy pipelines in the cloud (e.g., AWS Batch and Kubernetes jobs).
* We can use Spark (analytics engine for large-scale data processing)
* We can process data using Serverless services (e.g., AWS Lambda, Google functions).

### **3. Running Docker**<br />
First we download [docker desktop](https://www.docker.com/products/docker-desktop/), then we test to see if the downloaded docker works.
```
docker run hello-world
```
Now run image ubuntu in interactive mode(i) in terminal(t) so that we can type something for docker to react. And bash is parameter indicating we want to execute a bash on this image.
```
docker run -it ubuntu bash
```
We can also run a different one on image python with tag version 3.9 with entrypoint bash so that we can install some packages as needed.
```
docker run -it --entrypoint=bash python:3.9
```
### **4. Some fancy codes**<br />
First, let's create a dummy ```pipeline.py``` script to receives an argument and prints a sentence.
```
import sys

import pandas as pd

print(sys.argv)

# argument 0 is the name os the file
# argumment 1 contains the actual first argument we care about
day = sys.argv[1]

print(f'job finished successfully for day = {day}')
```

We can run the scripts with ```python pipeline.py <some_number>``` and it should print 2 lines:
```
['pipeline.py', '<some_number>']
job finished successfully for day = <some_number>
```

Now let's containerize it by creating a Docker image using the ```Dockerfile``` file:
```
# base Docker image that we will build on
FROM python:3.9

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT [ "python", "pipeline.py"]
```

Then we build an image using the ```Dockerfile``` at the current directory, using the image name ```test``` with tag ```pandas``` (tag will default to ```latest``` if not specified).
```
docker build -t test:pandas .
```
Now if we run the container with an argument, we will get 'job finished successfully for day = 2021-01-15'
```
docker run -it test:pandas 2021-01-15
```
