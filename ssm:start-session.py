import subprocess
import json

aws_iam_profile = input("Select a profile: ")
print("")

# List of EC2 Instances
aws_cli_ec2_instances = \
    subprocess.check_output('aws-vault exec {} -- \
    aws ec2 describe-instances \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
ec2_instances_data = json.loads(aws_cli_ec2_instances.decode("utf-8"))
print("List of available EC2 Instances: ")
for reservations in ec2_instances_data.get('Reservations'):
    for key in reservations.get('Instances'):
        print(" - {}".format(key.get('InstanceId')))
ecs_instance = input("Enter the value: ")
print("")

# Actual task
ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'start-session',
                '--target={}'.format(ecs_instance),
                '--output=json', '--no-cli-pager']
subprocess.run(ecs_run_task)
