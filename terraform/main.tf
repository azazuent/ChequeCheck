terraform {
  required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.39.0"
    }
  }
}

provider "vault" {
  address = "http://localhost:8200"
}

data "vault_generic_secret" "openstack" {
  path = "secret/openstack"
}

provider "openstack" {
  auth_url = data.vault_generic_secret.openstack.data["url"]  
  tenant_id = data.vault_generic_secret.openstack.data["id"]
  tenant_name = data.vault_generic_secret.openstack.data["name"]
  user_domain_name = data.vault_generic_secret.openstack.data["domain"]
  user_name = data.vault_generic_secret.openstack.data["uname"]
  password = data.vault_generic_secret.openstack.data["password"]
  region = data.vault_generic_secret.openstack.data["region"]
}

resource "openstack_networking_secgroup_v2" "secgroup" {
  name        = "cheque_check_sg"
}

resource "openstack_networking_secgroup_rule_v2" "secgroup_default_rule" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 1
  port_range_max    = 20000
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = openstack_networking_secgroup_v2.secgroup.id
}

resource "openstack_compute_instance_v2" "cheque_check_tgbot" {
  name        = "cheque_check_tgbot"
  image_name  = var.image_name
  flavor_name = var.flavor_name
  key_pair = var.key_pair
  security_groups = [openstack_networking_secgroup_v2.secgroup.name]

  network {
    name = var.network_name
  }
}

resource "openstack_compute_instance_v2" "cheque_check_db" {
  name        = "cheque_check_db"
  image_name  = var.image_name
  flavor_name = var.flavor_name
  key_pair = var.key_pair
  security_groups = [openstack_networking_secgroup_v2.secgroup.name]

  network {
    name = var.network_name
  }
}

resource "openstack_compute_instance_v2" "cheque_check_api" {
  name        = "cheque_check_api"
  image_name  = var.image_name
  flavor_name = var.flavor_name
  key_pair = var.key_pair
  security_groups = [openstack_networking_secgroup_v2.secgroup.name]

  network {
    name = var.network_name
  }
}
