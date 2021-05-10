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

resource "azurerm_databricks_workspace" "bricks" {
  name = "kobricks"
  resource_group_name = azurerm_resource_group.rg.name
  location = azurerm_resource_group.rg.location
  sku = "standard"

  tags = var.default_tags
}

output "kobricks_url" {
  value = azurerm_databricks_workspace.bricks.workspace_url
}
