import sys
import os
import time
import json

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status as HTTPStatus
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from data_models import IsoMetaData, CloudConfig
from tools import CloudInitIsoCreator

#-Build and prep the App----------------------------------------
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
)

#-Initial Things-------------------------------------------------
@app.on_event("startup")
def startup_event():
  inf = "maybe something here later"


#-The Routes----------------------------------------------------
@app.get("/api/", tags=["api_root"])
async def api_root():
  data = {
    "message": "Hello from the Cloud Init ISO Creation API",
    "timestamp": int(time.time())
  }
  return data

#--------------------
@app.get("/api/isos", tags=["meta"], response_model=list[IsoMetaData])
async def api_isos_get():
  res = CloudInitIsoCreator.list_isos()
  return res

#--------------------
@app.get("/api/iso/{id}", tags=["iso"] )
def api_iso_get(id):
  try:
    stream = CloudInitIsoCreator.get_iso_as_byte(iso_id=id)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))
  return StreamingResponse(
    stream,
    headers={'Content-Disposition': 'attachment; filename="%s.iso"' %id}
  )

#--------------------
@app.get("/api/isos/raw/{id}/{filename}", tags=["meta"] )
async def api_iso_conf_file_get(id, filename):
  try:
    res = CloudInitIsoCreator.get_raw_file_from_iso(iso_id=id, filename=filename)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))
  # return res
  return HTMLResponse(content=res, status_code=200)

#--------------------
@app.post("/api/iso", tags=["iso"])
async def api_iso_post(item:CloudConfig):
  myIso = CloudInitIsoCreator(cloud_config=item)
  myIso.write_cloudinit_metadata()
  myIso.write_cloudinit_iso()
  return { "iso_id": myIso.iso_id }

#--------------------


#--------------------


#--------------------


#--------------------


#-Serve the "static" SPA data------------------------
base_path = os.path.abspath("./")
spa_dir = "spa"
spa_path = os.path.join(base_path, spa_dir)

if not os.path.isdir(spa_path):
  os.makedirs(spa_path)
info_file_path = os.path.join(spa_path, "index.html")

if not os.path.isfile(info_file_path):
  with open(info_file_path, "w") as fl:
    fl.write("<h2>You can paste your webUI/SPA files here</h2>")

app.mount("/", StaticFiles(directory=spa_path, html=True), name="static")



#-The Runner---------------------------------------------------------
if __name__ == "__main__":

  if "dev".lower() in sys.argv:
    print("Dev Mode")
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=5000, reload=True)
  else:
    print("Prod Mode")
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=5000)

#--------------------------------------------------------------------