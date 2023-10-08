terraform {
  backend "azurerm" {
    resource_group_name  = "cloud-shell-storage-westeurope"
    storage_account_name = "blobstorageterraform"
    container_name       = "terraform-state"
    key                  = "terraform.tfstate"
  }
}
