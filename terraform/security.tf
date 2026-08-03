resource "aws_security_group" "chpp_alb_sg" {
  name        = "${var.project_name}-alb-sg"
  description = "Security group for the CHPP application load balancer"
  vpc_id      = aws_vpc.chpp_vpc.id

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "chpp_alb_ingress_demo" {
  security_group_id = aws_security_group.chpp_alb_sg.id
  description       = "Allow demo traffic from allowed CIDR"
  ip_protocol       = "tcp"
  from_port         = var.demo_container_port
  to_port           = var.demo_container_port
  cidr_ipv4         = var.allowed_ingress_cidr
}

resource "aws_vpc_security_group_ingress_rule" "chpp_alb_ingress_api" {
  security_group_id = aws_security_group.chpp_alb_sg.id
  description       = "Allow API traffic from allowed CIDR"
  ip_protocol       = "tcp"
  from_port         = var.api_container_port
  to_port           = var.api_container_port
  cidr_ipv4         = var.allowed_ingress_cidr
}

resource "aws_vpc_security_group_egress_rule" "chpp_alb_egress" {
  security_group_id            = aws_security_group.chpp_alb_sg.id
  ip_protocol                  = "tcp"
  from_port                    = var.demo_container_port
  to_port                      = var.api_container_port
  referenced_security_group_id = aws_security_group.chpp_ecs_sg.id
}

resource "aws_security_group" "chpp_ecs_sg" {
  name        = "${var.project_name}-ecs-sg"
  description = "Security group for CHPP ECS tasks"
  vpc_id      = aws_vpc.chpp_vpc.id

  tags = {
    Name = "${var.project_name}-ecs-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "chpp_ingress_from_alb_demo" {
  security_group_id            = aws_security_group.chpp_ecs_sg.id
  description                  = "Allow demo traffic from ALB only"
  ip_protocol                  = "tcp"
  from_port                    = var.demo_container_port
  to_port                      = var.demo_container_port
  referenced_security_group_id = aws_security_group.chpp_alb_sg.id
}

resource "aws_vpc_security_group_ingress_rule" "chpp_ingress_from_alb_api" {
  security_group_id            = aws_security_group.chpp_ecs_sg.id
  description                  = "Allow API traffic from ALB only"
  ip_protocol                  = "tcp"
  from_port                    = var.api_container_port
  to_port                      = var.api_container_port
  referenced_security_group_id = aws_security_group.chpp_alb_sg.id
}

resource "aws_vpc_security_group_egress_rule" "chpp_egress_https" {
  security_group_id = aws_security_group.chpp_ecs_sg.id
  description       = "Allow HTTPS for package and image pulls"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
}

resource "aws_vpc_security_group_egress_rule" "chpp_egress_dns_udp" {
  security_group_id = aws_security_group.chpp_ecs_sg.id
  description       = "Allow DNS resolution"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "udp"
  from_port         = 53
  to_port           = 53
}

resource "aws_vpc_security_group_egress_rule" "chpp_egress_dns_tcp" {
  security_group_id = aws_security_group.chpp_ecs_sg.id
  description       = "Allow DNS over TCP"
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "tcp"
  from_port         = 53
  to_port           = 53
}
