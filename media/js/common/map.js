var SchoolMap = {

    // projections
    epsg4326: new OpenLayers.Projection("EPSG:4326"),
    epsg900913: new OpenLayers.Projection("EPSG:900913"),
        
    options: {
        cloudmadeStyle: '16915',
        schoolsUrl: '/schools/geojson',

        detailView: false,
        hover: true,
        mobile: false,
        popups: true,
        select: true,

        addContentToPopup: function(popup, feature) { ; },
        onLoad: function() {},
        onFeatureSelect: function(feature) {},
        onFeatureUnselect: function(feature) {},
        onFeatureHighlight: function(feature) {},
        onFeatureUnhighlight: function(feature) {},

        id: null,
        boroughs: null,
        types: null,

        defaultZoom: 10,
        idZoom: 14,
        center: new OpenLayers.LonLat(-8234025.992578148, 4971255.355311619),
        initialZoom: 11,
    },

    defaultStyle: new OpenLayers.StyleMap({
        'default': new OpenLayers.Style({
            pointRadius: 4,
            fillColor: "#ff7800",
            fillOpacity: 0.8,
            strokeWidth: 0,
        }),
        'select': {
            pointRadius: 15,
        },
        'temporary': {
            pointRadius: 15,
        },
    }),

    mobileStyle: new OpenLayers.StyleMap({
        'default': new OpenLayers.Style({
             pointRadius: 10,
             fillColor: '#ff7800',
             fillOpacity: 0.8,
             strokeWidth: 0,
        }),
        'select': {
            pointRadius: 20,
        },
        'temporary': {
            pointRadius: 20,
        },
    }),

    gardenToCafeStyle: {
        fillColor: '#0F0',
    },

    wellnessInTheSchoolsStyle: {
        fillColor: '#F00',
    },


    init: function(options, elem) {
        this.options = $.extend({}, this.options, options);
        this.elem = elem;
        this.$elem = $(elem);

        this.style = this.defaultStyle;
        if (this.options.mobile) {
            this.style = this.mobileStyle;
        }
        this.addRulesToStyle(this.style.styles['default']);

        // create map
        var t = this;
        var controls = [ 
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.Attribution(),
            new OpenLayers.Control.LoadingPanel(),
        ];
        if (!t.options.detailView) {
            controls.push(new OpenLayers.Control.ZoomPanel());
        }
        this.olMap = new OpenLayers.Map(this.$elem.attr('id'), {
            controls: controls,
            restrictedExtent: this.createBBox(-74.319, 40.948, -73.584, 40.476), 
            zoomToMaxExtent: function() {   
                this.setCenter(t.options.center, t.options.initialZoom);
            },
            isValidZoomLevel: function(zoomLevel) {
                return (zoomLevel > 9 && zoomLevel < this.getNumZoomLevels());
            }                  
        });

        var cloudmade = new OpenLayers.Layer.CloudMade("CloudMade", {
            key: '781b27aa166a49e1a398cd9b38a81cdf',
            styleId: this.options.cloudmadeStyle,  
            transitionEffect: 'resize',     
        });
        this.olMap.addLayer(cloudmade); 
        this.olMap.zoomToMaxExtent();   
                                
        this.school_layer = this.getLayer('schools', this.buildUrl());
        this.school_layer.events.on({
            'loadend': function() {
                t.options.onLoad();
                if (t.options.detailView) {
                    t.centerOnFeature(t.school_layer, t.options.detailFid);
                }
                else {
                    t.addControls([t.school_layer]);
                }
            },
        });
        return this;
    },


    getLayer: function(name, url) {
        var layer = new OpenLayers.Layer.Vector(name, {
            projection: this.olMap.displayProjection,
            strategies: [
                new OpenLayers.Strategy.Fixed(),
            ],
            styleMap: this.style,
            protocol: new OpenLayers.Protocol.HTTP({
                url: url,
                format: new OpenLayers.Format.GeoJSON()
            })
        });
        this.olMap.addLayer(layer);
        return layer;
    },


    buildUrl: function() {
        var url = this.options.schoolsUrl + '?';
        if (this.options.id !== null) {
            url += 'id=' + this.options.id;
        }
        if (this.options.boroughs !== null) {
            url += 'boroughs=' + this.options.boroughs + '&';
        }
        if (this.options.types !== null) {
            url += 'types=' + this.options.types + '&';
        }
        return url;
    },


    addControls: function(layers) {
        var t = this;
        if (t.options.hover) {
            this.hoverControl = this.getControlHoverFeature(layers);
        }
        if (t.options.select) {
            this.selectControl = this.getControlSelectFeature(layers);
        }
    },


    getControlHoverFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers, {
            hover: true,
            highlightOnly: true,
            renderIntent: 'temporary',
        });
        selectControl.events.on({
            'featurehighlighted': this.options.onFeatureHighlight,
            'featureunhighlighted': this.options.onFeatureUnhighlight,
        });
        this.olMap.addControl(selectControl);
        selectControl.activate();
        return selectControl;
    },

    getControlSelectFeature: function(layers) {
        var selectControl = new OpenLayers.Control.SelectFeature(layers);
        var t = this;

        $.each(layers, function(i, layer) {
            layer.events.on({
                "featureselected": function(event) {
                    if (t.options.popups) {
                        var feature = event.feature;
                        var popup = t.createAndOpenPopup(feature);
                        t.addContentToPopup(popup, feature);
                    }
                    t.options.onFeatureSelect(feature);
                },
                "featureunselected": function(event) {
                    var feature = event.feature;
                    if(t.options.popups && feature.popup) {
                        t.olMap.removePopup(feature.popup);
                        t.options.onFeatureUnselect(feature);
                        feature.popup.destroy();
                        delete feature.popup;
                    }
                },
            });
        });
        this.olMap.addControl(selectControl);
        selectControl.activate();
        return selectControl;
    },

    addContentToPopup: function(popup, feature) {
        $content = $(popup).find('div');
        $content
            .append('<h2><a href="/schools/' + feature.fid + '/">' + feature.data.name + '</a></h2>')
            .append('<div class="address">' + feature.data.address + '</div>');
        if (feature.data.participates_in_wellness_in_the_schools) {
            $content.append('<div class="participation">Participates in <a href="http://www.wellnessintheschools.org/" target="_blank">Wellness in the Schools</a></div>');
        }
        if (feature.data.participates_in_garden_to_cafe) {
            $content.append('<div class="participation">Participates in <a href="http://growtolearn.org/view/DP5619" target="_blank">Garden to Cafe</a></div>');
        }
    },

    createAndOpenPopup: function(feature) {
        var t = this;

        var popup_width = 250;
        var map_width = t.$elem.innerWidth();
        var max_width = map_width - 65;
        if (popup_width > max_width) popup_width = max_width;
        var content_div_width = popup_width;

        var popup_height = 100;
        var map_height = t.$elem.innerHeight();
        var max_height = map_height - 65;
        if (popup_height > max_height) popup_height = max_height;
        var content_div_height = popup_height - 50;

        var content = "<div style=\"width: " + content_div_width + "px !important; min-height: " + content_div_height + "px;\"></div>";
        var popup = new OpenLayers.Popup.Anchored("chicken",
            feature.geometry.getBounds().getCenterLonLat(),
            new OpenLayers.Size(popup_width, popup_height),
            content,
            null,
            true,
            function(event) { t.selectControl.unselectAll(); }
        );
        popup.panMapIfOutOfView = true;
        feature.popup = popup;
        this.olMap.addPopup(popup);

        // don't let the close box add whitespace to the popup
        $('.olPopupContent').width($('.olPopupContent').width() + 20);
        return $('#chicken_contentDiv');
    },

    createBBox: function(lon1, lat1, lon2, lat2) {
        var b = new OpenLayers.Bounds();
        b.extend(this.getTransformedLonLat(lon1, lat1));
        b.extend(this.getTransformedLonLat(lon2, lat2));
        return b;
    },

    getTransformedLonLat: function(longitude, latitude) {
        return new OpenLayers.LonLat(longitude, latitude).transform(this.epsg4326, this.epsg900913);
    },

    // Add style rule to check for gardens and style them differently
    addRulesToStyle: function(style) {
        var rules = [];

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'participates_in_garden_to_cafe',
                value: true,
            }),
            symbolizer: this.gardenToCafeStyle,
        }));

        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: 'participates_in_wellness_in_the_schools',
                value: true,
            }),
            symbolizer: this.wellnessInTheSchoolsStyle,
        }));

        /*
        rules.push(new OpenLayers.Rule({
            filter: new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.NOT_EQUAL_TO,
                property: 'recent_change',
                value: null,
            }),
            symbolizer: this.recentChangesStyle,
        }));
        */

        if (this.options.mobile) {
            rules.push(new OpenLayers.Rule({
                minScaleDenominator: 100000,
                symbolizer: {
                    pointRadius: 3,
                },
            }));
        }

        rules.push(new OpenLayers.Rule({
            elseFilter: true,
        }));

        style.addRules(rules);
    },

    centerOnFeature: function(layer, fid) {
        var feature = layer.getFeatureByFid(fid);
        if (!feature) return;

        var l = new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y);
        this.olMap.setCenter(l, 15);
    },


};

$.plugin('schoolmap', SchoolMap);
