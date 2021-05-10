# kobricks

Demonstrate databricks setup and use in Azure.

## Use

Working environment is defined as a [nix](https://nixos.org/manual/nix/stable/) shell. Alternatively, build inputs in `shell.nix` must be installed manually. Individual and secret configuration should be set in a `.env` file in root directory which is sourced by `shell.nix`. Here is an example `.env` setup
```
az account set --subscription="<my-subscription-id>"  # set azure subscription for terraform and azure-cli examples

# Optionally configure default resource tags
export TF_VAR_default_tags=$(cat <<-EOM
{
    "<tag-label-1>" = "<tag-value-1>"
    "<tag-label-2>" = "<tag-value-2>"
}
EOM
)
```
**NOTE:** Must be logged in with azure-cli on an active subscription. 

### Deploy databricks environment
We use terraform for creating a reproducible test environment. In the `terraform/` directory run
```
terraform init  # For first time deployment
terraform apply
```
This will create a resource group called *kobas* containing 
- storage account *kobricksaccount*
- blob container *maindata* under *kobricksaccount*
- azure databricks service
- A notebook under `/Shared/blob`

in the currently active azure subscription. Note that the [terraform state](https://www.terraform.io/docs/language/state/index.html) is stored locally in this example. For robust and safe use one should keep the state remotely.

### Examples

#### 1. Create a SAS tokens
One way of connecting to a blob contianer is to use a Secure Access Signature (SAS) token. These allow for fine grained control on container level and have an expiry date for security. For admin access to the might be better to use a [storage account key](https://docs.microsoft.com/en-us/cli/azure/storage/account/keys?view=azure-cli-latest) or connection string.

To generate a SAS token using the azure-cli run
```
./scripts/generate-sas
```
from the root directory. The token will be written to `.env` file. The script uses [`az storage container`](https://docs.microsoft.com/en-us/cli/azure/storage/container?view=azure-cli-latest).

#### 2. Upload data to storage container
The following example uploads `./data/no2_consumption_temperature_2020.csv` to the blob `test/no2_consumption_temperature_2020.csv` in the maindata container using azure-cli. Make sure the credentials from **1.** (`AZURE_STORAGE_ACCOUNT` and `AZURE_STORAGE_SAS_TOKEN`) are set as environment variable and run
```
source .env  # set environment variables if necessary
./scripts/upload
```
This uses [`az storage blob`](https://docs.microsoft.com/en-us/cli/azure/storage/blob?view=azure-cli-latest) for uploading. Note the upcoming [`az storage blob directory`](https://docs.microsoft.com/en-us/cli/azure/storage/blob/directory?view=azure-cli-latest) is worth checking out.

#### 3. Connecting to blob storage in databricks
A complete example is uploaded with terraform deployment. However, this is how you mount a blob storage container to databricks file system using a SAS token
```
dbutils.fs.mount(
  source="wasbs://maindata@kobricksaccount.blob.core.windows.net",  # WASB url of blob
  mount_point="/mnt/maindata",  # where to mount blob here in databricks
  extra_configs = {  # authentication
    "fs.azure.sas.maindata.kobricksaccount.blob.core.windows.net": "<my-sas-key>"
  }
)
```