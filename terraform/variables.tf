variable "subscription_id" {
  type = string
}

variable "resource_group_name" {
  type    = string
  default = "rg-azure-estudo"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "db_host" {
  type = string
}

variable "db_name" {
  type    = string
  default = "adp_test"
}

variable "db_user" {
  type    = string
  default = "pgadmin"
}

variable "db_password" {
  type      = string
  sensitive = true
}
