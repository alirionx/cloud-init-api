from pydantic import BaseModel, ValidationError
from typing import List, Optional, Literal


#-The Data Models-------------------------------------

class NetworkConfig(BaseModel):
  version: int | None = None
  config: list | None = None

#---------------------
class MetaData(BaseModel):
  instance_id: str 
  local_hostname: str | None = None
  cloud_name: str | None = None
  distro: str | None = None
  distro_version: str | None = None

#---------------------
class User(BaseModel):
  name: str
  groups: List[str] | None = None
  passwd: str | None = None
  chpasswd: str| None = "{ expire: False }"
  lock_passwd: bool | None = False
  ssh_pwauth: bool | None = False
  ssh_authorized_keys: str | None = None
  sudo: str | None = None
  shell: Literal["/bin/sh", "/bin/bash", "/bin/zsh"] | None = None

#---------------------
class UserData(BaseModel):
  groups: list | None = None
  users: list[User] | None = None

#---------------------
class CloudConfig(BaseModel):
  meta_data: MetaData
  user_data: UserData
  network_config: NetworkConfig

#---------------------

#---------------------
  