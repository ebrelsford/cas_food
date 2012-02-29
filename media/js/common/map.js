var SchoolMap = {
    options: {
        cloudmadeStyle: '16915',
        schoolsUrl: '/schools/geojson',

        id: null,

        defaultCenter: new L.LatLng(40.712, -73.9515),
        defaultZoom: 10,
        idZoom: 14,
    },

    schoolStyle: {
        radius: 8,
        fillColor: "#ff7800",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8,
    },

    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);

        // create map
        this.map = new L.Map('map');
        var cloudmadeUrl = 'http://{s}.tile.cloudmade.com/781b27aa166a49e1a398cd9b38a81cdf/' + this.options.cloudmadeStyle + '/256/{z}/{x}/{y}.png',
            cloudmadeAttrib = 'Map data &copy; 2012 OpenStreetMap contributors, Imagery &copy; 2012 CloudMade',
            cloudmade = new L.TileLayer(cloudmadeUrl, {maxZoom: 18, attribution: cloudmadeAttrib});

        // set view
        this.map.setView(this.options.defaultCenter, this.options.defaultZoom).addLayer(cloudmade);

        // add schools
        this.schoolsLayer = this.loadSchools();

        return this;
    },

    loadSchools: function() {
        var t = this;

        // initialize layer
        var layer = new L.GeoJSON(null, {
            pointToLayer: function(latLng) {
                return new L.CircleMarker(latLng, t.schoolStyle);
            },   
        });
        layer.on('featureparse', function(f) {
            if (t.options.id !== null) {
                t.map.setView(f.layer._latlng, t.options.idZoom);
            }
            var content = f.properties.name + ' <a href="/schools/' + f.id + '/"><img src="/media/images/info.png" /></a>';
            f.layer.bindPopup(content);
        });

        // build url
        var url = this.options.schoolsUrl + '?';
        if (this.options.id !== null) {
            url += 'id=' + this.options.id;
        }

        // load GeoJSON from url, add to map
        $.getJSON(url, function(data) {
            layer.addGeoJSON(data);
        });
        this.map.addLayer(layer);
        return layer;
    }
};

$.plugin('schoolmap', SchoolMap);
