<template>
  <header>
  </header>

  <main>
    <Isos />
  </main>
</template>

<script>
import Isos from '@/components/Isos.vue'
import { useMainStore } from '@/stores/mainStore'

export default{
  setup(){
    const store = useMainStore()
    store.call_isos()
    return { store }
    
  },
  components:{
    Isos
  }
}
</script>



<style scoped>
header {
  line-height: 1.5;
}

</style>
