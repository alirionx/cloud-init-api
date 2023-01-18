<template>
  <header>
  </header>

  <main>
    <Isos />
    <!-- <Test /> -->
  </main>
</template>

<script>
import Isos from '@/components/Isos.vue'
import Test from '@/components/Test.vue'
import { useMainStore } from '@/stores/mainStore'

export default{
  setup(){
    const store = useMainStore()
    store.call_isos()
    return { store }
    
  },
  components:{
    Isos,
    Test
  }
}
</script>



<style scoped>
header {
  line-height: 1.5;
}

</style>
