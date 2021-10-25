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
ecs_instances = {}
count = 1
for reservations in ec2_instances_data.get('Reservations'):
    for key in reservations.get('Instances'):
        value = key.get('InstanceId')
        ecs_instances.update({count: value})
        print("[{}] - {}".format(count, value))
        count += 1
ecs_instance = ecs_instances.get(int(input("Enter the value: ")))
print("")

is_port_forwarding = input("Do you want to Port Forward (default Yes): ") or 'Y'
if is_port_forwarding == 'Y' or is_port_forwarding == 'y':
    port_number = input("What is the Port Number (default 3306): ") or 3306
    port_forwarding_name = '--document-name=AWS-StartPortForwardingSession'
    port_forwarding_parameters = '--parameters={{"portNumber":["{port_number}"], "localPortNumber":["{port_number}"]}}'.format(port_number=port_number)

    # Actual task
    ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'start-session',
                    '--target={}'.format(ecs_instance),
                    '{}'.format(port_forwarding_name),
                    '{}'.format(port_forwarding_parameters),
                    '--output=json', '--no-cli-pager']
    subprocess.run(ecs_run_task)
else:
    # Actual task
    ecs_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'start-session',
                    '--target={}'.format(ecs_instance),
                    '--output=json', '--no-cli-pager']
    subprocess.run(ecs_run_task)
