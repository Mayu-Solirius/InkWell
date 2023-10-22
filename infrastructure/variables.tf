variable "resource_group_name" {
  type        = string
  description = "Resource Group name in Azure"
}
variable "location" {
  type        = string
  description = "Resources location in Azure"
}
variable "cluster_name" {
  type        = string
  description = "AKS name in Azure"
}
variable "acr_name" {
  type        = string
  description = "ACR name"
}
variable "app_name" {
  type        = string
  description = "App Service name"
}
variable "app_plan_name" {
  type        = string
  description = "App Service Plan name"
}

variable "image_name" {
  type        = string
  description = "Name of the Docker image"
  default     = "inkwell-img"
}
