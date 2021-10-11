import subprocess
import json

aws_iam_profile = input("Select a profile: ")
print("")

# List of ECS Clusters
aws_cli_ecs_clusters = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-clusters \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ecs_clusters_data = json.loads(aws_cli_ecs_clusters.decode("utf-8"))
print("List of available ECS Clusters: ")
for key in ecs_clusters_data.get('clusterArns'):
    cluster = key.split("/")
    print(" - {}".format(cluster[1]))
ecs_cluster = input("Enter the value: ")
print("")

# List of ECS Task Definitions
aws_cli_ecs_task_definitions = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-task-definitions \
    --family-prefix ContainerStackDBMigrateTaskDefinition731D7433 \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ecs_task_definitions_data = json.loads(aws_cli_ecs_task_definitions.decode("utf-8"))
print("List of available ECS Task Definitions: ")
for key in ecs_task_definitions_data.get('taskDefinitionArns'):
    task_definition = key.split("/")
    print(" - {}".format(task_definition[1]))
ecs_task_definition = input("Enter the value: ")
print("")

# List of EC2 Subnets
aws_cli_ec2_subnet = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ec2 describe-subnets \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ec2_subnets_data = json.loads(aws_cli_ec2_subnet.decode("utf-8"))
print("List of available EC2 Subnets: ")
for key in ec2_subnets_data.get('Subnets'):
    subnet = key.get('SubnetArn').split("/")
    print(" - {}".format(subnet[1]))
ec2_subnet = input("Enter the value: ")
print("")

# # Your script you want to run
ecs_custom_script = input("Enter the script you want to execute e.g. php artisan migrate: ")
print("")

# Actual task
ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ecs', 'run-task',
                '--cluster={}'.format(ecs_cluster),
                '--task-definition={}'.format(ecs_task_definition),
                '--launch-type=FARGATE',
                '--network-configuration=awsvpcConfiguration={{subnets=["{}"]}}'.format(ec2_subnet),
                '--overrides={{"containerOverrides":[{{"name":"DBMigrateContainerDefinition","command":["{}"]}}]}}'.format(ecs_custom_script),
                '--output=json', '--no-cli-pager']
subprocess.Popen(ecs_run_task)
