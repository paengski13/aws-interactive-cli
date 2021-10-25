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

# Actual task
ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ecs', 'execute-command',
                '--region=ap-southeast-2',
                '--cluster={}'.format(ecs_cluster),
                '--task={}'.format(ecs_task),
                '--command="/bin/bash"',
                '--interactive', '--output=json', '--no-cli-pager']
subprocess.run(ecs_run_task)
