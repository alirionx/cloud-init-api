<template>
  <div class="pagePartDiv">
    <div class="pagePartBar" @click="switch_component()">
      <div class="title">{{title}}</div>
      <div class="arrow " :class="{aUp: active, aDown: !active}"></div>
    </div>
    <div class="pagePartContentFrame" v-if="active">
      <table>
        <thead>
          <tr>
            <th>Iso Id</th>
            <th>Meta Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, idx) in store.isos" :key="idx">
            <td>{{ item.iso_id }}</td>
            <td>{{ item.meta_timestamp }}</td>
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
      active: false
    }
  },
  methods:{
    switch_component(){
      this.active = !this.active
    }
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
.Isos table th,td{
  text-align: left;
  border: 0.5px solid #aaa;
}

</style>