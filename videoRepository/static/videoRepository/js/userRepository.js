
$(document).ready(function() {

	$("#id_selectManifest").change(function(){
		$("#selectedManifest").html($(this).val());
	});

	$("#id_selectVideoFiles").change(function(){
		var files = $(this)[0].files;
		var msg;
		if(files.length == 1) {
			msg = '1 file selected.'
		} else {
			msg = files.length + ' files selected.'
		}
		$("#selectedVideoFiles").html(msg);
	});

});


