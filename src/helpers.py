
import re 
import unicodedata


#--------------------------------------
def string_to_valid_filename(string:str, add_iso_ending=True):
  filename = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('ascii')
  filename = re.sub(r'[^\w\s-]', '', filename.lower())
  filename = re.sub(r'[-\s]+', '-', filename).strip('-_')
  
  if add_iso_ending and not filename.endswith(".iso"):
    filename = filename + ".iso"
  return filename

#--------------------------------------


#--------------------------------------


#--------------------------------------