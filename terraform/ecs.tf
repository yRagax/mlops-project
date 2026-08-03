resource "aws_ecs_cluster" "chpp_cluster" {
  name = var.project_name

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_service" "chpp_service" {
  name                               = "${var.project_name}-service"
  cluster                            = aws_ecs_cluster.chpp_cluster.id
  task_definition                    = aws_ecs_task_definition.chpp_task.arn
  desired_count                      = 1
  launch_type                        = "FARGATE"
  health_check_grace_period_seconds  = 60
  enable_execute_command             = false
  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  load_balancer {
    target_group_arn = aws_lb_target_group.chpp_alb_tg_demo.arn
    container_name   = "chpp-demo"
    container_port   = var.demo_container_port
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.chpp_alb_tg_api.arn
    container_name   = "chpp-api"
    container_port   = var.api_container_port
  }

  network_configuration {
    subnets          = [aws_subnet.chpp_subnet_a.id, aws_subnet.chpp_subnet_b.id, aws_subnet.chpp_subnet_c.id]
    security_groups  = [aws_security_group.chpp_ecs_sg.id]
    assign_public_ip = true
  }

  depends_on = [
    aws_lb_listener.chpp_alb_listener_demo,
    aws_lb_listener.chpp_alb_listener_api,
    aws_internet_gateway.chpp_igw
  ]
}

resource "aws_ecs_task_definition" "chpp_task" {
  family                   = var.project_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.ecs_task_cpu
  memory                   = var.ecs_task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "chpp-demo"
      image     = "058264301042.dkr.ecr.eu-north-1.amazonaws.com/devops-learning/california-house-price-prediction:demo-latest"
      essential = true
      portMappings = [
        {
          containerPort = var.demo_container_port
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.chpp_log_group.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      environment = [
        {
          name  = "DEMO_PORT"
          value = tostring(var.demo_container_port)
        },
        {
          name  = "API_PORT"
          value = tostring(var.api_container_port)
        }
      ]
      linuxParameters = {
        initProcessEnabled = true
      }
      privileged = false
    },
    {
      name      = "chpp-api"
      image     = "058264301042.dkr.ecr.eu-north-1.amazonaws.com/devops-learning/california-house-price-prediction:api-latest"
      essential = true
      portMappings = [
        {
          containerPort = var.api_container_port
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.chpp_log_group.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      environment = [
        {
          name  = "API_PORT"
          value = tostring(var.api_container_port)
        },
        {
          name  = "MODEL_PATH"
          value = tostring(var.model_path)
        }
      ]
      linuxParameters = {
        initProcessEnabled = true
      }
      privileged = false
    }
  ])
}
