## AWS Interactive CLI

An interactive python script built on top of aws-vault https://github.com/99designs/aws-vault. Allows you to execute a complex AWS commands by chaining one or more other AWS CLI dependency

## Usage
 - python3 src/ecs:execute-command.py
```
List of available aws-vault profiles:
[1] - development
[2] - staging
[3] - production
Enter aws-vault profile: 2

List of available ECS Clusters: 
[1] - Cluster1
[2] - Cluster2
Enter the value: 1

List of available ECS Services: 
[1] - Service1
[2] - Service2
Enter the value: 1

List of available ECS Tasks: 
[1] - Task1
[2] - Task2
Enter the value: 2

List of available ECS Task Containers: 
[1] - Container1
[2] - Container2
Enter the value: 1

Starting session with SessionId: ecs-execute-command-0e2309a55b9e18e30

```

## Requirements
 * Tested on Python 3.8 and up
 * working aws-vault
