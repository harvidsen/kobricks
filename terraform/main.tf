terraform {
  required_version = ">=0.15"
  required_providers {
    azurerm = {
        source = "hashicorp/azurerm"
        version = "2.57.0"
    }
    databricks = {
      source = "databrickslabs/databricks"
      version = "0.3.3"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "databricks" {
  azure_workspace_resource_id = azurerm_databricks_workspace.bricks.id
}
