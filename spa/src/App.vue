<template>
  <header>
  </header>

  <main>
    <Form />
    <Isos />
  </main>
</template>

<script>
import Isos from '@/components/Isos.vue'
import Form from '@/components/Form.vue'
import { useMainStore } from '@/stores/mainStore'

export default{
  setup(){
    const store = useMainStore()
    store.call_isos()
    return { store }
    
  },
  components:{
    Isos,
    Form
  }
}
</script>



<style scoped>
header {
  line-height: 1.5;
}

</style>
