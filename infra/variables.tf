variable "region" {
  default = "australia-southeast1"
}

variable "project_id" {
  type = string
}

variable "docker_repository_name" {
  
}

variable "docker_image_name" {
  type    = string
  default = "moneyapp-app"
}

variable "docker_image_tag" {
  type    = string
  default = "latest"
}

variable "cloudrun_service_urls" {
  type = list(string)
}

variable "moneyapp_environment" {
  type        = string
  description = ""
  default     = "prod"
}

variable "moneyapp_debug" {
  type        = string
  description = ""
  default     = false
}

variable "moneyapp_db_database" {
  type        = string
  description = "The name of the database for the MoneyApp application"
}

variable "moneyapp_db_username" {
  type        = string
  description = "The username for connecting to the MoneyApp database"
}

variable "moneyapp_db_password" {
  type        = string
  description = "The password for connecting to the MoneyApp database"
  sensitive   = true
}

variable "moneyapp_db_host" {
  type        = string
  description = "The host address of the MoneyApp database"
}

variable "moneyapp_db_port" {
  type        = string
  description = "The port number for connecting to the MoneyApp database"
}

variable "moneyapp_secret_key" {
  type        = string
  description = "The secret key for the MoneyApp application"
  sensitive   = true
}
