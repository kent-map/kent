<template>
  <v-card tile class="overflow-hidden">
    
    <v-navigation-drawer app v-if="nav.length > 0" v-model="drawer" style="z-index:201 !important;">
      <v-layout justify-space-between column fill-height>
        <v-list dense v-cloak>
          <v-list-item v-for="(menuItem, i) in nav" :key="i" @click="menuItemClicked(menuItem.path)" v-if="menuItem.enabled">
             <v-list-item-action><v-icon>{{menuItem.icon}}</v-icon></v-list-item-action>
              <v-list-item-content><v-list-item-title>{{menuItem.title}}</v-list-item-title></v-list-item-content>
          </v-list-item>
        </v-list>

        <v-list dense v-cloak justify-end>
          <v-divider></v-divider>

          <v-list-item><v-list-item-content>App version: {{appVersion}}</v-list-item-content></v-list-item>        
          <v-list-item><v-list-item-content>Lib version: {{libVersion}}</v-list-item-content></v-list-item>
          <v-divider></v-divider>
          <v-list-item v-if="siteConfig.branch !== 'master'">
            <span @click="drawer=false; editMarkdown('stackedit')" style="padding-right:18px; cursor:pointer;"><v-icon style="color:#ccc;">mdi-pencil-outline</v-icon></span>
          </v-list-item>
        </v-list> 
      </v-layout>
    </v-navigation-drawer>

    <v-app-bar
      id="header"
      v-mutate.attr="onMutate"
      app dark prominent
      elevate-on-scroll shrink-on-scroll
      elevation="6"
      :src="banner"
      :height="bannerHeight"
      scroll-target="#scrollableContent"
      :scroll-threshold="bannerHeight * 0.9"
      style="min-height: 104px;"
    >

      <v-app-bar-nav-icon large @click.stop="drawer = !drawer" style="padding:0; margin:6px 0 0 12px; z-index:100; background:rgba(0, 0, 0, .30);"></v-app-bar-nav-icon>

      <v-toolbar-title v-cloak>
        
        <v-container>
          
          <v-row style="margin-left:60px; height:100%;" no-gutters>

            <v-col cols="12" sm="9">
              <h3>{{title}}</h3>
              <p class="author" v-html="author"></p>
            </v-col>

            <v-col class="align-end" cols="12" sm="3" style="margin-top:6px; text-align:right;">
            </v-col>

          </v-row>

          <v-row>
            <v-col cols="12" sm="12" style="padding:3px; margin:0;">
            <v-progress-linear v-model="progress" height="7" color="#70CB2B"></v-progress-linear>
            </v-col>
          </v-row>

        </v-container>
      </v-toolbar-title>
    </v-app-bar>
  </v-card>
</template>

<script>
  module.exports = {
    props: {
      essayConfig: { type: Object, default: function(){ return {}} },
      siteConfig: { type: Object, default: function(){ return {}} },
      progress: { type: Number, default: 0 },
      nav: { type: Array, default: function(){ return []} },
      appVersion: { type: String },
      libVersion: { type: String }
    },    
    data: () => ({
      drawer: false,
      lastHeight: undefined
    }),
    computed: {
      essayConfigLoaded() { return this.essayConfig !== null },
      banner() { return this.essayConfigLoaded ? (this.essayConfig.banner || this.siteConfig.banner) : null },
      bannerHeight() { return this.essayConfig && this.essayConfig.bannerHeight || this.siteConfig.bannerHeight || 400 },
      title() { return this.essayConfigLoaded ? (this.essayConfig.title || this.siteConfig.title) : null },
      author() { return (this.essayConfigLoaded && this.essayConfig.author) || '&nbsp;' },
      numMaps() { return (this.essayConfigLoaded && this.essayConfig['num-maps']) },
      numImages() { return (this.essayConfigLoaded && this.essayConfig['num-images']) },
      numSpecimens() { return (this.essayConfigLoaded && this.essayConfig['num-specimens']) },
      numPrimarySources() { return (this.essayConfigLoaded && this.essayConfig['num-primary-sources']) },
      hasStats() { return this.numMaps || this.numImages || this.numSpecimens || this.numPrimarySources }
    },
    mounted() {
      document.getElementById('header').addEventListener('wheel', this.throttle(this.scrollContent, 40))
    },
    methods: {
      onMutate(mutations) {
        const mutation = mutations[mutations.length - 1]
        if (mutation.target && mutation.target.clientHeight !== this.lastHeight) {
          this.$emit('header-height', mutation.target.clientHeight)
          this.lastHeight = mutation.target.clientHeight
        }
      },
      menuItemClicked(file) {
        this.drawer = false
        this.$emit('menu-item-clicked', file)
      },
      viewMarkdown() {
        this.$emit('view-markdown')
      },
      editMarkdown(editor) {
        this.$emit('edit-markdown', editor)
      },
      throttle(callback, interval) {
        let enableCall = true
        return function(...args) {
          if (!enableCall) return
          enableCall = false
          callback.apply(this, args)
          setTimeout(() => enableCall = true, interval)
        }
      },
      scrollContent(e) {
        const wheelDelta = e.wheelDelta
        const scrollableContent = document.getElementById('scrollableContent')
        if (scrollableContent) {
          scrollableContent.scrollTo(0, scrollableContent.scrollTop - wheelDelta)
        }
      }
    }
  }
</script>

<style scoped>

  [v-cloak] { display: none; }

  #header {
    z-index: 200;
  }

  .v-toolbar__content {
    padding: 0;
  }

  .v-toolbar__title {
    width: 100%;
    color: white;
    background-color: rgba(0, 0, 0, .6);
    padding: 0 !important;
    position: absolute;
    top: calc(100% - 104px);
    min-height: 104px;
  }

  .v-toolbar__title h3 {
    font-size: 2.0rem;
    margin: 12px 0 6px 12px;
  }

  .v-toolbar__title .container {
    padding: 0;
    max-width: none;
  }

  .stats {
    font-size: 1.0rem !important;
    line-height: 1.2rem !important;
    margin-right: 20px !important;

  }

  .v-toolbar__image .v-image, .v-toolbar__content, #header {
    min-height: 104px!important;
  }

  .author {
    font-size: 1.25rem;
    margin: 6px 12px;
  }

</style>