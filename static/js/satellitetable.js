var satellitetable = $('script[src*=satellitetable]');
var satjson = satellitetable.attr('jsons');
var editableGridsat = null;


editableGridsat = new window.EditableGrid("satgrid", {

    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this? Note this feature is experimental and doesnt work 100% of the time')) editableGridsat.remove(" + cell.rowIndex+ "); editableGridsat.delete(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/delete.png\" border=\"0\" alt=\"delete\" title=\"delete\"/></a>";
                cell.innerHTML+= "&nbsp;<a onclick=\"editableGridsat.duplicate(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/duplicate.png\" border=\"0\" alt=\"duplicate\" title=\"Duplicate row\"/></a>";
            }
        }));

        // render the grid
        this.renderGrid("satellite_tablecontent", "testgrid");
    },

    // called when some value has been modified: we display a message
    modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) {

        //Longitude Change
        if (colIdx == 1) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(editableGridsat.data[rowIdx].columns[2], newValue, editableGridsat.data[rowIdx].columns[3]*1000))
            FOV.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(editableGridsat.data[rowIdx].columns[2], newValue, editableGridsat.data[rowIdx].columns[3]*1000/2))
        }
        //Latitude Change
        if (colIdx == 2) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(newValue, editableGridsat.data[rowIdx].columns[1], editableGridsat.data[rowIdx].columns[3]*1000))
            FOV.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(newValue, editableGridsat.data[rowIdx].columns[1], editableGridsat.data[rowIdx].columns[3]*1000/2))
        }
        // Altitude Change
        if (colIdx == 3) {
            SAT.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(editableGridsat.data[rowIdx].columns[2], editableGridsat.data[rowIdx].columns[1], newValue*1000))
            FOV.entities._entities._array[rowIdx]._position.setValue(Cesium.Cartesian3.fromDegrees(editableGridsat.data[rowIdx].columns[2], editableGridsat.data[rowIdx].columns[1], newValue*1000/2))
            FOV.entities._entities._array[rowIdx]._cylinder._length.setValue(newValue*1000)
            FOV.entities._entities._array[rowIdx]._cylinder._bottomRadius.setValue(newValue * 1000 * Math.tan((3.14159 / 180) * editableGridsat.data[rowIdx].columns[4]))
        }
        $.ajax({
            type: "POST",
            url: "/lbController/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "SAT",
                "columnname": editableGridsat.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {});

        SAT.load("/get_geojson_sat/"+window.location.pathname.split('/')[2]).then(function () {
        var entities = SAT.entities.values;
        for (var i = 0; i < entities.length; i++) {
            var entity = entities[i];
            entity.billboard = new Cesium.BillboardGraphics({
                image: "/linkbudgetweb/static/images/satellite.gif",
            })
        }
        });
    }
});

editableGridsat.delete = function(rowIndex) {
    console.log(rowIndex)
    console.log(editableGridsat.getRowId(rowIndex))
    $.ajax({
        type: "POST",
        url: "/lbController/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "SAT",
            "rowid": editableGridsat.getRowId(rowIndex),
        })
    }).done(function(msg) {});

    SAT.load("/get_geojson_sat/"+window.location.pathname.split('/')[2]).then(function () {
    var entities = SAT.entities.values;
    for (var i = 0; i < entities.length; i++) {
        var entity = entities[i];
        entity.billboard = new Cesium.BillboardGraphics({
            image: "/linkbudgetweb/static/images/satellite.gif",
        })
    }
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
	this.insertAfter(rowIndex, newRowId, values);

	$.ajax({
            type: "POST",
            url: "/lbController/copy",
            data: "array=" + JSON.stringify({
                "table": "SAT",
                "rowid": editableGridsat.getRowId(rowIndex),
            })
        }).done(function(msg) {});

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

};

editableGridsat.loadJSON(satjson);
