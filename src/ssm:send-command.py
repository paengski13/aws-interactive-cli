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

# List of RDS Instances
aws_cli_rds_instances = \
    subprocess.check_output('aws-vault exec {} -- \
    aws rds describe-db-instances \
    --output json --no-cli-pager'.format(aws_iam_profile), shell=True)
rds_instances_data = json.loads(aws_cli_rds_instances.decode("utf-8"))

print("List of available RDS Instances: ")
rds_instances = {}
count = 1
for db_instances in rds_instances_data.get('DBInstances'):
    value = db_instances.get('Endpoint').get('Address')
    rds_instances.update({count: value})
    print("[{}] - {}".format(count, value))
    count += 1
rds_instance = rds_instances.get(int(input("Enter the value: ")))
print("")

port_number = input("What is the Port Number (default 3306): ") or 3306

parameter = 'commands=["sudo socat TCP-LISTEN:{},reuseaddr,fork TCP4:{}:{} &"]'.format(port_number, rds_instance, port_number)

# Actual task
ssm_run_task = ['aws-vault', 'exec', aws_iam_profile, '--', 'aws', 'ssm', 'send-command',
                '--document-name=AWS-RunShellScript',
                '--instance-ids={}'.format(ecs_instance),
                '--parameters={}'.format(parameter),
                '--output=json', '--no-cli-pager']
print("Executing: {}".format(" ".join(ssm_run_task)))
subprocess.run(ssm_run_task)
