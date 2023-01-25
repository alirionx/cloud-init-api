<template>
  <div class="actionFormFrame">
    <div class="actionFormBox">
      <div class="hl">{{title}}</div>
      
      <div class="msgBox">{{ store.system_confirm.message }}</div>
      <div class="btnFrame">
        <button @click="confirm_fw">ok</button>
        <button @click="store.reset_system_confirm">cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import { useMainStore } from '@/stores/mainStore'

export default {
  setup () {
    const store = useMainStore()
    return { store }
  },
  data(){
    return{
      title: "System Confirm Dialog"
    }
  },
  methods:{
    confirm_fw(){
      this.store.system_confirm.forward();
      this.store.reset_system_confirm();
    } 
  }
}
</script>

<style scoped>
.msgBox{
  display: table;
  width: 95%;
  padding:12px;
  margin: 10px auto 2px auto;
  font-size: 18px;
  color:#000;
  text-align: center;
  background-color: #fafafa;
  border: 1px solid #aaa;
}


</style>