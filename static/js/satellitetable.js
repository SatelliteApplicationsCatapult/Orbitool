var satellitetable = jQuery('script[src*=satellitetable]');
var satjson = satellitetable.attr('jsons');
var editableGridsat = null;


editableGridsat = new window.EditableGrid("satgrid", {

    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this?')) editableGridsat.delete(" + cell.rowIndex + "); editableGridsat.remove(" + cell.rowIndex+ ");\" style=\"cursor:pointer\">" +
                    "<img height='23px' src=\"/linkbudgetweb/static/images/delete_sat.png\" border=\"0\" alt=\"delete\" title=\"Delete\"/></a>";
                cell.innerHTML+= "&nbsp;<a onclick=\"editableGridsat.duplicate(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/duplicate.png\" border=\"0\" alt=\"duplicate\" title=\"Copy\"/></a>";
            }
        }));

        // render the grid
        this.renderGrid("satellite_tablecontent", "testgrid", "sat");
    },

    // called when some value has been modified: we display a message
    modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) {
        var lon = editableGridsat.data[rowIdx].columns[2];
        var lat = editableGridsat.data[rowIdx].columns[1];
        var alt = editableGridsat.data[rowIdx].columns[3];
        //Longitude Change
        if (colIdx == 1) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(lon, newValue, alt*1000))
            SUBSAT.entities._entities._array[rowIdx]._polyline._positions.setValue([Cesium.Cartesian3.fromDegrees(lon, newValue, 0),Cesium.Cartesian3.fromDegrees(lon, newValue, alt*1000)])

        }
        //Latitude Change
        if (colIdx == 2) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(newValue, lat, alt*1000))
            SUBSAT.entities._entities._array[rowIdx]._polyline._positions.setValue([Cesium.Cartesian3.fromDegrees(newValue, lat, 0),Cesium.Cartesian3.fromDegrees(newValue, lat, alt*1000)])

        }
        // Altitude Change
        if (colIdx == 3) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(lon, lat, newValue*1000))
            SUBSAT.entities._entities._array[rowIdx]._polyline._positions.setValue([Cesium.Cartesian3.fromDegrees(lon, lat, 0),Cesium.Cartesian3.fromDegrees(lon, lat, newValue*1000)])
        }
        jQuery.ajax({
            type: "POST",
            url: "/default/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "SAT",
                "columnname": editableGridsat.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {
            viewer.dataSources.remove(TRSP_FOV_CIRCLE)
            viewer.dataSources.remove(FOV_CIRCLE)
            FOV_CIRCLE.load("/SAT_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function() {
                var entities = FOV_CIRCLE.entities.values;
                for (var i = 0; i < entities.length; i++) {
                    var entity = entities[i];
                    entity.polyline.loop = true;
                    entity.polyline.material = Cesium.Color.BLACK;
                    entity.polyline.width = .8; // lines get displayed properly with red strok
                }
            });
            TRSP_FOV_CIRCLE.load("/TRSP_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function() {
                var entities = TRSP_FOV_CIRCLE.entities.values;
                for (var i = 0; i < entities.length; i++) {
                    var entity = entities[i];
                    entity.polyline.loop = true;
                    entity.polyline.material = Cesium.Color.LIGHTGREY;
                    entity.polyline.width = .8;
                }
            });
            viewer.dataSources.add(FOV_CIRCLE);
            viewer.dataSources.add(TRSP_FOV_CIRCLE);

        });

    }
});

editableGridsat.delete = function(rowIndex) {
    jQuery.ajax({
        type: "POST",
        url: "/default/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "SAT",
            "rowid": editableGridsat.getRowId(rowIndex),
        })
    }).done(function(msg) {
        SAT.load("/get_geojson_sat/"+window.location.pathname.split('/')[2]).then(function () {
        var entities = SAT.entities.values;
        for (var i = 0; i < entities.length; i++) {
            var entity = entities[i];
            entity.billboard = new Cesium.BillboardGraphics({
                image: "/linkbudgetweb/static/images/satellite.gif",
            })
        }
        });
        SUBSAT.load("/json_subsatellite/"+window.location.pathname.split('/')[2]).then(function () {
                    var entities = SUBSAT.entities.values;
                    for (var i = 0; i < entities.length; i++) {
                        var entity = entities[i];
                        entity.polyline.width = 1;
                    }
                });
        viewer.dataSources.remove(TRSP_FOV_CIRCLE)
        viewer.dataSources.remove(FOV_CIRCLE)
        FOV_CIRCLE.load("/SAT_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function() {
            var entities = FOV_CIRCLE.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.polyline.loop = true;
                entity.polyline.material = Cesium.Color.BLACK;
                entity.polyline.width = .8; // lines get displayed properly with red strok
            }
        });
        TRSP_FOV_CIRCLE.load("/TRSP_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function() {
            var entities = TRSP_FOV_CIRCLE.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.polyline.loop = true;
                entity.polyline.material = Cesium.Color.LIGHTGREY;
                entity.polyline.width = .8;
            }
        });
        viewer.dataSources.add(FOV_CIRCLE);
        viewer.dataSources.add(TRSP_FOV_CIRCLE);




    });
};

editableGridsat.duplicate = function(rowIndex)
{
    // The below adds a new row on the front end without refreshing
	// // copy values from given row
	var values = this.getRowValues(rowIndex);
	// get id for new row (max id + 1)
	var newRowId = 0;
	for (var r = 0; r < this.getRowCount(); r++) newRowId = Math.max(newRowId, parseInt(this.getRowId(r)) + 1);
	// add new row
    var max_id = 0
    for (i=0; i<editableGridsat.data.length; i++){
        max_id = Math.max(editableGridsat.data[i]["columns"][0],max_id)
    }
    new_id = max_id+1
    values['SAT_ID']= new_id
	this.insertAfter(rowIndex, newRowId, values);
    // copies a row on the backend
	jQuery.ajax({
            type: "POST",
            url: "/default/copy",
            data: "array=" + JSON.stringify({
                "table": "SAT",
                "rowid": editableGridsat.getRowId(rowIndex),
                "new_id": new_id,
            })
        }).done(function(msg) {
                // copies a row on the backend
                SAT.load("/get_geojson_sat/"+window.location.pathname.split('/')[2]).then(function () {
                    var entities = SAT.entities.values;
                    for (var i = 0; i < entities.length; i++) {
                        var entity = entities[i];
                        entity.billboard = new Cesium.BillboardGraphics({
                            image: "/linkbudgetweb/static/images/satellite.gif",
                        })
                    }
                });
                SUBSAT.load("/json_subsatellite/"+window.location.pathname.split('/')[2]).then(function () {
                    var entities = SUBSAT.entities.values;
                    for (var i = 0; i < entities.length; i++) {
                        var entity = entities[i];
                        entity.polyline.width = 1;
                    }
                });
    });

};

editableGridsat.loadJSON(satjson);
