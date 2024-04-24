# key pair
resource "tls_private_key" "sd-ec2-key" {
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "sd-ec2-keypair" {
  key_name = "sd-ec2-keypair"
  public_key = tls_private_key.sd-ec2-key.public_key_openssh

  provisioner "local-exec" { # Create a "myKey.pem" to your computer!!
    command = "echo '${tls_private_key.sd-ec2-key.private_key_pem}' > ./myKey.pem"
  }
}


resource "aws_iam_instance_profile" "profile-sd-ec2" {
  role = aws_iam_role.role-sd-ec2.name
  name = "sd-ec2-instance-profile"
}

resource "aws_iam_role_policy_attachment" "policy-sd-ec2" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.role-sd-ec2.name
}

resource "aws_iam_role" "role-sd-ec2" {
  path = "/"
  name = "sd-ec2-role"
  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_security_group" "sg-sd-ec2" {
  name        = "sd-ec2-sg"
  ingress {
    from_port = 22
    protocol  = "tcp"
    to_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 8000
    protocol  = "tcp"
    to_port   = 8000
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}

# ec2
resource "aws_instance" "sd-ec2" {
  ami           = "ami-054fd176786cbaf84"
  instance_type = "g5.12xlarge"
  iam_instance_profile = aws_iam_instance_profile.profile-sd-ec2.name
  key_name = aws_key_pair.sd-ec2-keypair.key_name
  vpc_security_group_ids = [aws_security_group.sg-sd-ec2.id]
  #user_data = file("user_data.sh")
  user_data = "${file("user_data.sh")}"
  tags = {
        Name = "sdelahaies-ec2-tf"
    }
#   ebs_block_device {
#     device_name = "/dev/sda1"
#     volume_size           = "100"
#     volume_type           = "gp3"
#      }
  
}

output "public_ip" {
  value = aws_instance.sd-ec2.public_ip
}

# output "private_pem" {
#   value = tls_private_key.sd-ec2-key.private_key_pem
#   sensitive = true
# }









