var lbcesium = $('script[src*=lbcesium]');
var geo_json_vsat = lbcesium.attr('geo_json_vsat');
var geojson_sat = lbcesium.attr('geojson_sat');
var geojson_gw = lbcesium.attr('geojson_gw');
var geojson_FOV = lbcesium.attr('geojson_FOV');
var geojson_FOV_circle = lbcesium.attr('geojson_FOV_circle');
var geojson_TRSP_FOV = lbcesium.attr('geojson_TRSP_FOV');
var satellite_img = lbcesium.attr('satellite_img');
var ground_station_img = lbcesium.attr('ground_station_img');

var viewer = new Cesium.Viewer('cesiumContainer', {
    timeline: false,
    animation: false
});
var viewModel = {
    EIRPmin: 31.1984391831,
    ELEVATIONmin: 57,
    SAT_GPTmin: 1.6,
    Tmin: 282  //need to write a function to determin minimum temperature
};

var VSAT = new Cesium.GeoJsonDataSource();
VSAT.load(geo_json_vsat).then(function () {
    var entities = VSAT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            //color: Cesium.Color.fromBytes((((entity.properties.EIRP-viewModel.EIRPmin)))*80.875,0,(1/(entity.properties.EIRP-viewModel.EIRPmin))*320.875,210),
            color: Cesium.Color.fromBytes(0,((1/(entity.properties.EIRP-viewModel.EIRPmin)))*400.875,(entity.properties.EIRP-viewModel.EIRPmin)*120.875,210),
            //color: Cesium.Color.fromBytes((entity.properties.EIRP-viewModel.Tmin)*20.875,0,((1/(entity.properties.EIRP-viewModel.Tmin)))*540.875,210),  //currently plots temperature
            pixelSize: 8,
            outlineWidth: .5,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
            //translucencyByDistance : new Cesium.NearFarScalar(.6e7, 1,1.2e7, 0.01),
            //The artifacts you're seeing are called "z-fighting", which is a common problem in 3D rendering when multiple polygons are rendered at the same depth and the depth buffer can't distinguish them.
        })
    }
});
var ELEVATION = new Cesium.GeoJsonDataSource();
ELEVATION.load(geo_json_vsat).then(function () {
    var entities = ELEVATION.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromBytes((((entity.properties.ELEVATION - viewModel.ELEVATIONmin))) * 5.875, 0, (1 / (entity.properties.ELEVATION - viewModel.ELEVATIONmin)) * 3020.875, 210),
            pixelSize: 8,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        })
    }
});
var SAT_GPT = new Cesium.GeoJsonDataSource();
SAT_GPT.load(geo_json_vsat).then(function () {
    var entities = SAT_GPT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.point = new Cesium.PointGraphics({
            color: Cesium.Color.fromBytes(0, ((entity.properties.SAT_GPT - viewModel.SAT_GPTmin)) * 220.875, 0, 210),
            pixelSize: 8,
            scaleByDistance: new Cesium.NearFarScalar(.3e7, 1, 3.5e7, 0.01),
        })
    }
});
var GW = new Cesium.GeoJsonDataSource();
GW.load(geojson_gw).then(function () {
    var entities = GW.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: ground_station_img, //This image ships with cesium I believe
        })
    }
});
var SAT = new Cesium.GeoJsonDataSource();
SAT.load(geojson_sat).then(function () {
    var entities = SAT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: satellite_img,
        })
    }
});
var FOV = new Cesium.GeoJsonDataSource();
FOV.load(geojson_FOV).then(function () {
    var entities = FOV.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = undefined;
        entity.cylinder = new Cesium.CylinderGraphics({
            length: entity.properties.Height * 1000,
            topRadius: 0,
            bottomRadius: entity.properties.BottomRadius,
            outlineWidth: 2,
            outline: true,
            numberOfVerticalLines: 0,
            material: Cesium.Color.fromRandom({alpha: 0.25}),
        })
    }
});
var FOV_CIRCLE = new Cesium.GeoJsonDataSource();
FOV_CIRCLE.load(geojson_FOV_circle).then(function () {
    var entities = FOV_CIRCLE.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.loop = true;
        entity.polyline.material = Cesium.Color.BLACK;
        entity.polyline.width = .8;// lines get displayed properly with red strok
    }
});
var TRSP_FOV_CIRCLE = new Cesium.GeoJsonDataSource();
TRSP_FOV_CIRCLE.load(geojson_TRSP_FOV).then(function () {
    var entities = TRSP_FOV_CIRCLE.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.polyline.loop = true;
        entity.polyline.material = Cesium.Color.LIGHTGREY;
        entity.polyline.width = .8;
    }
});

var checkbox = document.getElementById('showVSATCheckbox');
checkbox.addEventListener('change', function () {
    // Checkbox state changed.
    if (checkbox.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(VSAT)) {
            viewer.dataSources.add(VSAT);
            //viewer.zoomTo(VSAT, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(VSAT)) {
            viewer.dataSources.remove(VSAT);
        }
    }
}, false);
var checkbox1 = document.getElementById('showSATCheckbox');
checkbox1.addEventListener('change', function () {
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
var checkbox2 = document.getElementById('showGWCheckbox');
checkbox2.addEventListener('change', function () {
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
var checkbox3 = document.getElementById('showELEVATIONCheckbox');
checkbox3.addEventListener('change', function () {
    // Checkbox state changed.
    if (checkbox3.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(ELEVATION)) {
            viewer.dataSources.add(ELEVATION);
            // viewer.zoomTo(ELEVATION, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(ELEVATION)) {
            viewer.dataSources.remove(ELEVATION);
        }
    }
}, false);

var checkbox7 = document.getElementById('showSAT_GPTCheckbox');
checkbox7.addEventListener('change', function () {
    // Checkbox state changed.
    if (checkbox7.checked) {
        // Show if not shown.
        if (!viewer.dataSources.contains(SAT_GPT)) {
            viewer.dataSources.add(SAT_GPT);
            // viewer.zoomTo(ELEVATION, new Cesium.HeadingPitchRange(40,-90,9000000));
        }
    } else {
        // Hide if currently shown.
        if (viewer.dataSources.contains(SAT_GPT)) {
            viewer.dataSources.remove(SAT_GPT);
        }
    }
}, false);

var checkbox4 = document.getElementById('showFOVCheckbox');
checkbox4.addEventListener('change', function () {
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
checkbox5.addEventListener('change', function () {
    // Checkbox state changed.
    if (checkbox5.checked) {
        viewer.zoomTo(SAT, new Cesium.HeadingPitchRange(40, -90, 9000000));
    }
}, false);
var checkbox6 = document.getElementById('showTRSPCheckbox');
checkbox6.addEventListener('change', function () {
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
checkbox8.addEventListener('change', function () {
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
viewer.zoomTo(VSAT, new Cesium.HeadingPitchRange(40, -90, 9000000));
var credit = new Cesium.Credit('Catapult', '../images/saWhite26.png', 'http://sa.catapult.org.uk');
viewer.scene.frameState.creditDisplay.addDefaultCredit(credit)
