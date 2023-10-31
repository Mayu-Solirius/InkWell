resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = var.location
  sku                 = "Standard"
  admin_enabled       = true
}

resource "azurerm_service_plan" "app_service_plan" {
  name                = var.app_plan_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "F1"
}
resource "azurerm_linux_web_app" "webapp" {
  name                = var.app_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.app_service_plan.id

  site_config {
    always_on = false
  }

  app_settings = {
    "WEBSITES_PORT" = "8000"
  }
}

resource "azurerm_role_assignment" "role_acrpull" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = "AcrPull"
  principal_id                     = azurerm_linux_web_app.webapp.identity[0].principal_id
  skip_service_principal_aad_check = true
}

# resource "azurerm_kubernetes_cluster" "aks" {
#   name                = var.cluster_name
#   location            = var.location
#   resource_group_name = azurerm_resource_group.rg.name
#   dns_prefix          = var.cluster_name

#   default_node_pool {
#     name                = "default"
#     node_count          = 1
#     vm_size             = "Standard_B2s"
#     enable_auto_scaling = false
#     max_pods            = 30
#   }

#   identity {
#     type = "SystemAssigned"
#   }

#   tags = {
#     nodepooltype = "free"
#   }
# }

# resource "azurerm_role_assignment" "role_acrpull" {
#   scope                            = azurerm_container_registry.acr.id
#   role_definition_name             = "AcrPull"
#   principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity.0.object_id
#   skip_service_principal_aad_check = true
# }
