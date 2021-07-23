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
        
        loc = new Array([
            ["St Augustine's Abbey", [51.278128, 1.088206]],
            ["Canterbury", [51.278333, 1.0775]],
            ["Chartham", [51.255, 1.0205]]
        ])

        return loc
        /*
      return this.locations
        .filter(loc => loc.metadata && loc.metadata.coords)
        .map(loc => {
          if (!Array.isArray(loc.metadata.coords))
            loc.metadata.coords = loc.metadata.coords.split(',').map(coord => parseFloat(coord))
          return loc
        })
        */
    }
  },
  mounted() { this.loadDependencies(dependencies, 0, this.init) },
  methods: {

    init() {
      this.createMap()
      this.getLocations()
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

    getLocations() {
        text = document.getElementById('map-locations').innerText

        lines = text.split("\n")

        // Gets all names
        var names = lines.filter(function (el) {
            return (el.startsWith('name:'));
        });

        // Gets all coords
        var coords = lines.filter(function (el) {
            return (el.startsWith('coords:'));
        });

        var res = new Array()

        for (var i = 0; i < names.length; i++) {

            // Sanatise names and coords
            var name = names[i].replace('name: ', '')
            var coord = coords[i].replace('coords: ', '')

            // Split coords and convert to float
            var splitCoords = coord.split(', ')
            for (var j = 0; j < splitCoords.length; j++) {
                splitCoords[j] = +(splitCoords[j])
            }

            res[i] = [name, splitCoords]
        }
        
        return res
    },

    addMarkers() {
        locs = this.getLocations()

        console.log(locs)

        for (var i = 0; i < locs.length; i++) {
            L.marker(locs[i][1]).addTo(this.map).bindPopup(locs[i][0])
        }
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