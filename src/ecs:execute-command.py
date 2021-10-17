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

# List of ECS services
aws_cli_ecs_services = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ecs list-services \
    --cluster {} \
    --output json --no-cli-pager'.format(aws_iam_profile, ecs_cluster), shell=True)
ecs_services_data = json.loads(aws_cli_ecs_services.decode("utf-8"))
print("List of available ECS Services: ")
for key in ecs_services_data.get('serviceArns'):
    service = key.split("/")
    print(" - {}".format(service[2]))
ecs_service = input("Enter the value: ")
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
for key in ecs_tasks_data.get('taskArns'):
    task = key.split("/")
    print(" - {}".format(task[2]))
ecs_task = input("Enter the value: ")
print("")

# Actual task
ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ecs', 'execute-command',
                '--region=ap-southeast-2',
                '--cluster={}'.format(ecs_cluster),
                '--task={}'.format(ecs_task),
                '--command="/bin/bash"',
                '--interactive', '--output=json', '--no-cli-pager']
subprocess.run(ecs_run_task)
#
# # Actual task
# ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ecs', 'run-task',
#                 '--cluster={}'.format(ecs_cluster),
#                 '--task-definition={}'.format(ecs_task_definition),
#                 '--launch-type=FARGATE',
#                 '--network-configuration=awsvpcConfiguration={{subnets=["{}"]}}'.format(ec2_subnet),
#                 '--overrides={{"containerOverrides":[{{"name":"DBMigrateContainerDefinition","command":["{}"]}}]}}'.format(ecs_custom_script),
#                 '--output=json', '--no-cli-pager']
# subprocess.Popen(ecs_run_task)
