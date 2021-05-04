<template>
  <v-container id="footer" ref="footer" v-mutate.attr="onMutate" style="z-index:100 !important;">
    <v-row>
      <v-col cols="12" nogutter>
        <span style="padding-bottom: 8px; font-weight: bold; display: block">A collaboration between:</span>
        <img src="https://gitcdn.link/repo/kent-map/kent/main/dickens/images/CCCU-logo-2colour.svg" height="30px"> &nbsp;&nbsp;&nbsp;&nbsp;
        <img src="https://gitcdn.link/repo/kent-map/kent/main/images/labs.jpg" height="30px">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  module.exports = {  
    data: () => ({
      height: undefined
    }),
    mounted() {
      this.height = this.$refs.footer.clientHeight
      this.$emit('footer-height', this.height)
    },
    methods: {
      onMutate(mutations) {
        const mutation = mutations[mutations.length - 1]
        if (mutation.target && mutation.target.clientHeight !== this.height) {
          this.height = mutation.target.clientHeight
          this.$emit('footer-height', this.height)
        }
      }
    }
  }
</script>

<style scoped>
  
  [v-cloak] { display: none; }
  #footer {
    border: 1px solid #ddd;
    margin: 0;
    max-width: none;
    padding: 4px;
  } 
  .site-footer, .row {
    padding: 0;
    margin: 0;
  }
  .col {
    padding: 0 16px;
  }

</style>
