<template>
  <div class="actionFormFrame">
    <div class="actionFormBox cusBox">
      <div class="hl">Cloud init Iso Details: {{ this.iso_id }}</div>

      <div  v-if="details_data.meta_data" >
        <div class="ta_hl">Meta Data</div>
        <textarea class="textBox small" disabled>{{ details_data.meta_data }}</textarea>
      </div>
      
      <div  v-if="details_data.user_data" >
        <div class="ta_hl">User Data</div>
        <textarea class="textBox" disabled>{{ details_data.user_data }}</textarea>
      </div>
      
      <div  v-if="details_data.network_config" >
        <div class="ta_hl">Network Config</div>
        <textarea class="textBox" disabled>{{ details_data.network_config }}</textarea>
      </div>
    
      <div class="btnFrame">
        <button @click="callback">ok</button>
      </div>
    </div>
    
  </div>
</template>

<script>
  import axios from 'axios';
  import { useMainStore } from '@/stores/mainStore'

  export default {
    props:{
      iso_id: String,
      callback: Function,
    },
    setup(){
    const store = useMainStore()
    return { store }
  },
    data(){
      return{
        file_list:{
          "meta-data": "meta_data",
          "user-data": "user_data",
          "network-config": "network_config",
        },
        details_data: {
          meta_data: null,
          user_data: null,
          network_config: null
        }
      }
    },
    methods:{
      call_iso_deatais(){
        for(const [fn, prop] of Object.entries(this.file_list) ){
          axios.get("/api/isos/raw/"+this.iso_id+"/"+fn)
          .then((resp=>{
            this.details_data[prop] = resp.data;
          }))
          .catch((err)=>{

          })
        }
      }
    },
    mounted: function(){
      this.call_iso_deatais();
    }
  }
</script>

<style scoped>
.cusBox{
  margin: 4vh auto 2vh auto;
  min-width: 700px;
}

.ta_hl{
  text-align: left;
  margin: 8px auto 0px auto;
  font-size: 12px;
  font-weight: bold;
}
.textBox{
  margin: 2px auto 2px auto;
  width:98%;
  height: 180px;
  overflow-y: scroll;
  resize: none;
  padding:10px;
}
.small{
  height: 100px;
}

</style>