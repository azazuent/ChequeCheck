output "docker" {
  value = {
    docker_server_ip4 = openstack_compute_instance_v2.cheque_check_docker.access_ip_v4
  }
}

