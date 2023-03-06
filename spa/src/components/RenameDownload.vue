<template>
  <div class="actionFormFrame">
    <div class="actionFormBox">
      <div class="hl">{{title}}</div>
      <div class="ipt_hl">Download-Filename</div>
      <input type="text" v-model="new_dl_filename" />
      
      <div class="btnFrame">
        <button @click="initiate_download">download</button>
        <button @click="callback">cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
// import { useMainStore } from '@/stores/mainStore'

export default {
  setup () {
    // const store = useMainStore()
    // return { store }
  },
  props:{
    selected_rename_download: String,
    set_dl_filename:Function,
    fw_func: Function,
    callback: Function
  },
  data(){
    return{
      title: "Rename Iso Download Dialog",
      new_dl_filename: null
    }
  },
  methods:{
    initiate_download(){
      this.set_dl_filename(this.new_dl_filename)
      this.callback()
    }
  },
  mounted(){
    this.new_dl_filename = this.selected_rename_download.toString()
  }

}
</script>

<style scoped>



</style>