"""
AWSTemplateFormatVersion: '2010-09-09'
Description: Launch an EC2 instance with HTTPD installed, using input parameters.

Parameters:
  KeyName:
    Description: cloudformation
    Type: String
    ConstraintDescription: cloudformation

  InstanceType:
    Description: EC2 instance type
    Type: String
    Default: t2.micro
    AllowedValues:
      - t2.micro
      - t2.small
      - t2.medium
      - t3.micro
      - t3.small
      - t3.medium
    ConstraintDescription: Must be a valid EC2 instance type.

  VPC:
    Description: VPC ID where the instance will be launched
    Type: AWS::EC2::VPC::Id
    Default: vpc-0e2e1cf283d9594b5
    ConstraintDescription: Must be an existing VPC ID.

  Subnet:
    Description: Subnet ID where the instance will be launched
    Type: AWS::EC2::Subnet::Id
    Default: subnet-01df82e19f1543237
    ConstraintDescription: Must be a valid Subnet ID within the specified VPC.

  AMIId:
    Description: AMI ID for the EC2 instance (e.g., Amazon Linux 2)
    Type: String
    Default: ami-019374baf467d6601
    ConstraintDescription: Must be a valid AMI ID.

Resources:
  EC2SecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties: 
      GroupDescription: Enable SSH and HTTP access
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      InstanceType: !Ref InstanceType
      KeyName: !Ref KeyName
      SubnetId: !Ref Subnet
      ImageId: !Ref AMIId
      SecurityGroupIds:
        - !Ref EC2SecurityGroup
      Tags:
        - Key: Name
          Value: HTTPD-Server
      UserData: 
        Fn::Base64: !Sub |
          #!/bin/bash
          yum update -y
          yum install -y httpd
          systemctl start httpd
          systemctl enable httpd
          echo "<h1>Welcome to HTTPD on EC2!</h1>" > /var/www/html/index.html

Outputs:
  InstanceId:
    Description: ID of the newly created EC2 instance
    Value: !Ref EC2Instance

  PublicIP:
    Description: Public IP address of the EC2 instance
    Value: !GetAtt EC2Instance.PublicIp

  WebURL:
    Description: URL to access the web server
    Value: !Sub "http://${EC2Instance.PublicIp}"
    
"""