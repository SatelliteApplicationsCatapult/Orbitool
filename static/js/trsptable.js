var trsptable = jQuery('script[src*=trsptable]');
var json = trsptable.attr('json');
var editableGridtrsp = null;

editableGridtrsp = new window.EditableGrid("trspgrid", {
    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this ? ')) editableGridtrsp.delete(" + cell.rowIndex + "); editableGridtrsp.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img height='23px' src=\"/linkbudgetweb/static/images/delete_trsp.png\" border=\"0\" alt=\"delete\" title=\"Delete\"/></a>";
                cell.innerHTML+= "&nbsp;<a onclick=\"editableGridtrsp.duplicate(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/duplicate.png\" border=\"0\" alt=\"duplicate\" title=\"Copy\"/></a>";

            }
        }));

        // render the grid
        this.renderGrid("trsp_tablecontent", "testgrid", "trsp");
    },

    // called when some value has been modified: we display a message
    modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) {
        jQuery.ajax({
            type: "POST",
            url: "/lbController/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "TRSP",
                "columnname": editableGridtrsp.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {
            viewer.dataSources.remove(TRSP_FOV_CIRCLE)
            TRSP_FOV_CIRCLE.load("/TRSP_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function() {
                var entities = TRSP_FOV_CIRCLE.entities.values;
                for (var i = 0; i < entities.length; i++) {
                    var entity = entities[i];
                    entity.polyline.loop = true;
                    entity.polyline.material = Cesium.Color.LIGHTGREY;
                    entity.polyline.width = .8;
                }
            });
            viewer.dataSources.add(TRSP_FOV_CIRCLE);
        });
    }

});

editableGridtrsp.delete = function(rowIndex) {
    jQuery.ajax({
        type: "POST",
        url: "/lbController/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "TRSP",
            "rowid": editableGridtrsp.getRowId(rowIndex),
        })
    }).done(function(msg) {
        TRSP_FOV_CIRCLE.load("/TRSP_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function () {
            var entities = TRSP_FOV_CIRCLE.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.polyline.loop = true;
                entity.polyline.material = Cesium.Color.LIGHTGREY;
                entity.polyline.width = .8;
            }
            });
    });
};


editableGridtrsp.duplicate = function(rowIndex)
{
    // The below adds a new row on the front end without refreshing
	// // copy values from given row
	var values = this.getRowValues(rowIndex);
	// get id for new row (max id + 1)
	var newRowId = 0;
	for (var r = 0; r < this.getRowCount(); r++) newRowId = Math.max(newRowId, parseInt(this.getRowId(r)) + 1);
	// add new row
    var max_id = 0
    for (i=0; i<editableGridtrsp.data.length; i++){
        max_id = Math.max(editableGridtrsp.data[i]["columns"][1],max_id)
    }
    new_id = max_id+1
    values['TRSP_ID']= new_id
	this.insertAfter(rowIndex, newRowId, values);
    // copies a row on the backend
	jQuery.ajax({
            type: "POST",
            url: "/lbController/copy",
            data: "array=" + JSON.stringify({
                "table": "TRSP",
                "rowid": editableGridtrsp.getRowId(rowIndex),
                "new_id": new_id,
            })
        }).done(function(msg) {
                TRSP_FOV_CIRCLE.load("/TRSP_FOV_to_JSON/"+window.location.pathname.split('/')[2]).then(function () {
                        var entities = TRSP_FOV_CIRCLE.entities.values;
                        for (var i = 0; i < entities.length; i++) {
                            var entity = entities[i];
                            entity.polyline.loop = true;
                            entity.polyline.material = Cesium.Color.LIGHTGREY;
                            entity.polyline.width = .8;
                        }
                    });
    });

};

// load XML file
editableGridtrsp.loadJSON(json);
