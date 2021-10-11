## AWS Interactive CLI

An interactive python script built on top of aws-vault https://github.com/99designs/aws-vault. Allows you to execute a complex AWS commands by chaining one or more other AWS CLI dependency

## Usage
 - python ssm:start-session.py
```
Select a profile: fi-staging
List of available EC2 Instances: 
 - i-abcinstance1
 - i-efginstance2
Enter the value: i-abcinstance1
Starting session with SessionId: 1213979597540752000-03ae7ab849677cfae
```

 - python ecs:run-task.py
```
Select a profile: fi-poc

List of available ECS Clusters:
 - ContainerStack-ProjectClusterABC-abc123
 - ContainerStack-ProjectClusterEFG-efg456
Enter the value: ContainerStack-ProjectClusterEFG-efg456

List of available ECS Task Definitions: 
 - ContainerStackProjectTaskDefinition731D7411:22
Enter the value: ContainerStackProjectTaskDefinition731D7411:22

List of available EC2 Subnets:
- subnet-abc3a0bd35b411111
- subnet-abc3a0bd35b422222
- subnet-abc3a0bd35b433333
Enter the value: subnet-abc3a0bd35b422222e

Enter the script you want to execute e.g. php artisan migrate: php artisan cache:clear
```

## Requirements
 * Tested on Python 3.5 and up
 * working aws-vault