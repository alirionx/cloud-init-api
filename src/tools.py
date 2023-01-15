import os
import yaml
from io import BytesIO, StringIO
import pycdlib

from data_models import CloudConfig

#-The Classes/Tools-----------------------------------
class IsoCreator:
  def __init__(self, cloud_config:CloudConfig):
    
    self.meta_data = self.remove_none_values(
      cloud_config.meta_data.dict()
    )
    self.user_data = self.remove_none_values(
      cloud_config.user_data.dict()
    )
    self.network_config = self.remove_none_values(
      cloud_config.network_config.dict()
    )

    self.meta_data_str = None
    self.user_data_str = None
    self.network_config_str = None

    self.iso_filename = "default.iso"
    self.iso_dir = "./isos"

    self.create_yaml_strs()

  #-------------------------------
  def check_tgt_path(self):
    if not os.path.isdir(self.iso_dir):
      os.makedirs(self.iso_dir)

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
  def create_yaml_strs(self):
    
    #----------
    tmp_item = {}
    for key,val in self.meta_data.items():
      new_key = key.replace("_","-")
      tmp_item[new_key] = val 
    self.meta_data_str = yaml.dump(tmp_item) 

    #----------
    self.user_data_str = "#cloud-config\n\n" + yaml.dump(self.user_data)

    self.network_config_str = yaml.dump(self.network_config)
    
  #-------------------------------
  def write_cloudinit_iso(self):
    self.check_tgt_path()
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

  
    


#-----------------------------------------------------

#-----------------------------------------------------
    
  