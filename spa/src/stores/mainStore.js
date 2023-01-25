import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMainStore = defineStore({
  id: 'mainStore', 
  state: () => {
    return {
      loader: false,
      system_confirm:{
        message: "Penneralarm",
        forward: null
      },
      isos: []
    }
  },
  actions: {
    set_loader(){
      this.loader = true;
    },
    reset_loader(){
      this.loader = false;
    },
    reset_system_confirm(){
      this.system_confirm.message = null;
      this.system_confirm.forward = null;
    },
    call_isos(){
      axios.get("/api/isos")
      .then((response)=>{
        // console.log(response.status)
        this.isos =  response.data
      })
      .catch((err)=>{
        console.error(err)
      })
      .finally(()=>{
        // this.sort_isos("name")
        this.sort_isos("meta_timestamp", true)
      })
    },
    sort_isos(key, reverse=false){
      this.isos.sort((a,b) => (a[key] > b[key]) ? 1 : ((b[key] > a[key]) ? -1 : 0))
      if(reverse) this.isos.reverse()
    },
    create_iso(data, callback){
      axios.post("/api/iso", data)
      .then((response)=>{
        // console.log(response.status)
        this.call_isos()
      })
      .catch((err)=>{
        console.error(err)
      })
      .finally(()=>{
        if(callback){ callback() }
      })
    },
    delete_iso_by_idx(idx){
      let iso_id = this.isos[idx].iso_id
      axios.delete("/api/iso/"+iso_id)
      .then((response)=>{
        // console.log(response.status)
        this.isos.splice(idx, 1)
      })
      .catch((err)=>{
        console.error(err)
      })
      .finally(()=>{
      })
    }
  }
})

