var lbcesium = jQuery('script[src*=lbcesium]');
var geojson_sat = lbcesium.attr('geojson_sat');
var geojson_gw = lbcesium.attr('geojson_gw');
var geojson_FOV_circle = lbcesium.attr('geojson_FOV_circle');
var geojson_TRSP_FOV = lbcesium.attr('geojson_TRSP_FOV');
var satellite_img = lbcesium.attr('satellite_img');
var ground_station_img = lbcesium.attr('ground_station_img');
var catapult_logo = lbcesium.attr('catapult_logo');
var performance_maxmin = lbcesium.attr('performance_maxmin');
var get_performance_json = lbcesium.attr('get_performance_json');
var json_subsatellite = lbcesium.attr('json_subsatellite');

Cesium.BingMapsApi.defaultKey = '***REMOVED***'
var viewer = new Cesium.Viewer('cesiumContainer', {
    timeline: false,
    animation: false,
    fullscreenButton: false,
    homeButton : false,
    geocoder: false

 });

// hue change binder
var viewModel = {
    perf_alpha: 0.6,
    hue_scale: 1.0  ,
    hue_preset: [1.0,0.9,0.8,0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
};
Cesium.knockout.track(viewModel);
var toolbar = document.getElementById('toolbar');
Cesium.knockout.applyBindings(viewModel, toolbar);


jQuery.getJSON(performance_maxmin, function(json) {
    maxminjson = json;
    EIRPmax = maxminjson["EIRP"]["max"][0]
    EIRPmin = maxminjson["EIRP"]["min"][0]
    ELEVATIONmin = maxminjson["ELEVATION"]["min"][0]
    ELEVATIONmax = maxminjson["ELEVATION"]["max"][0]
    SAT_GPTmin = maxminjson["SAT_GPT"]["min"][0]
    SAT_GPTmax = maxminjson["SAT_GPT"]["max"][0]
    SAT_GAIN_TXmin = maxminjson["SAT_GAIN_TX"]["min"][0]
    SAT_GAIN_TXmax = maxminjson["SAT_GAIN_TX"]["max"][0]
    SAT_GAIN_RXmin = maxminjson["SAT_GAIN_RX"]["min"][0]
    SAT_GAIN_RXmax = maxminjson["SAT_GAIN_RX"]["max"][0]
    DISTmin = maxminjson["DIST"]["min"][0]
    DISTmax = maxminjson["DIST"]["max"][0]
    FSL_UPmin = maxminjson["FSL_UP"]["min"][0]
    FSL_UPmax = maxminjson["FSL_UP"]["max"][0]
    FSL_DNmin = maxminjson["FSL_DN"]["min"][0]
    FSL_DNmax = maxminjson["FSL_DN"]["max"][0]
    SPEC_EFFmin = maxminjson["SPEC_EFF"]["min"][0]
    SPEC_EFFmax = maxminjson["SPEC_EFF"]["max"][0]
    CSN_TOTmin = maxminjson["CSN_TOT"]["min"][0]
    CSN_TOTmax = maxminjson["CSN_TOT"]["max"][0]
    CSN0_DNmin = maxminjson["CSN0_DN"]["min"][0]
    CSN0_DNmax = maxminjson["CSN0_DN"]["max"][0]
    CSI0_DNmin = maxminjson["CSI0_DN"]["min"][0]
    CSI0_DNmax = maxminjson["CSI0_DN"]["max"][0]
    LATmin = maxminjson["LAT"]["min"][0]
    LATmax = maxminjson["LAT"]["max"][0]
    LONmin = maxminjson["LON"]["min"][0]
    LONmax= maxminjson["LON"]["max"][0]


    //heatmap attempt
        var nuConfig = {
        radius: 40,
      maxOpacity: .5,
      minOpacity: 0,
      blur: .75,
        gradient: {                   // maybe try viridis
        '.3': 'blue',
        '.65': 'green',
        '.8': 'yellow',
        '.95': 'red'
        },
    };
    var instances = [EIRP_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    ELEVATION_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    SAT_GPT_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    DIST_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    FSL_UP_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    FSL_DN_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    SPEC_EFF_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    CSN_TOT_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    CSN0_DN_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig),
                    CSI0_DN_instance = CesiumHeatmap.create(viewer, {north:LATmax, east:LONmax, south:LATmin, west:LONmin}, nuConfig)]

    var heatmaps = instances
    jQuery.getJSON(get_performance_json, function(json) {
        features = json["features"];
        for(i=0;i<10;i++){
            heatmaps[i].data = []
            for(j=0; j<features.length; j++){
                lon = features[j].geometry.coordinates[0]
                lat = features[j].geometry.coordinates[1]
                if(i==0){heatmaps[i].values = features[j].properties.EIRP}
                if(i==1){heatmaps[i].values = features[j].properties.ELEVATION}
                if(i==2){heatmaps[i].values = features[j].properties.SAT_GPT}
                if(i==3){heatmaps[i].values = features[j].properties.DIST}
                if(i==4){heatmaps[i].values = features[j].properties.FSL_UP}
                if(i==5){heatmaps[i].values = features[j].properties.FSL_DN}
                if(i==6){heatmaps[i].values = features[j].properties.SPEC_EFF}
                if(i==7){heatmaps[i].values = features[j].properties.CSN_TOT}
                if(i==8){heatmaps[i].values = features[j].properties.CSN0_DN}
                if(i==9){heatmaps[i].values = features[j].properties.CSI0_DN}
                heatmaps[i].data.push({x:lon, y:lat, value:heatmaps[i].values})
            }
        if(i==0){
                instances[i].setWGS84Data(EIRPmax-30,EIRPmax, heatmaps[i].data)
            }
        if(i==1) {
            instances[i].setWGS84Data(ELEVATIONmin, ELEVATIONmax, heatmaps[i].data)
        }
        if(i==2){instances[i].setWGS84Data(SAT_GPTmin,SAT_GPTmax, heatmaps[i].data)
            }
        if(i==3){instances[i].setWGS84Data(DISTmin,DISTmax, heatmaps[i].data)
            }
        if(i==4) {
            instances[i].setWGS84Data(FSL_UPmin, FSL_UPmax, heatmaps[i].data)
        }
        if(i==5){instances[i].setWGS84Data(FSL_DNmin,FSL_DNmax, heatmaps[i].data)
            }
        if(i==6){instances[i].setWGS84Data(SPEC_EFFmin,SPEC_EFFmax, heatmaps[i].data)
            }
        if(i==7){instances[i].setWGS84Data(CSN_TOTmax-30,CSN_TOTmax, heatmaps[i].data)
            }
        if(i==8) {
            instances[i].setWGS84Data(CSN0_DNmin, CSN0_DNmax, heatmaps[i].data)
        }
        if(i==9) {
            instances[i].setWGS84Data(CSN0_DNmin, CSN0_DNmax, heatmaps[i].data)
        }
        instances[i].show(false)
        }
    });

    // little pop-up with the min and max values
    jQuery("#heatmap").change(function() {
        var el = jQuery(this);
        if (el.val() === "EIRP") {
            instances[0].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + EIRPmin.toFixed(2) + '<br>Max = ' + EIRPmax.toFixed(2) + '</p>')
        }
        else {
            instances[0].show(false)
        }
        if (el.val() === "Elevation") {
            instances[1].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + ELEVATIONmin.toFixed(2) + '<br>Max = ' + ELEVATIONmax.toFixed(2) + '</p>')
        }

        else {
            instances[1].show(false)
        }
        if (el.val() === "GPT") {
            instances[2].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + SAT_GPTmin.toFixed(2) + '<br>Max = ' + SAT_GPTmax.toFixed(2) + '</p>')
        }
        else {
            instances[2].show(false)
        }
        if (el.val() === "DIST") {
            instances[3].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + DISTmin.toFixed(2) + '<br>Max = ' + DISTmax.toFixed(2) + '</p>')
        }
        else {
            instances[3].show(false)
        }
        if (el.val() === "FSL_UP") {
            instances[4].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + FSL_UPmin.toFixed(2) + '<br>Max = ' + FSL_UPmax.toFixed(2) + '</p>')
        }
        else {
            instances[4].show(false)
        }
        if (el.val() === "FSL_DN") {
            instances[5].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + FSL_DNmin.toFixed(2) + '<br>Max = ' + FSL_DNmax.toFixed(2) + '</p>')
        }
        else {
            instances[5].show(false)
        }
        if (el.val() === "SPEC_EFF") {
            instances[6].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + SPEC_EFFmin.toFixed(2) + '<br>Max = ' + SPEC_EFFmax.toFixed(2) + '</p>')
        }
        else {
            instances[6].show(false)
        }
        if (el.val() === "CSN_TOT") {
            instances[7].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + CSN_TOTmin.toFixed(2) + '<br>Max = ' + CSN_TOTmax.toFixed(2) + '</p>')
        }
        else {
            instances[7].show(false)
        }
        if (el.val() === "CSN0_DN") {
            instances[8].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + CSN0_DNmin.toFixed(2) + '<br>Max = ' + CSN0_DNmax.toFixed(2) + '</p>')
        }

        else {
            instances[8].show(false)
        }
        if (el.val() === "CSI0_DN") {
            instances[9].show(true)
            jQuery('#minmax').replaceWith('<p id="minmax">Min = ' + CSN0_DNmin.toFixed(2) + '<br>Max = ' + CSN0_DNmax.toFixed(2) + '</p>')
        }
        else {
            instances[9].show(false)
        }
    })
});


var SAT = new Cesium.GeoJsonDataSource();
SAT.load(geojson_sat).then(function() {
    var entities = SAT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: satellite_img,
        });
    }
});

var SUBSAT = new Cesium.GeoJsonDataSource();
SUBSAT.load(json_subsatellite).then(function() {
    var entities = SUBSAT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.width = 1;
    }
});

var FOV_CIRCLE = new Cesium.GeoJsonDataSource();
FOV_CIRCLE.load(geojson_FOV_circle).then(function() {
    var entities = FOV_CIRCLE.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.loop = true;
        entity.polyline.material = Cesium.Color.BLACK;
        entity.polyline.width = .8; // lines get displayed properly with red strok
    }
});
var TRSP_FOV_CIRCLE = new Cesium.GeoJsonDataSource();
TRSP_FOV_CIRCLE.load(geojson_TRSP_FOV).then(function() {
    var entities = TRSP_FOV_CIRCLE.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.loop = true;
        entity.polyline.material = Cesium.Color.LIGHTGREY;
        entity.polyline.width = .8;
    }
});

var GW = new Cesium.GeoJsonDataSource();
GW.load(geojson_gw).then(function() {
    var entities = GW.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: ground_station_img,
        });
    }
});



//OLD performance points, useful for extracting each point individually
var EIRP = new Cesium.GeoJsonDataSource();
var ELEVATION = new Cesium.GeoJsonDataSource();
var SAT_GPT = new Cesium.GeoJsonDataSource();
var DIST = new Cesium.GeoJsonDataSource();
var FSL_UP = new Cesium.GeoJsonDataSource();
var FSL_DN = new Cesium.GeoJsonDataSource();
var SPEC_EFF = new Cesium.GeoJsonDataSource();
var CSN_TOT = new Cesium.GeoJsonDataSource();
var CSN0_DN = new Cesium.GeoJsonDataSource();
var CSI0_DN = new Cesium.GeoJsonDataSource();
var checkbox = document.getElementById('showVSATCheckbox');
jQuery("#performance").change(function() {
    var el = jQuery(this);
    checkbox.addEventListener('change', function() {
        if (el.val() === "EIRP") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(EIRP)) {
                    EIRP.load(get_performance_json).then(function() {
                        var entities = EIRP.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((EIRPmax - entity.properties.EIRP) / (EIRPmax - EIRPmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((EIRPmax - entities[i].properties.EIRP) / (EIRPmax - EIRPmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });
                    viewer.dataSources.add(EIRP);
                } else {
                        EIRP._entityCollection._show = true
                }
            }
        } else if (el.val() === "Elevation") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(ELEVATION)) {
                    ELEVATION.load(get_performance_json).then(function() {
                        var entities = ELEVATION.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((ELEVATIONmax - entity.properties.ELEVATION) / (ELEVATIONmax - ELEVATIONmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((ELEVATIONmax - entities[i].properties.ELEVATION) / (ELEVATIONmax - ELEVATIONmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });
                    viewer.dataSources.add(ELEVATION);
                } else {
                        ELEVATION._entityCollection._show = true
                }
            }
        } else if (el.val() === "GPT") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(SAT_GPT)) {
                    SAT_GPT.load(get_performance_json).then(function() {
                        var entities = SAT_GPT.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((SAT_GPTmax - entity.properties.SAT_GPT) / (SAT_GPTmax - SAT_GPTmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((SAT_GPTmax - entities[i].properties.SAT_GPT) / (SAT_GPTmax - SAT_GPTmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(SAT_GPT);
                } else {
                        SAT_GPT._entityCollection._show = true
                }
            }
        } else if (el.val() === "DIST") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(DIST)) {
                    DIST.load(get_performance_json).then(function() {
                        var entities = DIST.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((DISTmax - entity.properties.DIST) / (DISTmax - DISTmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((DISTmax - entities[i].properties.DIST) / (DISTmax - DISTmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(DIST);
                } else {
                        DIST._entityCollection._show = true
                }
            }
        } else if (el.val() === "FSL_UP") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(FSL_UP)) {
                    FSL_UP.load(get_performance_json).then(function() {
                        var entities = FSL_UP.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((FSL_UPmax - entity.properties.FSL_UP) / (FSL_UPmax - FSL_UPmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((FSL_UPmax - entities[i].properties.FSL_UP) / (FSL_UPmax - FSL_UPmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(FSL_UP);
                } else {
                        FSL_UP._entityCollection._show = true
                }
            }
        } else if (el.val() === "FSL_DN") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(FSL_DN)) {
                    FSL_DN.load(get_performance_json).then(function() {
                        var entities = FSL_DN.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((FSL_DNmax - entity.properties.FSL_DN) / (FSL_DNmax - FSL_DNmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((FSL_DNmax - entities[i].properties.FSL_DN) / (FSL_DNmax - FSL_DNmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(FSL_DN);
                } else {
                        FSL_DN._entityCollection._show = true
                }
            }
        } else if (el.val() === "SPEC_EFF") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(SPEC_EFF)) {
                    SPEC_EFF.load(get_performance_json).then(function() {
                        var entities = SPEC_EFF.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((SPEC_EFFmax - entity.properties.SPEC_EFF) / (SPEC_EFFmax - SPEC_EFFmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((SPEC_EFFmax - entities[i].properties.SPEC_EFF) / (SPEC_EFFmax - SPEC_EFFmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(SPEC_EFF);
                } else {
                        SPEC_EFF._entityCollection._show = true
                }
            }
        } else if (el.val() === "CSN_TOT") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(CSN_TOT)) {
                    CSN_TOT.load(get_performance_json).then(function() {
                        var entities = CSN_TOT.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((CSN_TOTmax - entity.properties.CSN_TOT) / (CSN_TOTmax - CSN_TOTmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((CSN_TOTmax - entities[i].properties.CSN_TOT) / (CSN_TOTmax - CSN_TOTmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });

                    viewer.dataSources.add(CSN_TOT);
                } else {
                        CSN_TOT._entityCollection._show = true
                }
            }
        } else if (el.val() === "CSN0_DN") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(CSN0_DN)) {
                    CSN0_DN.load(get_performance_json).then(function() {
                        var entities = CSN0_DN.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((CSN_TOTmax - entity.properties.CSN0_DN) / (CSN_TOTmax - CSN0_DNmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((CSN0_DNmax - entities[i].properties.CSN0_DN) / (CSN0_DNmax - CSN0_DNmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });
                    viewer.dataSources.add(CSN0_DN);
                } else {
                        CSN0_DN._entityCollection._show = true
                }
            }
        } else if (el.val() === "CSI0_DN") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(CSI0_DN)) {
                    CSI0_DN.load(get_performance_json).then(function() {
                        var entities = CSI0_DN.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.billboard = undefined;
                            entity.point = new Cesium.PointGraphics({
                                color: Cesium.Color.fromHsl(0.7*viewModel.hue_scale * ((CSI0_DNmax - entity.properties.CSI0_DN) / (CSI0_DNmax - CSI0_DNmin)), 1, .5, viewModel.perf_alpha),
                                pixelSize: 8,
                                outlineWidth: 0.5,
                                scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
                            })
                        }
                        Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
                            function(newValue) {
                                for (var i = 0; i < entities.length; i++) {
                                    entities[i].point.color = Cesium.Color.fromHsl(0.7*newValue * ((CSI0_DNmax - entities[i].properties.CSI0_DN) / (CSI0_DNmax - CSI0_DNmin)), 1, .5, viewModel.perf_alpha);
                                }
                            }
                        );
                    });
                    viewer.dataSources.add(CSI0_DN);
                } else {
                        CSI0_DN._entityCollection._show = true
                }
            }
        }
    }, false);
});
//
jQuery("#clear").click(function() {
    EIRP._entityCollection._show = false
    ELEVATION._entityCollection._show = false
    SAT_GPT._entityCollection._show = false
    DIST._entityCollection._show = false
    FSL_UP._entityCollection._show = false
    FSL_DN._entityCollection._show = false
    SPEC_EFF._entityCollection._show = false
    CSN_TOT._entityCollection._show = false
    CSN0_DN._entityCollection._show = false
    CSI0_DN._entityCollection._show = false
});
//
// jQuery('#centreCheckbox').click(function() {
//     viewer.zoomTo(SAT, new Cesium.HeadingPitchRange(40, -90, 9000000));
// });
//
jQuery("#screenshot").click(function() {
    // viewer.render();
    // screenshot = viewer.canvas.toDataURL("image/jpg", 0.2)
    // window.open(screenshot);
    var scene = viewer.scene;
    var canvas = viewer.canvas;
    canvas.setAttribute('tabindex', '0'); // needed to put focus on the canvas
    canvas.onclick = function() {
        canvas.focus();
    };
    var ellipsoid = scene.globe.ellipsoid;
    // disable the default event handlers
    scene.screenSpaceCameraController.enableRotate = false;
    scene.screenSpaceCameraController.enableTranslate = false;
    scene.screenSpaceCameraController.enableZoom = false;
    scene.screenSpaceCameraController.enableTilt = false;
    scene.screenSpaceCameraController.enableLook = false;
    var startMousePosition;
    var mousePosition;
    var flags = {
        looking : false,
        moveForward : false,
        moveBackward : false,
        moveUp : false,
        moveDown : false,
        moveLeft : false,
        moveRight : false
    };
    var handler = new Cesium.ScreenSpaceEventHandler(canvas);
    handler.setInputAction(function(movement) {
        flags.looking = true;
        mousePosition = startMousePosition = Cesium.Cartesian3.clone(movement.position);
    }, Cesium.ScreenSpaceEventType.LEFT_DOWN);
    handler.setInputAction(function(movement) {
        mousePosition = movement.endPosition;
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
    handler.setInputAction(function(position) {
        flags.looking = false;
    }, Cesium.ScreenSpaceEventType.LEFT_UP);
    function getFlagForKeyCode(keyCode) {
        switch (keyCode) {
        case 'W'.charCodeAt(0):
            return 'moveForward';
        case 'S'.charCodeAt(0):
            return 'moveBackward';
        case 'Q'.charCodeAt(0):
            return 'moveUp';
        case 'E'.charCodeAt(0):
            return 'moveDown';
        case 'D'.charCodeAt(0):
            return 'moveRight';
        case 'A'.charCodeAt(0):
            return 'moveLeft';
        default:
            return undefined;
        }
    }
    document.addEventListener('keydown', function(e) {
        var flagName = getFlagForKeyCode(e.keyCode);
        if (typeof flagName !== 'undefined') {
            flags[flagName] = true;
        }
    }, false);
    document.addEventListener('keyup', function(e) {
        var flagName = getFlagForKeyCode(e.keyCode);
        if (typeof flagName !== 'undefined') {
            flags[flagName] = false;
        }
    }, false);
    viewer.clock.onTick.addEventListener(function(clock) {
        var camera = viewer.camera;
        if (flags.looking) {
            var width = canvas.clientWidth;
            var height = canvas.clientHeight;
            // Coordinate (0.0, 0.0) will be where the mouse was clicked.
            var x = (mousePosition.x - startMousePosition.x) / width;
            var y = -(mousePosition.y - startMousePosition.y) / height;
            var lookFactor = 0.05;
            camera.lookRight(x * lookFactor);
            camera.lookUp(y * lookFactor);
        }
        // Change movement speed based on the distance of the camera to the surface of the ellipsoid.
        var cameraHeight = ellipsoid.cartesianToCartographic(camera.position).height;
        var moveRate = cameraHeight / 100.0;
        if (flags.moveForward) {
            camera.moveForward(moveRate);
        }
        if (flags.moveBackward) {
            camera.moveBackward(moveRate);
        }
        if (flags.moveUp) {
            camera.moveUp(moveRate);
        }
        if (flags.moveDown) {
            camera.moveDown(moveRate);
        }
        if (flags.moveLeft) {
            camera.moveLeft(moveRate);
        }
        if (flags.moveRight) {
            camera.moveRight(moveRate);
        }
    });


});

var credit = new Cesium.Credit('Catapult', catapult_logo, 'http://sa.catapult.org.uk');
viewer.scene.frameState.creditDisplay.addDefaultCredit(credit);
