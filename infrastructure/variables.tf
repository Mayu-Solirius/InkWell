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

# Extra variables
variable "container_registry_url" {
  type        = string
  description = "URL of the container registry"
}

variable "repository_name" {
  type        = string
  description = "Name of the repository"
}

variable "image_name" {
  type        = string
  description = "Name of the Docker image"
}

variable "image_tag" {
  type        = string
  description = "Tag or version of the Docker image"
}

variable "docker_image_url" {
  type        = string
  description = "Docker image URL in the format '<container-registry-url>/<repository-name>/<image-name>:<tag>'"
  default     = "${var.container_registry_url}/${var.repository_name}/${var.image_name}:${var.image_tag}"
}
