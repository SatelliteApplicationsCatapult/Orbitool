var satellitetable = $('script[src*=satellitetable]');
var satjson = satellitetable.attr('jsons');
var editableGridsat = null;

function loadJSONsat()
{
	editableGridsat = new window.EditableGrid("satgrid", {

		// called when the XML has been fully loaded
		tableLoaded: function() {

			// display a message

			// renderer for the action column
			this.setCellRenderer("action", new CellRenderer({render: function(cell, value) {
			cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this person ? ')) editableGridsat.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
							 "<img src=\"/linkbudgetweb/static/images/delete.png\" border=\"0\" alt=\"delete\" title=\"delete\"/></a>";

			}}));

			// render the grid
			this.renderGrid("satellite_tablecontent", "testgrid");
		},

		// called when some value has been modified: we display a message
		modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) { $.ajax({
          type: "POST",
          url: "/lbController/ajax_to_db",
          data: "array="+JSON.stringify({"table":"SAT", "columnname":editableGridsat.columns[colIdx].name, "value":newValue, "rowid":row,})
       }).done(function( msg ) { }); }
	});

	// load XML file
	editableGridsat.loadJSON(satjson);
}

// start when window is loaded
window.onload = loadJSONsat;
