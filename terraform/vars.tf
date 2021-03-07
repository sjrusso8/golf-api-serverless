variable "db_subnet_group" {
  description = "the subnet group for which the db can be accessed"
  type        = string
}

variable "vpc_secgroup_ids" {
  description = "the security groups associated with the rds instance"
  type        = list(string)
}

variable "db_config" {
  description = "db settings for the rds instance"
  type        = map(string)
}