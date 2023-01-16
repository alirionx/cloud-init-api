import yaml

from data_models import CloudConfig, User
from tools import IsoCreator
import passlib.hash



#----------------------------------
my_passwd_hash =  passlib.hash.sha512_crypt.hash("daniel")

# print(my_passwd_hash)
# exit()

#----------------------------------


# myUser = User(**user)
# myIso.add_user(data=myUser)
# myIso.create_userdata_str()
# print(myIso.yaml_str)
# myIso.write_yaml_data_to_iso()



cloud_config = {
  "meta_data": {
    "instance_id": "palim",
    "local_hostname": "palim",
    # "cloud_n.ame": "hyperV",
    "distro": "ubuntu",
    "distro_version": "20.04",
  },
  "user_data": { 
    "groups": ["penners"],
    "users": [
      {
        "name": "daniel",
        "groups": ["sudo", "adm", ],
        "passwd": my_passwd_hash,
        "lock_passwd": False,
        "ssh_pwauth": True,
        "ssh_authorized_keys": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDXp0D0tDZRNxlGcUN/tpVbt7BZCVmdXjJYUbj+BVLc65tjf8gNEY3vCv/gFecW1807TipRnkQ9TGFLXDN7BZ06lXX5VUNS7AFiXY+iGAvJsGLWy6+VLbyBMlNeK+vFQ0GKnQDa7nrVF84uh8Oh6bQ7Jgbtx8HOIDv6Pp4RIDK5X/BWUOfWpeSipXnk1k0c6kv0Hz3B8XzbutgA5YYNabOLIryMMf+07ntCB6dg55nNgItjiw9ogG3EcEshEDJI4T1K4d5EIHc75CxPjGjDLiEjzclsGjldtSTbB+SG7qM4ZTeEb5OSL+Pm225z5xy7AbOVUqEofysKMYNhEpePkY7F",
        "sudo": "ALL=(ALL) NOPASSWD:ALL",
        "shell": "/bin/bash",
        "package_update": True,
        "packages": [
          "iputils-ping",
          "git"
        ],
      }
    ]
  },
  "network_config": {
    "dhcp4": False,
    "ip4_cidrs": [
      "172.18.208.10/20",
      "192.168.0.44/24",
    ],
    "ip4_gw": "172.18.208.1",
    "nameservers": [
      "192.168.10.1",
      "8.8.8.8"
    ],
    "searches": [
      "app-scape.lab",
      "app-scape.de"
    ],

  }
}

myCloudConfig = CloudConfig(**cloud_config)
# print( yaml.dump(myCloudConfig.dict()) )

myIso = IsoCreator(cloud_config=myCloudConfig)
myIso.iso_filename = "ubuntu_cloudinit_test.iso"
myIso.write_cloudinit_iso()

# print(myIso.meta_data_str)
