terraform {
  required_version = ">=0.15"
  required_providers {
    azurerm = {
        source = "hashicorp/azurerm"
        version = "2.57.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name = "kobricks"
  location = "norwayeast"
  tags = var.default_tags
}

resource "azurerm_storage_account" "main" {
  name                     = "kobricksaccount"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags = var.default_tags
}

resource "azurerm_storage_container" "main" {
  name                  = "maindata"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}