# Databricks on Azure with Terraform

Tags: Terraform

This note is mainly to give an overall walk-through of how to deploy Databricks workspace and cluster by using Terraform.

### Providers

```jsx
provider "azurerm" {
  features {}
}

provider "databricks" {
  azure_workspace_resource_id = azurerm_databricks_workspace.this.id
}
```

### Versions

This is where we tell Terraform what version of Terraform it must use as well constraints we may have about any providers.

```jsx
terraform {
  required_version = ">= 1.0"

  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 1.0"
    }
    databricks = {
      source = "databrickslabs/databricks"
    }
  }
}
```

### Variables

What information we pass into our code, below we declare the variables we required or optional.

```jsx
variable "location" {
  type        = string
  description = "(Optional) The location for resource deployment"
  default     = "australiaeast"
}

variable "environment" {
  type        = string
  description = "(Required) Three character environment name"

  validation {
    condition     = length(var.environment) <= 3
    error_message = "Err: Environment cannot be longer than three characters."
  }
}

variable "project" {
  type        = string
  description = "(Required) The project name"
}

variable "databricks_sku" {
  type        = string
  description = <<EOT
    (Optional) The SKU to use for the databricks instance"

    Default: standard
EOT

  validation {
    condition     = can(regex("standard|premium|trial", var.databricks_sku))
    error_message = "Err: Valid options are 'standard', 'premium' or 'trial'."
  }
}
```

### Main

```jsx
locals {
  naming = {
    location = {
      "australiaeast" = "aue"
    }
  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "this" {
  name = format("rg-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  location = var.location
}

resource "azurerm_key_vault" "this" {
  name = format("kv-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  tenant_id           = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "Set",
      "Delete",
      "Recover",
      "Purge"
    ]
  }
}

resource "azurerm_databricks_workspace" "this" {
  name = format("dbs-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
  sku                 = var.databricks_sku

  custom_parameters {
    virtual_network_id  = azurerm_virtual_network.this.id
    public_subnet_name  = azurerm_subnet.public.name
    private_subnet_name = azurerm_subnet.private.name
  }

  depends_on = [
    azurerm_subnet_network_security_group_association.public,
    azurerm_subnet_network_security_group_association.private,
  ]
}
```

### Network

- `[azurerm_virtual_network](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network)` - The virtual network (or VPC on AWS/GCP) that will be used to hold our subnets.
- `[azurerm_subnet](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet)` - The subnets that will be associated with our `[azurerm_databricks_workspace](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/databricks_workspace)`
- `[azurerm_network_security_group](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group)` - This is where any *firewall* type activity will be setup.
- `[azurerm_subnet_network_security_group_association](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet_network_security_group_association)` - The association between the subnet and the network security group

```jsx
resource "azurerm_virtual_network" "this" {
  name = format("vn-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name

  address_space = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "private" {
  name = format("sn-%s-%s-%s-priv",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.0.0.0/24"]

  delegation {
    name = "databricks-delegation"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action",
      ]
    }
  }
}

resource "azurerm_network_security_group" "private" {
  name = format("nsg-%s-%s-%s-priv",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
}

resource "azurerm_subnet_network_security_group_association" "private" {
  subnet_id                 = azurerm_subnet.private.id
  network_security_group_id = azurerm_network_security_group.private.id
}

resource "azurerm_subnet" "public" {
  name = format("sn-%s-%s-%s-pub",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name  = azurerm_resource_group.this.name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "databricks-delegation"

    service_delegation {
      name = "Microsoft.Databricks/workspaces"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
        "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action",
        "Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action",
      ]
    }
  }
}

resource "azurerm_network_security_group" "public" {
  name = format("nsg-%s-%s-%s-pub",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location
}

resource "azurerm_subnet_network_security_group_association" "public" {
  subnet_id                 = azurerm_subnet.public.id
  network_security_group_id = azurerm_network_security_group.public.id
}
```

> It is very important to note the following things:
> 
- Delegation **must** be set on the subnets for the resource type Microsoft.Databricks/workspaces
- Network security groups must be associated with the subnets. It is suggested that the NSGs are empty as Databricks will assign the appropriate rules.
- In order to prevent an error about *Network Intent Policy* there **must** be an explicit dependsOn between the network security group associations and the Databricks workspace.

### Azure Active Directory (AAD)

Before we look into creating the internals of our Databricks instance or our Azure Synapse database we must first create the Azure Active Directory (AAD) application that will be used for authentication.

```jsx
resource "random_password" "service_principal" {
  length  = 16
  special = true
}

resource "azurerm_key_vault_secret" "service_principal" {
  name         = "service-principal-password"
  value        = random_password.service_principal.result
  key_vault_id = azurerm_key_vault.this.id
}

resource "azuread_application" "this" {
  display_name = format("app-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)
}

resource "azuread_service_principal" "this" {
  application_id               = azuread_application.this.application_id
  app_role_assignment_required = false
}

resource "azuread_service_principal_password" "this" {
  service_principal_id = azuread_service_principal.this.id
  value                = azurerm_key_vault_secret.service_principal.value
}

resource "azurerm_role_assignment" "this" {
  scope                = azurerm_storage_account.this.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.this.object_id
}
```

Above we are creating resources with the following properties:

- `[random_password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password)` - A randomly generated password that will be assigned to our service principal
- `[azurerm_key_vault_secret](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret)` - A secret that will be used to store the password for the service principal
- `[azuread_application](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/application)` - A new Azure Active Directory (AAD) application that will be used for the service principal
- `[azuread_service_principal](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/service_principal)` - A new service principal that will be used for authentication on our Synapse instance
- `[azuread_service_principal_password](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/service_principal_password)` - The password that will be associated with the service principal, this is what we stored in the key vault earlier
- `[azurerm_role_assignment](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment)` - A new role assignment that will be used to grant the service principal the ability to access and manage a storage account for Synapse

### Synapse

```jsx
resource "azurerm_storage_account" "this" {
  name = format("sa%s%s%s",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "BlobStorage"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "this" {
  name = format("fs%s%s%s",
  local.naming.location[var.location], var.environment, var.project)
  storage_account_id = azurerm_storage_account.this.id
}

resource "azurerm_key_vault_secret" "sql_administrator_login" {
  name         = "sql-administrator-login"
  value        = "sqladmin"
  key_vault_id = azurerm_key_vault.this.id
}

resource "random_password" "sql_administrator_login" {
  length  = 16
  special = false
}

resource "azurerm_key_vault_secret" "sql_administrator_login_password" {
  name         = "sql-administrator-login-password"
  value        = random_password.sql_administrator_login.result
  key_vault_id = azurerm_key_vault.this.id
}

resource "azurerm_synapse_workspace" "this" {
  name = format("ws-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  resource_group_name                  = azurerm_resource_group.this.name
  location                             = azurerm_resource_group.this.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.this.id

  aad_admin = [
    {
      login     = "AzureAD Admin"
      object_id = azuread_service_principal.this.object_id
      tenant_id = data.azurerm_client_config.current.tenant_id
    }
  ]

  sql_administrator_login          = azurerm_key_vault_secret.sql_administrator_login.value
  sql_administrator_login_password = azurerm_key_vault_secret.sql_administrator_login_password.value
}

resource "azurerm_synapse_sql_pool" "this" {
  name = format("pool_%s",
  var.project)

  synapse_workspace_id = azurerm_synapse_workspace.this.id
  sku_name             = "DW100c"
  create_mode          = "Default"
}

resource "azurerm_synapse_firewall_rule" "allow_azure_services" {
  name                 = "AllowAllWindowsAzureIps"
  synapse_workspace_id = azurerm_synapse_workspace.this.id
  start_ip_address     = "0.0.0.0"
  end_ip_address       = "0.0.0.0"
}
```

### Databricks

A single node Databricks cluster

```jsx
data "databricks_node_type" "smallest" {
  local_disk = true

  depends_on = [
    azurerm_databricks_workspace.this
  ]
}

data "databricks_spark_version" "latest_lts" {
  long_term_support = true

  depends_on = [
    azurerm_databricks_workspace.this
  ]
}

resource "databricks_cluster" "this" {
  cluster_name = format("dbsc-%s-%s-%s",
  local.naming.location[var.location], var.environment, var.project)

  spark_version = data.databricks_spark_version.latest_lts.id
  node_type_id  = data.databricks_node_type.smallest.id

  autotermination_minutes = 20

  spark_conf = {
    "spark.databricks.cluster.profile" : "singleNode"
    "spark.master" : "local[*]"
  }

  custom_tags = {
    "ResourceClass" = "SingleNode"
  }
}
```

### Outputs

- the information we want returned to us once the deployment of all the previous code is complete
- In some case, some value pass onto other modules which can be used

```jsx
output "azure_details" {
  sensitive = true
  value = {
    tenant_id     = data.azurerm_client_config.current.tenant_id
    client_id     = azuread_application.this.application_id
    client_secret = azurerm_key_vault_secret.service_principal.value
  }
}

output "storage_account" {
  sensitive = true
  value = {
    name           = azurerm_storage_account.this.name
    container_name = azurerm_storage_data_lake_gen2_filesystem.this.name
    access_key     = azurerm_storage_account.this.primary_access_key
  }
}

output "synapse" {
  sensitive = true
  value = {
    database = azurerm_synapse_sql_pool.this.name
    host     = azurerm_synapse_workspace.this.connectivity_endpoints
    user     = azurerm_synapse_workspace.this.sql_administrator_login
    password = azurerm_synapse_workspace.this.sql_administrator_login_password
  }
}
```

### Deploy

```bash
terraform init
```

```bash
terraform plan -var="environment=dev" -var="project=meow"
```

```bash
terraform apply -var="environment=dev" -var="project=meow"
```