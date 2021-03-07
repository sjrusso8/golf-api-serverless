resource "aws_rds_cluster" "golf_rds" {
    cluster_identifier = "golf-serverless-db"
    engine = "aurora-postgressql"
    engine_mode = "serverless"

    availability_zones = [ "us-east-2a", "us-east-2b", "us-east-2c" ]
    
    database_name = var.database_name
    master_username = var.master_username
    master_password = var.master_password
    
}