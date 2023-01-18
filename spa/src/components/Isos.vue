<template>
  <div class="Isos">
    <div class="hl">{{title}}</div>
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
      title: "Stored CloudInit Isos"
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