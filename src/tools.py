import os
import time
import json
import yaml
from io import BytesIO, StringIO
from uuid import uuid4
import pycdlib

from data_models import CloudConfig, NetworkConfig

#-The Classes/Tools-----------------------------------
class CloudInitIsoCreator:
  iso_dir = "./data/isos"
  meta_dir = "./data/meta"

  def __init__(self, cloud_config:CloudConfig):
    
    self.cloud_config = cloud_config

    self.meta_data_str = None
    self.user_data_str = None
    self.network_config_str = None

    self.iso_id = str(uuid4())
    self.iso_filename = "%s.iso" %self.iso_id
    # self.iso_filename = "default.iso"

    #-----
    self.meta_data = self.remove_none_values(
      self.cloud_config.meta_data.dict()
    )
    self.user_data = self.remove_none_values(
      self.cloud_config.user_data.dict()
    )

    #-----
    if self.cloud_config.network_config:
      self.map_network_conf(item=self.cloud_config.network_config)
    else:
      self.user_data = None

    #-----
    self.create_yaml_strs()
    self.check_tgt_path()

  #-------------------------------
  def check_tgt_path(self):
    os.makedirs(self.iso_dir, exist_ok=True)
    os.makedirs(self.meta_dir, exist_ok=True)

  #-------------------------------
  def remove_none_values(self, obj):
    if isinstance(obj, (list, tuple, set)):
      return type(obj)(self.remove_none_values(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
      return type(obj)((self.remove_none_values(k), self.remove_none_values(v))
        for k, v in obj.items() if k is not None and v is not None)
    else:
      return obj

  #-------------------------------
  def map_network_conf(self, item:CloudConfig):
    tmp_item = {      
      "version": 2,
      "ethernets": {
        "nic0": {
          "match": {
            "name": item.src_nic_match
          },
          "set-name": item.tgt_nic_name,
          "dhcp4": item.dhcp4,
          "addresses": item.ip4_cidrs,
          "gateway4": item.ip4_gw,        
          "nameservers": {
            "search": item.searches,
            "addresses": item.nameservers,    
          }
        } 
      }
    }
    self.network_config = self.remove_none_values(tmp_item)

  #-------------------------------
  def create_yaml_strs(self):
    tmp_item = {}
    for key,val in self.meta_data.items():
      new_key = key.replace("_","-")
      tmp_item[new_key] = val 
    self.meta_data_str = yaml.dump(tmp_item) 

    #----------
    self.user_data_str = "#cloud-config\n\n" + yaml.dump(self.user_data)

    self.network_config_str = yaml.dump(self.network_config)
    
  #-------------------------------
  def write_cloudinit_metadata(self):
    tgt_file_path = os.path.join(self.meta_dir, self.iso_id)
    item = {
      "iso_id": self.iso_id,
      "iso_filename": self.iso_filename,
      "meta_timestamp": int(time.time()),
      "class_config_data": self.cloud_config.dict(),
      "cloud_config_data": {
        "meta-data": self.meta_data_str,
        "user-data": self.user_data_str,
        "network-config": self.network_config_str
      }
    }

    with open(tgt_file_path, "w") as fl:
      fl.write(
        json.dumps(item, indent=2) 
      )


  #-------------------------------
  def write_cloudinit_iso(self):
    tgt_file_path = os.path.join(self.iso_dir, self.iso_filename)
    
    #-----
    iso = pycdlib.PyCdlib()
    iso.new(
      interchange_level=3,
      joliet=True,
      sys_ident='LINUX',
      rock_ridge='1.09',
      vol_ident='cidata'
    )

    #-----
    metadata_file = BytesIO(
      self.meta_data_str.encode()
    )
    iso.add_fp(
      metadata_file, 
      len(self.meta_data_str), 
      '/METADATA.;1', 
      rr_name="meta-data",
      joliet_path="/meta-data"
    )
    
    #-----
    userdata_file = BytesIO(  
      self.user_data_str.encode())
    iso.add_fp(
      userdata_file, 
      len(self.user_data_str), 
      '/USERDATA.;1', 
      rr_name="user-data",
      joliet_path="/user-data"
    )

    #-----
    network_config_file = BytesIO(  
      self.network_config_str.encode())
    iso.add_fp(
      network_config_file, 
      len(self.network_config_str), 
      '/NETWORKCONFIG.;1', 
      rr_name="network-config",
      joliet_path="/network-config"
    )

    #-----
    iso.write( tgt_file_path )
    iso.close()

  #-------------------------------
  @staticmethod
  def list_isos():
    res = []
    for filename in os.listdir(CloudInitIsoCreator.meta_dir):
      filepath = os.path.join(CloudInitIsoCreator.meta_dir, filename)
      with open(filepath, "r") as fl:
        json_str = fl.read()
        try: 
          item = json.loads(json_str)
        except Exception as e:
          print(e)
          continue
        res.append(item)
    return res

  #-------------------------------
  @staticmethod
  def get_iso_filename_by_id(iso_id:str):
    meta_filepath = os.path.join(CloudInitIsoCreator.meta_dir, iso_id)
    if not os.path.isfile(meta_filepath):
      raise Exception("ISO with id '%s' not found" %iso_id)
    with open(meta_filepath, "r") as fl:
      item = json.loads(fl.read())
    iso_filename = item["iso_filename"]
    return iso_filename

  #-------------------------------
  @staticmethod
  def delete_iso_by_id(iso_id:str):
    meta_filepath = os.path.join(CloudInitIsoCreator.meta_dir, iso_id)
    if not os.path.isfile(meta_filepath):
      raise Exception("ISO with id '%s' not found" %iso_id)
    
    iso_filename = CloudInitIsoCreator.get_iso_filename_by_id(iso_id=iso_id)
    iso_filepath = os.path.join(CloudInitIsoCreator.iso_dir, iso_filename)
    os.unlink(meta_filepath)
    os.unlink(iso_filepath)

  #-------------------------------
  @staticmethod
  def get_raw_file_from_iso(iso_id:str, filename:str):    
    iso_filename = CloudInitIsoCreator.get_iso_filename_by_id(iso_id=iso_id)
    iso_filepath = os.path.join(CloudInitIsoCreator.iso_dir, iso_filename)

    iso = pycdlib.PyCdlib()
    iso.open(filename=iso_filepath)
    extracted = BytesIO()
    try:
      iso.get_file_from_iso_fp(extracted, iso_path='/%s.;1' %filename.upper().replace("-", ""))
    except:
      raise Exception("could not extract file '%s' from iso '%s'" %(filename, iso_id) )
    iso.close()
    return extracted.getvalue().decode('utf-8')

  #-------------------------------
  @staticmethod
  def get_iso_as_byte(iso_id:id):
    iso_filename = CloudInitIsoCreator.get_iso_filename_by_id(iso_id=iso_id)
    iso_filepath = os.path.join(CloudInitIsoCreator.iso_dir, iso_filename)
    with open(iso_filepath, "rb") as fl:
      yield from fl

  #-------------------------------
  #-------------------------------
  

  
    


#-----------------------------------------------------

#-----------------------------------------------------
    
  