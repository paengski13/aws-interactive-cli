import subprocess
import json

# Get list of available aws-vault profiles
aws_vault_profiles_data = subprocess.check_output('aws-vault list --profiles', shell=True)
aws_vault_profiles_data = aws_vault_profiles_data.decode("utf-8").split("\n")
print("List of available aws-vault profiles: ")
aws_vault_profiles = {}
count = 1
for value in aws_vault_profiles_data:
    if not value:
        continue
    aws_vault_profiles.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1

aws_iam_profile = aws_vault_profiles.get(int(input("Enter aws-vault profile: ")))
print("")

# List of ECS Clusters
aws_cli_ecs_clusters = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-clusters \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ecs_clusters_data = json.loads(aws_cli_ecs_clusters.decode("utf-8"))

print("List of available ECS Clusters: ")
ecs_clusters = {}
count = 1
for key in ecs_clusters_data.get('clusterArns'):
    value = key.split("/")[1]
    ecs_clusters.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1
ecs_cluster = ecs_clusters.get(int(input("Enter the value: ")))
print("")

# List of ECS Task Definitions
aws_cli_ecs_task_definitions = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-task-definitions \
    --family-prefix ContainerStackDBMigrateTaskDefinition731D7433 \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ecs_task_definitions_data = json.loads(aws_cli_ecs_task_definitions.decode("utf-8"))

print("List of available ECS Task Definitions: ")
ecs_task_definitions = {}
count = 1
for key in ecs_task_definitions_data.get('taskDefinitionArns'):
    value = key.split("/")[1]
    ecs_task_definitions.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1
ecs_task_definition = ecs_task_definitions.get(int(input("Enter the value: ")))
print("")

# List of EC2 Cluster VPC
aws_cli_ec2_vpc = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ec2 describe-vpcs \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ec2_vpcs_data = json.loads(aws_cli_ec2_vpc.decode("utf-8"))

print("List of available EC2 Cluster VPC: ")
ec2_vpcs = {}
count = 1
for key in ec2_vpcs_data.get('Vpcs'):
    value = key.get('VpcId')
    ec2_vpcs.update({count: value})
    print("[{}] - {} ({})".format(count, value, key.get('CidrBlock')))
    count += 1
ec2_vpc = ec2_vpcs.get(int(input("Enter the value: ")))
print("")

# List of EC2 Subnets
aws_cli_ec2_subnet = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ec2 describe-subnets \
    --filters "Name=vpc-id,Values={}" \
    --output json --no-cli-pager'.format(aws_iam_profile, ec2_vpc), shell=True)
ec2_subnets_data = json.loads(aws_cli_ec2_subnet.decode("utf-8"))

print("List of available EC2 Subnets: ")
ec2_subnets = {}
count = 1
for key in ec2_subnets_data.get('Subnets'):
    value = key.get('SubnetArn').split("/")[1]
    ec2_subnets.update({count: value})
    print("[{}] - {} ({})".format(count, value, key.get('CidrBlock')))
    count += 1
ec2_subnet = ec2_subnets.get(int(input("Enter the value: ")))
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
print("Executing: {}".format(" ".join(ecs_run_task)))
subprocess.Popen(ecs_run_task)
