
data "databricks_node_type" "smallest" {
  local_disk = true
}

data "databricks_spark_version" "mlruntime" {
  ml = true
  spark_version = "3.1"
}

resource "databricks_cluster" "smallcluster" {
  cluster_name            = "smallcluster"
  spark_version           = data.databricks_spark_version.mlruntime.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 30
  autoscale {
    min_workers = 1
    max_workers = 10
  }
}


data "databricks_current_user" "me" { }

resource "databricks_notebook" "blob" {
  source = "${path.module}/../notebooks/blob.py"
  path = "${data.databricks_current_user.me.home}/blob"
}