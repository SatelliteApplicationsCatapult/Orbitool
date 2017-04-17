var simpletable = $('script[src*=simpletable]');
var json = simpletable.attr('json');
var editableGrid = null;

function loadJSON()
{
	editableGrid = new EditableGrid("DemoGridSimple", {

		// called when the XML has been fully loaded
		tableLoaded: function() {

			// display a message
			_$("trsp_message").innerHTML = "<p class='ok'>Ready!</p>";

			// renderer for the action column
			this.setCellRenderer("action", new CellRenderer({render: function(cell, value) {
				cell.innerHTML = "<a onclick=\"if (confirm('Are you sure you want to delete this person ? ')) editableGrid.remove(" + cell.rowIndex + ");\" style=\"cursor:pointer\">" +
								 "<img src=\"/linkbudgetweb/static/images/delete.png\" border=\"0\" alt=\"delete\" title=\"delete\"/></a>";
				 $.ajax({
			          type: "POST",
			          url: "/lbController/delete_row_editablegrid",
			          data: "array="+JSON.stringify({"table":"TRSP", "columnname":editableGrid.columns[colIdx].name, "value":newValue, "rowid":row,})
			       }).done(function( msg ) { });
				}}));

				// render the grid
			this.renderGrid("trsp_tablecontent", "testgrid");
		},

		// called when some value has been modified: we display a message
		modelChanged: function(rowIdx, colIdx, oldValue, newValue, row) { $.ajax({
          type: "POST",
          url: "/lbController/ajax_to_db",
          data: "array="+JSON.stringify({"table":"TRSP", "columnname":editableGrid.columns[colIdx].name, "value":newValue, "rowid":row,})
       }).done(function( msg ) { }); }
	});

	// load XML file
	editableGrid.loadJSON(json);
}

// start when window is loaded
window.onload = loadJSON;
