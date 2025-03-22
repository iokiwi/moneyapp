# Output the service URL
output "service_url" {
  value = google_cloud_run_v2_service.default.uri
}

output "image" {
  value = data.google_artifact_registry_docker_image.moneyapp.self_link
}