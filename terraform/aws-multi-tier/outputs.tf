output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "database_subnet_ids" {
  description = "IDs of database subnets"
  value       = aws_subnet.database[*].id
}

output "web_security_group_id" {
  description = "ID of web tier security group"
  value       = aws_security_group.web.id
}

output "database_security_group_id" {
  description = "ID of database tier security group"
  value       = aws_security_group.database.id
}

output "s3_bucket_name" {
  description = "Name of S3 bucket for assets"
  value       = aws_s3_bucket.app_assets.id
}
