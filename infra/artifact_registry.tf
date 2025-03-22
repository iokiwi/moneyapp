resource "google_artifact_registry_repository" "my-repo" {
  location      = var.region
  repository_id = var.docker_repository_name
  description   = "example docker repository"
  format        = "DOCKER"
}
