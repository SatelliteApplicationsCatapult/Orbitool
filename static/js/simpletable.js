var simpletable = $('script[src*=simpletable]');
var json = simpletable.attr('json');
var editableGridtrsp = null;

editableGridtrsp = new window.EditableGrid("trspgrid", {
	// called when the XML has been fully loaded
	tableLoaded: function() {

		// display a message

		// renderer for the action column
		this.setCellRenderer("action", new CellRenderer({render: function(cell, value) {
		cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this ? ')) editableGrid.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
						 "<img src=\"/linkbudgetweb/static/images/delete.png\" border=\"0\" alt=\"delete\" title=\"delete\"/></a>";

		}}));

		// render the grid
		this.renderGrid("trsp_tablecontent", "testgrid");
	},

	// called when some value has been modified: we display a message
	modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) { $.ajax({
        type: "POST",
        url: "/lbController/ajax_to_db",
        data: "array="+JSON.stringify({"table":"TRSP", "columnname":editableGridtrsp.columns[colIdx].name, "value":newValue, "rowid":row,})
     }).done(function( msg ) { }); }
});

// load XML file
editableGridtrsp.loadJSON(json);
