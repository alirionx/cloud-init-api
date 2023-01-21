<template>
  <div class="pagePartDiv">
    <div class="pagePartBar" @click="switch_component()">
      <div class="title">{{title}}</div>
      <div class="arrow " :class="{aUp: active, aDown: !active}"></div>
    </div>
    <div class="pagePartContentFrame" v-if="active">
      <table class="isosTable">
        <thead>
          <tr>
            <th>Iso Id</th>
            <th>Name</th>
            <th style="text-align: center;">Meta Timestamp</th>
            <th style="text-align: center;">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in store.isos" :key="idx">
            <td>{{ item.iso_id }}</td>
            <td>{{ item.name }}</td>
            <td style="text-align: center;">{{ to_date(item.meta_timestamp) }}</td>
            <td style="text-align: center;">
              <div class="actionMenu">
                <img class="icoBtn" src="@/assets/icon_action.png" @click="set_action_idx(idx)" />
                <div class="frame" v-if="action_idx===idx">
                  <div class="btn" @click="details_call">Details</div>
                  <div class="btn" @click="download_call">Download</div>
                  <div class="btn" @click="delete_call">Delete</div>
                </div>
              </div>  
            </td>
          </tr>

        </tbody>
      </table>
    </div>
  </div>
</template>


<script>
import { useMainStore } from '@/stores/mainStore'

export default{
  name: "Isos",
  setup(){
    const store = useMainStore()
    return { store }
  }, 
  data(){
    return {
      id: "isos",
      title: "Stored CloudInit Isos",
      active: true,
      action_idx: null,
      defi: [
       
      ]
    }
  },
  methods:{
    switch_component(){
      this.active = !this.active
    },
    to_date(unx_ts){
      let date = new Date(unx_ts * 1000)
      let date_str = date.toLocaleDateString("de-DE") + " " + date.toLocaleTimeString("de-DE")
      return date_str
    },
    set_action_idx(idx){
      this.action_idx = idx
    },
    reset_action_idx(){
      this.action_idx = null
    },

    details_call(){
      console.log("details: " + this.action_idx)
    },
    download_call(){
      console.log("download: " + this.action_idx)
      let dl_url = "/api/iso/"+this.store.isos[this.action_idx].iso_id
      window.open(dl_url)
    },
    delete_call(){
      console.log("delete: " + this.action_idx)
      this.store.delete_iso_by_idx(this.action_idx)
      
    },

  },
  mounted(){
    document.body.addEventListener("click", (event)=>{
      // console.log(event.target)
      if(!event.target.classList.contains('icoBtn') && !event.target.classList.contains('icoBtn')){
        this.reset_action_idx()
      }
    })
  }
}

</script>


<style scoped>

.Isos{
  text-align: left;
}
.Isos .hl{
  font-size: 20px;
  text-decoration: underline;
  padding:10px;
}
.isosTable{
  margin: 10px auto 14px auto;
  width: 98%;
  max-width: 1600px;
  font-size: 15px;
  padding:0px;
  box-shadow: 0px 2px 3px #444;
}
.isosTable th{
  border-bottom: 1px solid #222;
  background-color: #fff;
  padding:6px;
}
.isosTable td{
  background-color: #fff;
  padding:6px;
  /* position: relative; */
}

.actionMenu{
  position: relative;
  font-size: 12px;
  text-align: center;
  display: table;
  margin: auto;
  width: 120px;
}
.icoBtn{
  height: 28px;
  margin: -6px;
  border-radius: 4px;
  cursor: pointer;
}
.actionMenu .frame{
  z-index: 2;
  position: absolute;
  top: -4px;
  left: 74px;
  box-shadow: 0px 4px 10px #222;
}

.actionMenu .btn{
  background-color: rgb(62, 79, 93);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  padding: 3px;
  border: 1px solid #000;
  margin-bottom: -1px;
  width: 120px;
}
.actionMenu .btn:hover{
  background-color: rgb(80, 100, 118);
}

</style>