# ProvisionAWS
Program that provisions automatically on AWS

# Before running the program
Run the command from the project base folder:

<code>pip install -r aws/requirements.txt</code>

# Web Server
The web server resides in the **server** folder. It is only a static nodejs file that runs the server. The Dockerfile is the docker I built already and published to the docker hub.

[Docker Hub Link](https://hub.docker.com/repository/docker/amitbenami/server-details)

# Program
The program is written in python and uses the **boto3** AWS SDK package to interact with AWS.

The provision program provisions the web server upon AWS ECS cluster.

The whole system infrastructure includes the following:

* Creating a VPC, and subnets in all of the Availability Zones in the current region (High Availability) - **EC2**
* Creating a Security Group for incoming HTTP/HTTPS requests - **EC2**
* Creating **IAM** policy and role for logging to **Cloud Watch**
* Creating LB and Target Group to connect the LB to the ECS cluster (Over SSL) - **ELB**
* Creating the **ECS** cluster with the desired number of servers in **FARGATE** mode to autoprovision

\# Currently auto deletion still not supported

# Running the program
There are two ways to run the program:

<Code>python aws/main.py</Code>

In this case, the program by default will provision 1 web server

or

<Code>python aws/main.py --server N</Code>

In this case, N is the number of web servers you want to provision

You can run the following command for help:

<code>python aws/main.py -h</code>

# Sanity Checks
There are few checks:

* Load Balancer health checks - to determine whether a task is good to receive traffic
* Each component provisioned, is waited until created. Otherwise an exception will be thrown

# Logging
The cluster is provisioned with writing to AWS Cloud Watch. The log group name is: **awslogsWeb** (Can be changed in the **config.ini** file)

# Configuration
The **config.ini* file holds all of the configuration, and it is pretty straight forward

# Manual Deletion
These are the steps required to manually delete the provisions:

* Stop all cluster's tasks
* Delete the Cluster
* Delete the Load Balancer
* Delete the Cloud Watch log group
* Delete the Target Group
* Delete the VPC
* Delete the Role and Policy created
* Delete the SSL Server Certificate