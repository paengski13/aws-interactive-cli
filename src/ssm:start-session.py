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
    remote_port_number = input("What is the Remote Port Number (default 3306): ") or 3306
    local_port_number = input("What is the Local Port Number (default 3306): ") or 3306
    port_forwarding_name = '--document-name=AWS-StartPortForwardingSession'
    port_forwarding_parameters = '--parameters={{"portNumber":["{remote_port_number}"], "localPortNumber":["{local_port_number}"]}}'.format(remote_port_number=remote_port_number, local_port_number=local_port_number)

    # Actual task
    ssm_start_session = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'start-session',
                    '--target={}'.format(ecs_instance),
                    '{}'.format(port_forwarding_name),
                    '{}'.format(port_forwarding_parameters),
                    '--output=json', '--no-cli-pager']
    print("Executing: {}".format(" ".join(ssm_start_session)))
    subprocess.run(ssm_start_session)
else:
    # Actual task
    ssm_start_session = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'start-session',
                    '--target={}'.format(ecs_instance),
                    '--output=json', '--no-cli-pager']
    print("Executing: {}".format(" ".join(ssm_start_session)))
    subprocess.run(ssm_start_session)
