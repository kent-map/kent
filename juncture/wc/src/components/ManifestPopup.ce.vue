<template>

  <div ref="root" >
    <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 512 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M256 512A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM216 336h24V272H216c-13.3 0-24-10.7-24-24s10.7-24 24-24h48c13.3 0 24 10.7 24 24v88h8c13.3 0 24 10.7 24 24s-10.7 24-24 24H216c-13.3 0-24-10.7-24-24s10.7-24 24-24zm40-208a32 32 0 1 1 0 64 32 32 0 1 1 0-64z"/></svg>
  </div>

</template>
  
<script setup lang="ts">

  import { computed, ref, watch } from 'vue'
  import tippy from 'tippy.js'

  const props = defineProps({
    manifest: { type: String }
  })

  const root = ref<HTMLElement | null>(null)
  const host = computed(() => (root.value?.getRootNode() as any)?.host)

  watch(host, () => { 
    tippy(host.value, {
      theme: 'light-border',
      allowHTML: true,
      interactive: true,
      appendTo: document.body,
      placement: 'bottom-end',
      arrow: true,
      delay: [null, null],
      // content: `<ve-entity-card qid="Q5582"></ve-entity-card>`
      // content: '<div style="background-color:white;padding:12px;">Hello</div>',
      // content: `<ve-manifest manifest="${manifest.value.id}"></ve-manifest>`
      onShow: (instance:any) => instance.setContent(`<div class="manifest-popup"><ve-manifest manifest="${props.manifest}"></ve-manifest></div>`)
    })
  })

</script>

<style>

  #tippy {
      width: 24px;
      height: 24px;
      font-size: 20px;
      border: 2px solid rgba(255, 255, 255, 0.8);
      border-radius: 50%;
      background-color: white;
      display: flex;
      justify-content: center;
    }

</style>