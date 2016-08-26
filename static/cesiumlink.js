var viewer = new Cesium.Viewer('cesiumContainer',{
            timeline : false,
            animation : false
    });
    var scene = viewer.scene;
    //var dataSource = Cesium.GeoJsonDataSource.load('{{=URL('default', 'get_geojson')}}');
    var dataSource = new Cesium.GeoJsonDataSource();
    dataSource.load({{=data}}).then(function(){
        var entities = dataSource.entities.values;
        console.log(dataSource);
        for (var i = 0; i < entities.length; i++) {
            var entity = entities[i];
            entity.billboard = undefined;
            entity.point = new Cesium.PointGraphics({
                color: Cesium.Color.fromBytes((entity.properties.EIRP-290)*17.5,0,0,255),
                pixelSize: 10,
                scaleByDistance : Cesium.NearFarScalar(3.2e5, 100.0, 1.2e6, 0.01),
            })
        };
    });
    viewer.dataSources.add(dataSource);
    viewer.zoomTo(dataSource);
    $("#log").click(function(){
        console.log(viewer.camera.getMagnitude())
});
