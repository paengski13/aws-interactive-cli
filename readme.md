## AWS Interactive CLI

An interactive python script built on top of aws-vault https://github.com/99designs/aws-vault. Allows you to execute a complex AWS commands by chaining one or more other AWS CLI dependency

## Usage
 - python src/ssm:start-session.py
```
Select a profile: fi-staging
List of available EC2 Instances: 
[1] - i-abcinstance1
[2] - i-efginstance2
Enter the value: 1
Starting session with SessionId: 1213979597540752000-03ae7ab849677cfae
```

 - python ecs:run-task.py
```
Select a profile: fi-poc

List of available ECS Clusters:
[1] - ContainerStack-ProjectClusterABC-abc123
[2] - ContainerStack-ProjectClusterEFG-efg456
Enter the value: 2

List of available ECS Task Definitions: 
[1] - ContainerStackProjectTaskDefinition731D7411:22
Enter the value: 1

List of available EC2 Cluster VPC: 
[1] - vpc-abc3a0bd35b4aaa (192.168.1.1/18)
[2] - vpc-abc3a0bd35b4bbb (192.168.1.1/16)
[3] - vpc-abc3a0bd35b4ccc (192.168.1.1/10)
Enter the value: 1

List of available EC2 Subnets:
[1] - subnet-abc3a0bd35b411111 (192.168.1.1/18)
[2] - subnet-abc3a0bd35b422222 (192.168.1.2/16)
[3] - subnet-abc3a0bd35b433333 (192.168.1.3/18)
Enter the value: 2

Enter the script you want to execute e.g. php artisan migrate: php artisan cache:clear
```

## Requirements
 * Tested on Python 3.5 and up
 * working aws-vault