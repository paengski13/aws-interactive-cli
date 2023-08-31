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

# List of ECS services
aws_cli_ecs_services = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-services \
    --cluster {} \
    --output json --no-cli-pager'.format(aws_iam_profile, ecs_cluster), shell=True)
ecs_services_data = json.loads(aws_cli_ecs_services.decode("utf-8"))

print("List of available ECS Services: ")
ecs_services = {}
count = 1
for key in ecs_services_data.get('serviceArns'):
    value = key.split("/")[2]
    ecs_services.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1
ecs_service = ecs_services.get(int(input("Enter the value: ")))
print("")

# List of ECS tasks
aws_cli_ecs_tasks = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-tasks \
    --cluster {} \
    --service-name {} \
    --output json --no-cli-pager'.format(aws_iam_profile, ecs_cluster, ecs_service), shell=True)
ecs_tasks_data = json.loads(aws_cli_ecs_tasks.decode("utf-8"))

print("List of available ECS Tasks: ")
ecs_tasks = {}
count = 1
for key in ecs_tasks_data.get('taskArns'):
    value = key.split("/")[2]
    ecs_tasks.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1
ecs_task = ecs_tasks.get(int(input("Enter the value: ")))
print("")

# List of ECS task containers
aws_cli_ecs_task_container = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs describe-tasks \
    --cluster {} \
    --task {} \
    --output json --no-cli-pager'.format(aws_iam_profile, ecs_cluster, ecs_task), shell=True)

ecs_task_containers_data = json.loads(aws_cli_ecs_task_container.decode("utf-8"))

print("List of available ECS Task Containers: ")
ecs_task_container = {}
count = 1
for key in ecs_task_containers_data.get('tasks'):
    containers = key.get('containers')
    for container in containers:
        value = container.get('name')
        ecs_task_container.update({count: value})
        print("[{}] - {}".format(count, value))
        count += 1
ecs_task_container = ecs_task_container.get(int(input("Enter the value: ")))
print("")

# Actual task
ecs_execute_command = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ecs', 'execute-command',
                '--region=ap-southeast-2',
                '--cluster={}'.format(ecs_cluster),
                '--task={}'.format(ecs_task),
                '--command="/bin/bash"',
                '--container={}'.format(ecs_task_container),
                '--interactive', '--output=json', '--no-cli-pager']
print("Executing: {}".format(" ".join(ecs_execute_command)))
subprocess.run(ecs_execute_command)
