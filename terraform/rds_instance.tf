resource "aws_rds_cluster" "golf_rds" {
  cluster_identifier = "golf-serverless-db"
  engine             = "aurora-postgresql"

  engine_mode          = "serverless"
  enable_http_endpoint = true

  availability_zones     = ["us-east-2a", "us-east-2b", "us-east-2c"]
  db_subnet_group_name   = var.db_subnet_group
  vpc_security_group_ids = var.vpc_secgroup_ids

  database_name   = var.db_config["name"]
  master_username = var.db_config["username"]
  master_password = var.db_config["password"]

  backup_retention_period = 7
  deletion_protection     = true

  scaling_configuration {
    auto_pause               = true
    min_capacity             = 0
    max_capacity             = 2
  }
}