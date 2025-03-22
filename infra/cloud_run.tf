resource "google_cloud_run_v2_service" "default" {
  name                = "moneyapp"
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"


  template {

    containers {
      image = data.google_artifact_registry_docker_image.moneyapp.self_link

      ports {
        container_port = 8000
      }

      env {
        name  = "DB_DATABASE"
        value = var.moneyapp_db_database
      }

      env {
        name  = "DB_USERNAME"
        value = var.moneyapp_db_username
      }

      env {
        name  = "DB_PASSWORD"
        value = var.moneyapp_db_password
      }

      env {
        name  = "DB_HOST"
        value = var.moneyapp_db_host
      }

      env {
        name  = "DB_PORT"
        value = var.moneyapp_db_port
      }

      env {
        name  = "SECRET_KEY"
        value = var.moneyapp_secret_key
      }

      env {
        name  = "ENVIRONMENT"
        value = var.moneyapp_environment
      }

      env {
        name  = "DEBUG"
        value = var.moneyapp_debug
      }

      env {
        name  = "CLOUDRUN_SERVICE_URLS"
        value = join(",", var.cloudrun_service_urls)
      }
    }
  }
}

# Allow unauthenticated invocations
resource "google_cloud_run_v2_service_iam_member" "public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
