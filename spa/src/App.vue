<template>
  <header>
  </header>

  <main>
    <Form></Form>
    <Isos />
    <Loader v-if="store.loader" />
    <ConfirmBox v-if="store.system_confirm.forward" />
  </main>
</template>

<script>
import Loader from '@/components/Loader.vue'
import ConfirmBox from '@/components/ConfirmBox.vue'
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
    Loader,
    ConfirmBox,
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
