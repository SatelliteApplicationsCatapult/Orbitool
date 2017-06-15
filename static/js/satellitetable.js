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
    }
});

editableGridsat.delete = function(rowIndex) {
    $.ajax({
        type: "POST",
        url: "/lbController/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "SAT",
            "rowid": editableGridsat.getRowId(rowIndex),
        })
    }).done(function(msg) {});
};

editableGridsat.duplicate = function(rowIndex)
{
    // The below adds a new row on the front end without refreshing
	// // copy values from given row
	// var values = this.getRowValues(rowIndex);
	// values['name'] = values['name'] + ' (copy)';
    //
	// // get id for new row (max id + 1)
	// var newRowId = 0;
	// for (var r = 0; r < this.getRowCount(); r++) newRowId = Math.max(newRowId, parseInt(this.getRowId(r)) + 1);
    //
	// // add new row
	// this.insertAfter(rowIndex, newRowId, values);

    // copies a row on the backend
	$.ajax({
            type: "POST",
            url: "/lbController/copy",
            data: "array=" + JSON.stringify({
                "table": "SAT",
                "rowid": editableGridsat.getRowId(rowIndex),
            })
        }).done(function(msg) {});
};


// load XML file
editableGridsat.loadJSON(satjson);
