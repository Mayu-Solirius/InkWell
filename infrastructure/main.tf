resource "azurerm_resource_group" "aks-rg" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_role_assignment" "role_acrpull" {
  scope                            = azurerm_container_registry.acr.id
  role_definition_name             = "AcrPull"
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity.0.object_id
  skip_service_principal_aad_check = true
}

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.aks-rg.name
  location            = var.location
  sku                 = "Standard"
  admin_enabled       = true
}

# resource "azurerm_kubernetes_cluster" "aks" {
#   name                = var.cluster_name
#   location            = var.location
#   resource_group_name = azurerm_resource_group.aks-rg.name
#   dns_prefix          = var.cluster_name

#   default_node_pool {
#     name                = "default"
#     node_count          = 1              # Set to 1 for the free tier
#     vm_size             = "Standard_B1s" # Use a free tier VM size
#     enable_auto_scaling = false          # Disable auto-scaling for the free tier
#     max_pods            = 30             # Max pods for the free tier
#   }

#   identity {
#     type = "SystemAssigned"
#   }

#   tags = {
#     nodepooltype = "free"
#   }
# }
