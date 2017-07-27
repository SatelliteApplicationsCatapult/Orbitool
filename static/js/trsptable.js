var trsptable = $('script[src*=trsptable]');
var json = trsptable.attr('json');
var editableGridtrsp = null;

editableGridtrsp = new window.EditableGrid("trspgrid", {
    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this ? ')) editableGridtrsp.remove(" + cell.rowIndex + "); editableGridtrsp.delete(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
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
        $.ajax({
            type: "POST",
            url: "/lbController/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "TRSP",
                "columnname": editableGridtrsp.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {});
    }

});

editableGridtrsp.delete = function(rowIndex) {
    $.ajax({
        type: "POST",
        url: "/lbController/delete_row_editablegrid",
        data: "array=" + JSON.stringify({
            "table": "TRSP",
            "rowid": editableGridtrsp.getRowId(rowIndex),
        })
    }).done(function(msg) {});
};

editableGridtrsp.duplicate = function(rowIndex)
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
                "table": "TRSP",
                "rowid": editableGridtrsp.getRowId(rowIndex),
            })
        }).done(function(msg) {});
};

// load XML file
editableGridtrsp.loadJSON(json);
