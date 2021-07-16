<template>
  <div id="footer" :style="`max-width:${maxWidth}px; overflow:hidden;`">
        <a href = "https://twitter.com/cccu_humanities"><img :src="`${assetsBase}/images/twitter.png`" height="30px"></a>
    <span style="padding-bottom: 8px; font-weight: bold; display: block">A collaboration between:</span>
    <img :src="`${assetsBase}/dickens/images/CCCU-logo-2colour.svg`" style="height:30px;"> &nbsp;&nbsp;&nbsp;&nbsp;
    <img :src="`${assetsBase}/images/labs.jpg`" height="30px">
  </div>
</template>

<script>

  module.exports = {  
    name: 'Footer',
    props: {
      siteConfig: { type: Object, default: function(){ return {}} },
      contentSource:  { type: Object, default: () => ({}) }
    },
    data: () => ({}),
    computed: {
      maxWidth() { return window.innerWidth },
      assetsBase() { return this.contentSource.assetsBaseUrl }
    },
    mounted() {},
    methods: {},
    watch: {}
  }

</script>

<style>
  
  [v-cloak] { display: none; }

  #footer {
    font-family: Roboto, sans-serif;
    display: flex;
    align-items: center;
    height: 50px;
    font-size: .8rem;
    font-weight: bold;
    padding-left: 20px;
  } 
  #footer img {
    height: 30px;
    margin: 0 12px;
  }

</style>
