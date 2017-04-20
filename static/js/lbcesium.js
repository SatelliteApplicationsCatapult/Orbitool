var lbcesium = $('script[src*=lbcesium]');
var get_performance_json = lbcesium.attr('get_performance_json');
var geojson_sat = lbcesium.attr('geojson_sat');
var geojson_gw = lbcesium.attr('geojson_gw');
var geojson_FOV = lbcesium.attr('geojson_FOV');
var geojson_FOV_circle = lbcesium.attr('geojson_FOV_circle');
var geojson_TRSP_FOV = lbcesium.attr('geojson_TRSP_FOV');
var satellite_img = lbcesium.attr('satellite_img');
var ground_station_img = lbcesium.attr('ground_station_img');
var catapult_logo = lbcesium.attr('catapult_logo');
var performance_maxmin = lbcesium.attr('performance_maxmin');
var json_subsatellite = lbcesium.attr('json_subsatellite');

var viewer = new Cesium.Viewer('cesiumContainer', {
    timeline: false,
    animation: false
});

var viewModel = {
    FOVcolors: Cesium.knockout.observable(['735078', '3c8d87', 'd26f52', '923d50', 'FFFFFF', '000000', 'adadad']),
    FOVcolor: "735078",
    FOValpha: "42",
    perf_alpha: 0.6,
    hue_scale: 1.0,
    hue_preset: [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
};
Cesium.knockout.track(viewModel);
var toolbar = document.getElementById('toolbar');
Cesium.knockout.applyBindings(viewModel, toolbar);

$.getJSON(performance_maxmin, function(json) {
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
    EFFICIENCYmin = maxminjson["EFFICIENCY"]["min"][0]
    EFFICIENCYmax = maxminjson["EFFICIENCY"]["max"][0]
});

var EIRP = new Cesium.GeoJsonDataSource();
EIRP.load(get_performance_json).then(function() {
    var entities = EIRP.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromHsl(viewModel.hue_scale * ((entity.properties.EIRP - EIRPmin) / (EIRPmax - EIRPmin)), 1, .5, viewModel.perf_alpha),
            pixelSize: 8,
            outlineWidth: 0.5,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        })
    }
    Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].point.color = Cesium.Color.fromHsl(newValue * ((entities[i].properties.EIRP - EIRPmin) / (EIRPmax - EIRPmin)), 1, .5, viewModel.perf_alpha);
            }
        }
    );
});
var ELEVATION = new Cesium.GeoJsonDataSource();
ELEVATION.load(get_performance_json).then(function() {
    var entities = ELEVATION.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromHsl(((entity.properties.ELEVATION - ELEVATIONmin) / (ELEVATIONmax - ELEVATIONmin)), 1, .5, viewModel.perf_alpha),
            pixelSize: 8,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        })
    }
    Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].point.color = Cesium.Color.fromHsl(newValue * ((entities[i].properties.ELEVATION - ELEVATIONmin) / (ELEVATIONmax - ELEVATIONmin)), 1, .5, viewModel.perf_alpha);
            }
        }
    );
});
var SAT_GPT = new Cesium.GeoJsonDataSource();
SAT_GPT.load(get_performance_json).then(function() {
    var entities = SAT_GPT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromHsl(((entity.properties.SAT_GPT - SAT_GPTmin) / (SAT_GPTmax - SAT_GPTmin)), 1, .5, viewModel.perf_alpha),
            pixelSize: 8,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        });
    }
    Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].point.color = Cesium.Color.fromHsl(newValue * ((entities[i].properties.SAT_GPT - SAT_GPTmin) / (SAT_GPTmax - SAT_GPTmin)), 1, .5, viewModel.perf_alpha);
            }
        }
    );
});

var DIST = new Cesium.GeoJsonDataSource();
DIST.load(get_performance_json).then(function() {
    var entities = DIST.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromHsl(((entity.properties.DIST - DISTmin) / (DISTmax - DISTmin)), 1, .5, viewModel.perf_alpha),
            pixelSize: 8,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        });
    }
    Cesium.knockout.getObservable(viewModel, 'hue_scale').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].point.color = Cesium.Color.fromHsl(newValue * ((entities[i].properties.DIST - DISTmin) / (DISTmax - DISTmin)), 1, .5, viewModel.perf_alpha);
            }
        }
    );
});






var GW = new Cesium.GeoJsonDataSource();
GW.load(geojson_gw).then(function() {
    var entities = GW.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: ground_station_img, //This image ships with cesium I believe
        });
    }
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
    var entities = FOV_CIRCLE.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.width = 1;
    }
});


var FOV = new Cesium.GeoJsonDataSource();
FOV.load(geojson_FOV).then(function() {
    var entities = FOV.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.cylinder = new Cesium.CylinderGraphics({
            length: entities[i].properties.Height * 1000,
            topRadius: 0,
            bottomRadius: entity.properties.BottomRadius,
            outlineWidth: 2,
            outline: true,
            numberOfVerticalLines: 0,
            material: Cesium.Color.fromRgba(["0x"] + [viewModel.FOValpha] + [viewModel.FOVcolor]),
        });
    }
    Cesium.knockout.getObservable(viewModel, 'FOVcolor').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].cylinder.material = Cesium.Color.fromRgba(["0x"] + [viewModel.FOValpha] + [newValue]);
            }
        }
    );
    Cesium.knockout.getObservable(viewModel, 'FOValpha').subscribe(
        function(newValue) {
            for (var i = 0; i < entities.length; i++) {
                entities[i].cylinder.material = Cesium.Color.fromRgba(["0x"] + [newValue] + [viewModel.FOVcolor]);
            }

        }
    );
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

var checkbox1 = document.getElementById('showSATCheckbox');
checkbox1.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox1.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(SAT)) {
            viewer.dataSources.add(SAT);
            // viewer.zoomTo(SAT, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(SAT)) {
            viewer.dataSources.remove(SAT);
        }
    }
}, false);
var checkboxline = document.getElementById('showLineCheckbox');
checkboxline.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkboxline.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(SUBSAT)) {
            viewer.dataSources.add(SUBSAT);
            // viewer.zoomTo(SAT, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(SUBSAT)) {
            viewer.dataSources.remove(SUBSAT);
        }
    }
}, false);
var checkbox2 = document.getElementById('showGWCheckbox');
checkbox2.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox2.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(GW)) {
            viewer.dataSources.add(GW);
            //viewer.zoomTo(GW, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(GW)) {
            viewer.dataSources.remove(GW);
        }
    }
}, false);

var checkbox4 = document.getElementById('showFOVCheckbox');
checkbox4.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox4.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(FOV)) {
            viewer.dataSources.add(FOV);
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(FOV)) {
            viewer.dataSources.remove(FOV);
        }
    }
}, false);

var checkbox5 = document.getElementById('centreCheckbox');
checkbox5.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox5.checked) {
        viewer.zoomTo(SAT, new Cesium.HeadingPitchRange(40, -90, 9000000));
    }
}, false);

var checkbox6 = document.getElementById('showTRSPCheckbox');
checkbox6.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox6.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(TRSP_FOV_CIRCLE)) {
            viewer.dataSources.add(TRSP_FOV_CIRCLE);
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(TRSP_FOV_CIRCLE)) {
            viewer.dataSources.remove(TRSP_FOV_CIRCLE);
        }
    }
}, false);

var checkbox8 = document.getElementById('showFOVCIRCLECheckbox');
checkbox8.addEventListener('change', function() {
    // Checkbox state changed.
    if (checkbox8.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(FOV_CIRCLE)) {
            viewer.dataSources.add(FOV_CIRCLE);
            // viewer.zoomTo(ELEVATION, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(FOV_CIRCLE)) {
            viewer.dataSources.remove(FOV_CIRCLE);
        }
    }
}, false);


var checkbox = document.getElementById('showVSATCheckbox');
$("#performance").change(function() {

    var el = $(this);
    checkbox.addEventListener('change', function() {
        if (el.val() === "EIRP") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(EIRP)) {
                    viewer.dataSources.add(EIRP);

                }
            }
        } else if (el.val() === "Elevation") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(ELEVATION)) {
                    viewer.dataSources.add(ELEVATION);
                }
            }
        } else if (el.val() === "GPT") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(SAT_GPT)) {
                    viewer.dataSources.add(SAT_GPT);
                }
            }
        }
        else if (el.val() === "DIST") {
            if (checkbox.checked) {
                if (!viewer.dataSources.contains(DIST)) {
                    viewer.dataSources.add(DIST);
                }
            }
        }
    }, false);
});

$("#clear").click(function() {
  viewer.dataSources.remove(EIRP);
  viewer.dataSources.remove(ELEVATION);
  viewer.dataSources.remove(SAT_GPT);
  viewer.dataSources.remove(DIST);
});

$("#screenshot").click(function() {
    viewer.render();
    window.open(viewer.canvas.toDataURL("image/png"));
});

viewer.zoomTo(EIRP, new Cesium.HeadingPitchRange(40, -90, 9000000));
var credit = new Cesium.Credit('Catapult', catapult_logo, 'http://sa.catapult.org.uk');
viewer.scene.frameState.creditDisplay.addDefaultCredit(credit);
