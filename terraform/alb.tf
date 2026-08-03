resource "aws_lb" "chpp" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.chpp_alb_sg.id]
  subnets            = [aws_subnet.chpp_subnet_a.id, aws_subnet.chpp_subnet_b.id, aws_subnet.chpp_subnet_c.id]

  drop_invalid_header_fields = true

  tags = {
    Name = "${var.project_name}-alb"
  }
}

resource "aws_lb_target_group" "chpp_alb_tg_demo" {
  name        = "${var.project_name}-alb-tg-demo"
  port        = var.demo_container_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.chpp_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/"
    matcher             = "200-399"
  }

  tags = {
    Name = "${var.project_name}-alb-tg-demo"
  }
}

resource "aws_lb_target_group" "chpp_alb_tg_api" {
  name        = "${var.project_name}-alb-tg-api"
  port        = var.api_container_port
  protocol    = "HTTP"
  vpc_id      = aws_vpc.chpp_vpc.id
  target_type = "ip"

  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/docs"
    matcher             = "200-399"
  }

  tags = {
    Name = "${var.project_name}-alb-tg-api"
  }
}

resource "aws_lb_listener" "chpp_alb_listener_demo" {
  load_balancer_arn = aws_lb.chpp.arn
  port              = var.demo_container_port
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.chpp_alb_tg_demo.arn
  }
}

resource "aws_lb_listener" "chpp_alb_listener_api" {
  load_balancer_arn = aws_lb.chpp.arn
  port              = var.api_container_port
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.chpp_alb_tg_api.arn
  }
}
