var gwtable = jQuery('script[src*=gwtable]');
var json3 = gwtable.attr('json3');
var editableGridgw = null;

editableGridgw = new window.EditableGrid("gwgrid", {
    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this ? ')) editableGridgw.delete(" + cell.rowIndex + "); editableGridgw.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img height='23px' src=\"/linkbudgetweb/static/images/delete_ut.png\" border=\"0\" alt=\"delete\" title=\"Delete\"/></a>";
                cell.innerHTML+= "&nbsp;<a onclick=\"editableGridgw.duplicate(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/duplicate.png\" border=\"0\" alt=\"duplicate\" title=\"Copy\"/></a>";

            }
        }));

        // render the grid
        this.renderGrid("gw_tablecontent", "testgrid", "gw");
    },

    // called when some value has been modified: we display a message
    modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) {
        jQuery.ajax({
            type: "POST",
            url: "/default/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "GW",
                "columnname": editableGridgw.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {
            GW.load("/get_geojson_gw/"+window.location.pathname.split('/')[2]).then(function() {
            var entities = GW.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.billboard = new Cesium.BillboardGraphics({
                    image: "/static/images/groundstation.gif",
                });
            }
        });
        });
    }

});


editableGridgw.delete = function(rowIndex) {
    jQuery.ajax({
        type: "POST",
        url: "/default/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "GW",
            "rowid": editableGridgw.getRowId(rowIndex),
        })
    }).done(function(msg) {
        GW.load("/get_geojson_gw/"+window.location.pathname.split('/')[2]).then(function() {
            var entities = GW.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.billboard = new Cesium.BillboardGraphics({
                    image: "/static/images/groundstation.gif",
                });
            }
        });
    });
};


editableGridgw.duplicate = function(rowIndex)
{
        // The below adds a new row on the front end without refreshing
	// // copy values from given row
	var values = this.getRowValues(rowIndex);
	// get id for new row (max id + 1)
	var newRowId = 0;
	for (var r = 0; r < this.getRowCount(); r++) newRowId = Math.max(newRowId, parseInt(this.getRowId(r)) + 1);
	// add new row
	this.insertAfter(rowIndex, newRowId, values);
    // copies a row on the backend
	jQuery.ajax({
            type: "POST",
            url: "/default/copy",
            data: "array=" + JSON.stringify({
                "table": "GW",
                "rowid": editableGridgw.getRowId(rowIndex),
            })
        }).done(function(msg) {
            GW.load("/get_geojson_gw/"+window.location.pathname.split('/')[2]).then(function() {
            var entities = GW.entities.values;
            for (var i = 0; i < entities.length; i++) {
                var entity = entities[i];
                entity.billboard = new Cesium.BillboardGraphics({
                    image: "/static/images/groundstation.gif",
                });
            }
        });
    });
};

// load XML file
editableGridgw.loadJSON(json3);
