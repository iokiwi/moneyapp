data "google_artifact_registry_docker_image" "moneyapp" {
  location      = google_artifact_registry_repository.my-repo.location
  repository_id = google_artifact_registry_repository.my-repo.repository_id
  image_name    = "${var.docker_image_name}:${var.docker_image_tag}"
}
