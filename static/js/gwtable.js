var gwtable = $('script[src*=gwtable]');
var json3 = gwtable.attr('json3');
var editableGridgw = null;

editableGridgw = new window.EditableGrid("gwgrid", {
    // called when the XML has been fully loaded
    tableLoaded: function() {

        // display a message

        // renderer for the action column
        this.setCellRenderer("action", new CellRenderer({
            render: function(cell, value) {
                cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this ? ')) editableGridgw.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
                    "<img src=\"/linkbudgetweb/static/images/delete.png\" border=\"0\" alt=\"delete\" title=\"delete\"/></a>";

            }
        }));

        // render the grid
        this.renderGrid("gw_tablecontent", "testgrid");
    },

    // called when some value has been modified: we display a message
    modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) {
        $.ajax({
            type: "POST",
            url: "/lbController/ajax_to_db",
            data: "array=" + JSON.stringify({
                "table": "GW",
                "columnname": editableGridgw.columns[colIdx].name,
                "value": newValue,
                "rowid": row,
            })
        }).done(function(msg) {});
    }

});

// load XML file
editableGridgw.loadJSON(json3);
