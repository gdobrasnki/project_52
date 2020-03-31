var lonlat1
var flagtoUseCurrentLoc = false
var geolocation = new ol.Geolocation();
/**
    * Elements that make up the popup.
    */
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');


/**
 * Create an overlay to anchor the popup to the map.
 */
var overlay = new ol.Overlay({
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
});


/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function () {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};


function submitForm() {
    codeAddress(document.getElementById('id_address').value)

    // $.get("/addingcase/", {
    //     sqlParam: 'INSERT INT    O public.app_cases( name, telephone, "X", y, condition, age, sex, food_need, hygine_need, other_need, geom) VALUES (\'' + $('#id_name').val() + '\', \'' + $('#id_telephone').val() + '\', ' + parseFloat($('#id_X').val()) + ', ' + parseFloat($('#id_y').val()) + ',\'' + $('#id_condition').val() + '\', ' + parseInt($('#id_age').val()) + ', \'' + $('#id_sex').val() + '\', \'' + $('#id_food_need').val() + '\', \'' + $('#id_hygine_need').val() + '\', \'' + $('#other_need').val() + '\', ST_SetSRID( ST_Point(' + parseFloat($('#id_X').val()) + ',' + parseFloat($('#id_y').val()) + '), 3857));'
    // }, function (res) {
    //     console.log(red)
    // })
}

function unablePostalCode() {
    var inp = document.getElementById('div_id_postal_code')
    if (inp.style.display == 'none') {
        inp.style.display = 'block'
    } else {
        inp.style.display = 'none'
    }
}


function UseCurrentLoc() {
    if (flagtoUseCurrentLoc == false) {
        flagtoUseCurrentLoc = true
    } else {
        flagtoUseCurrentLoc = false
    }
    geolocation.setTracking(flagtoUseCurrentLoc)
}

; // here the browser may ask for confirmation
geolocation.on('change:position', function () {
    console.log(geolocation.getPosition());
    var coordinates = geolocation.getPosition();
    lonlat1 = ol.proj.transform(coordinates, 'EPSG:4326', 'EPSG:3857');

});
// base map 
var basemap = new ol.layer.Tile({
    source: new ol.source.OSM()
})
var geoserverLink = "http://localhost:8080/geoserver/"
var view = new ol.View
    ({
        // projection: 'EPSG:4326',
        zoom: 5,
        center: [-10993426.912371118, 4062679.713247195]
    })

var Centroids = new ol.source.ImageWMS({
    url: 'http://localhost:8080/geoserver/corona/wms',
    params: { 'LAYERS': '	corona:app_cases' },
    serverType: 'geoserver',
    // crossOrigin: 'anonymous'
});
var casesFeatures
$.getJSON('http://localhost:8080/geoserver/corona/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=corona%3Aapp_cases&outputFormat=application%2Fjson', function (data) {
    addCluster(data)
})
var postcodes = new ol.source.ImageWMS({
    url: 'http://localhost:8080/geoserver/corona/wms',
    params: { 'LAYERS': '	corona:postcodes' },
    serverType: 'geoserver',
    // crossOrigin: 'anonymous'
});
var postcodeslayers = new ol.layer.Image({
    source: postcodes
});
var litterLayer = new ol.layer.Image({
    source: Centroids
});

// The map
var map = new ol.Map({
    // controls: ol.control.defaults({
    //     attributionOptions: {
    //         collapsible: false
    //     }
    // }).extend([
    //     new app.drawFeatures()
    // ]),
    target: 'map',
    overlays: [overlay],
    // overlays: [popup],
    view: view,
    // interactions: ol.interaction.defaults(),
    layers: [basemap]
});


map.on('singleclick', function (evt) {
    var viewResolution = /** @type {number} */ (view.getResolution());
    var url = Centroids.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, 'EPSG:3857',
        { 'INFO_FORMAT': 'application/json' });
    if (url) {
        $.getJSON(url, function (data) {
            if (data.features.length != 0) {
                var properties = data.features[0].properties
                content.innerHTML = '<b> Name : </b> ' + properties['name'] +
                    '<br><b> Phone : </b> ' + properties['telephone'] +
                    '<br><b> Gender : </b> ' + properties['sex'] +
                    '<br><b> Age : </b> ' + properties['age']

                // addBadge('food_need','success')

                if (properties['food_need']) {
                    content.innerHTML += '<br><b> Food Needs : </b> '
                    var allfoods = properties['food_need'].split(',')
                    for (i = 0; i < allfoods.length; i++) {
                        if (allfoods[i] != 'undefined') {
                            content.innerHTML += '<span class="badge badge-success">' + allfoods[i] + '</span>'
                        }
                    }


                }
                if (properties['hygine_need']) {
                    content.innerHTML += '<br><b> Hygine Needs : </b> '
                    var allfoods = properties['hygine_need'].split(',')
                    for (i = 0; i < allfoods.length; i++) {
                        if (allfoods[i] != 'undefined') {

                            content.innerHTML += '<span class="badge badge-warning">' + allfoods[i] + '</span>'
                        }
                    }

                }
                if (properties['other_need']) {
                    content.innerHTML += '<br><b> other Needs : </b> '
                    var allfoods = properties['other_need'].split(',')
                    for (i = 0; i < allfoods.length; i++) {
                        if (allfoods[i] != 'undefined') {
                            content.innerHTML += '<span class="badge badge-info">' + allfoods[i] + '</span>'
                        }
                    }
                }
                content.innerHTML += '<button  class="urgent" onclick="urgentHelp()"> I can help in 4 Hours</button>'
                overlay.setPosition(evt.coordinate);
            }

        })
    }
});


function addCluster(data) {
    clusterSource.getSource().addFeatures((new ol.format.GeoJSON()).readFeatures(data));
}
// Addfeatures to the cluster
function addFeatures(nb) {
    var ext = map.getView().calculateExtent(map.getSize());
    var features = [];
    for (var i = 0; i < nb; ++i) {
        features[i] = new ol.Feature(new ol.geom.Point([ext[0] + (ext[2] - ext[0]) * Math.random(), ext[1] + (ext[3] - ext[1]) * Math.random()]));
        features[i].set('id', i);
    }
    clusterSource.getSource().clear();
    clusterSource.getSource().addFeatures(features);
}

// Style for the clusters
var styleCache = {};
function getStyle(feature, resolution) {
    var size = feature.get('features').length;
    var style = styleCache[size];
    if (!style) {
        var color = size > 25 ? "192,0,0" : size > 8 ? "255,128,0" : "0,128,0";
        var radius = Math.max(8, Math.min(size * 0.75, 20));
        var dash = 2 * Math.PI * radius / 6;
        var dash = [0, dash, dash, dash, dash, dash, dash];
        style = styleCache[size] = new ol.style.Style({
            image: new ol.style.Circle({
                radius: radius,
                stroke: new ol.style.Stroke({
                    color: "rgba(" + color + ",0.5)",
                    width: 15,
                    lineDash: dash,
                    lineCap: "butt"
                }),
                fill: new ol.style.Fill({
                    color: "rgba(" + color + ",1)"
                })
            }),
            text: new ol.style.Text({
                text: size.toString(),
                //font: 'bold 12px comic sans ms',
                //textBaseline: 'top',
                fill: new ol.style.Fill({
                    color: '#fff'
                })
            })
        });
    }
    return style;
}
// var vectorSource = new ol.source.Vector({
//     features: (new ol.format.GeoJSON()).readFeatures(geojsonObject)
// });

// Cluster Source
var clusterSource = new ol.source.Cluster({
    distance: 40,
    source: new ol.source.Vector()
});
// Animated cluster layer
var clusterLayer = new ol.layer.AnimatedCluster({
    name: 'Cluster',
    source: clusterSource,
    animationDuration: $("#animatecluster").prop('checked') ? 700 : 0,
    // Cluster style
    style: getStyle
});
map.addLayer(clusterLayer);
// add 2000 features
// addFeatures(2000);

// Style for selection
var img = new ol.style.Circle({
    radius: 5,
    stroke: new ol.style.Stroke({
        color: "rgba(0,255,255,1)",
        width: 1
    }),
    fill: new ol.style.Fill({
        color: "rgba(0,255,255,0.3)"
    })
});
var style0 = new ol.style.Style({
    image: img
});
var style1 = new ol.style.Style({
    image: img,
    // Draw a link beetween points (or not)
    stroke: new ol.style.Stroke({
        color: "#fff",
        width: 1
    })
});
// Select interaction to spread cluster out and select features
var selectCluster = new ol.interaction.SelectCluster({
    // Point radius: to calculate distance between the features
    pointRadius: 7,
    animate: $("#animatesel").prop('checked'),
    // Feature style when it springs apart
    featureStyle: function () {
        return [$("#haslink").prop('checked') ? style1 : style0]
    },
    // selectCluster: false,	// disable cluster selection
    // Style to draw cluster when selected
    style: function (f, res) {
        var cluster = f.get('features');
        if (cluster.length > 1) {
            var s = [getStyle(f, res)];
            if ($("#convexhull").prop("checked") && ol.coordinate.convexHull) {
                var coords = [];
                for (i = 0; i < cluster.length; i++) coords.push(cluster[i].getGeometry().getFirstCoordinate());
                var chull = ol.coordinate.convexHull(coords);
                s.push(new ol.style.Style({
                    stroke: new ol.style.Stroke({ color: "rgba(0,0,192,0.5)", width: 2 }),
                    fill: new ol.style.Fill({ color: "rgba(0,0,192,0.3)" }),
                    geometry: new ol.geom.Polygon([chull]),
                    zIndex: 1
                }));
            }
            return s;
        } else {
            return [
                new ol.style.Style({
                    image: new ol.style.Circle({
                        stroke: new ol.style.Stroke({ color: "rgba(0,0,192,0.5)", width: 2 }),
                        fill: new ol.style.Fill({ color: "rgba(0,0,192,0.3)" }),
                        radius: 5
                    })
                })];
        }
    }
});
map.addInteraction(selectCluster);
var geocoder = new google.maps.Geocoder();

function codeAddress(address) {
    geocoder.geocode({ address: address }, function (results, status) {
        if (status == "OK") {
            //center the map over the result
            //place a marker at the location

            document.getElementById('id_x').value = results[0].geometry.location["lng"]()
            document.getElementById('id_y').value = results[0].geometry.location["lat"]()
            document.getElementById('newLoca').submit()
        } else if (status == "ZERO_RESULTS") {
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: 'Enter different address',
                showConfirmButton: false,
                timer: 1500
            })
        }
    });
}