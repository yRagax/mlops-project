output "alb_dns_name" {
  description = "Public DNS name of the application load balancer."
  value       = aws_lb.chpp.dns_name
}

output "demo_url" {
  description = "URL for the Gradio demo."
  value       = "http://${aws_lb.chpp.dns_name}:${var.demo_container_port}"
}

output "api_url" {
  description = "URL for the inference API."
  value       = "http://${aws_lb.chpp.dns_name}:${var.api_container_port}"
}
