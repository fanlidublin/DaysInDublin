# Reducing Terraform code duplication

Tags: Terraform

One thing that happens a lot with Infrastructure as Code, especially with Terraform is that a lot of the code is repeated. Whether that be through duplication of calls to modules, or naked resources. What I mean by duplication in this instance is as follows; say we have three environments each of these environments requires an identical set of cloud resources, one practice would be to have three instances of this terraform code ( either existing in their own repository or directory ) then input variables are supplied to each of these instances. This means, that we have the same, or nearly the same code written - or worse, copy pasted - three times.

```yaml
global:
  zone: "us-west1-b"

environments:
  dev:
    zone: "us-west2-a"
    iaas:
      image: "debian-cloud/debian-10"
      machine_type: "e2-micro"
    network:
      name: "default"
  prod:
    zone:
    iaas:
      image: "debian-cloud/debian-10"
      machine_type: "e2-standard-8"
```

As can be seen in the above, we have two primary sections global and environment, the former holds information that is applicable across anything that the Terraform code may be doing whereas the latter contains configuration information about a specific environment. One thing to note here, is that we have zone defined in our global section however, we also have this defined in out dev environment, this is essentially how we will be enabling an override of a default value. The below code shows the corresponding Terraform code that will consume our `config.yaml`

```jsx
locals {
  raw_config = yamldecode(file(format("%s/config.yaml", path.module)))
  config = {
    global = local.raw_config.global
    environment = lookup(local.raw_config.environments, var.environment, "err: invalid environment")
  }
}

variable "environment" {
  type = string
  description = "(Optional) Name of the environment to deploy into"
  default = "dev"
}

resource "google_compute_instance" "this" {
  name = format("iaas-%s", var.environment)
  machine_type = local.config.environment.iaas.machine_type
  // This is essentially saying
  // if the value for local.config.environment.zone is null 
  // then use the value at local.config.global.zone this simple technique 
  // is something that is extremely useful in both the yaml 
  // config solution as well as general Terraform.
	zone = local.config.environment.zone != null ? local.config.environment.zone : local.config.global.zone

  boot_disk {
    initialize_params {
      image = local.config.environment.iaas.image
    }
  }

  network_interface {
    network = local.config.environment.network.name
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
}
```

when apply, we can do something like following

```jsx
terraform apply -var=”environment=prod”
```