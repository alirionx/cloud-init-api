import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useMainStore = defineStore({
  id: 'mainStore', 
  state: () => {
    return {
      isos: []
    }
  },
  actions: {
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

      })
    }
  }
})

