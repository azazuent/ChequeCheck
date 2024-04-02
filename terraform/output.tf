output "servers" {
  value = {
    api_server_ip4 = openstack_compute_instance_v2.cheque_check_api.access_ip_v4
    tgbot_server_ip4 = openstack_compute_instance_v2.cheque_check_tgbot.access_ip_v4
    db_server_ip4 = openstack_compute_instance_v2.cheque_check_db.access_ip_v4
  }
}

