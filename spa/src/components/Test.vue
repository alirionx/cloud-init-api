<template>
  <div @click="change_it">
    {{ test }}
  </div>
</template>

<script>
export default {
  setup () {
    return {
      
    }
  },
  data(){
    return{
      test: "Penner"
    }
  },
  methods:{
    change_it(){
      this.test = "PALIM"
    }
  }
}
</script>

<style lang="scss" scoped>

</style>