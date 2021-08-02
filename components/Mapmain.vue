<template>
  <div id="map">
    test
  </div>
</template>

<script>


const dependencies = [
  'https://cdn.jsdelivr.net/npm/leaflet@1.5.1/dist/leaflet.css',
  'https://cdn.jsdelivr.net/npm/leaflet@1.5.1/dist/leaflet.js'
]

module.exports = {
  name: 'Map',
  props: {
    locations: {type: Array, default: () => ([])}
  },
  data: () => ({
    map: null
  }),
  computed: {
    locationsWithCoords() { 
      return this.locations
        .filter(loc => loc.metadata && loc.metadata.coords)
        .map(loc => {
          if (!Array.isArray(loc.metadata.coords))
            loc.metadata.coords = loc.metadata.coords.split(',').map(coord => parseFloat(coord))
          return loc
        })
    }
  },
  mounted() { this.loadDependencies(dependencies, 0, this.init) },
  methods: {

    init() {
      this.createMap()
      this.addMarkers()
    },

    createMap() {
      this.map = L.map('map', {
        center: [51.2119, 0.79756], 
        zoom: 10, 
        layers: [
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', 
                      { maxZoom: 18, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>' })
        ]
      })
    },

    addMarkers() {

      console.log("Adding markers")

      // More pins can be added here
      this.locations = [
        [[51.278128, 1.088206], "St Augustine's Abbey"],
        [[51.278333, 1.0775], "Canterbury"],
        [[51.255, 1.0205], "Chartham"],
        [[51.343911, 1.404031], "Ramsgate"],
        [[51.081389, 1.164722], "Folkestone"]
      ]


      console.log(this.locations)
      this.locations.forEach(loc => {
        L.marker(loc[0]).addTo(this.map).bindPopup(loc[1])
      })
    }

  },
  watch: {}
}

</script>

<style>

  #map {
    height: 100%;
  }

</style>