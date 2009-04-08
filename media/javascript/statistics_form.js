$.preloadImages = function() {
	for (var i = 0; i < arguments.length; i++) {
		$('<img>').attr('src', arguments[i]);
	}
};

$.preloadImages('/media/icons/ajax-loader.gif');

$(function() {
	$('#id_StartDate').datepicker({
		dateFormat: 'dd.mm.yy',
		changeYear: true,
		minDate: new Date('01/01/1920'),
		maxDate: (new Date()).addDays( - 1),
		onSelect : function(selectedDate) {
			d = new Date(selectedDate.substring(3,5)+'/'+selectedDate.substring(0,2)+'/'+selectedDate.substring(6,10)).addDays(1);
			$('#id_EndDate').datepicker('option','minDate',d);			
		}
	});
	$('#id_EndDate').datepicker({
		dateFormat: 'dd.mm.yy',
		changeYear: true,
		minDate: new Date('01/02/1920'),
		maxDate: new Date(),
		onSelect : function(selectedDate) {
			d = new Date(selectedDate.substring(3,5)+'/'+selectedDate.substring(0,2)+'/'+selectedDate.substring(6,10)).addDays(-1);
			$('#id_StartDate').datepicker('option','maxDate',d);			
		}
	});
});

$(document).ready(function() {
	var producto_height = $('#producto-chooser').height();
	var from_width = $('#from-chooser').width();
	var mercado_height = $('#mercado-chooser').height();
	var mercado_width = $('#mercado-chooser').width();
	var producto_width = $('#producto-chooser').width();
	var submit_height = $('#form-submitter').height();
	//var contents_width = $('#contents').width();
	$('#mercado-chooser').css({
		'left': (producto_width + 10) + 'px'
	});
	$('#from-chooser').css({
		'left': (producto_width + mercado_width + 20) + 'px'
	});
	$('#lluvia-chooser').css({
		'left': (producto_width + mercado_width + from_width + 30) + 'px'
	});
	$('#until-chooser').css({
		'left': (producto_width + mercado_width + 20) + 'px'
	});
	$('#form-submitter').css({
		'left': (producto_width + 10) + 'px',
		'top': (mercado_height + 10) + 'px'
	});
	$('#dbformfiller').css({
		'height': (Math.max(mercado_height + submit_height + 10, producto_height) + 10) + 'px'
	});

});

function beforeForm() {
	$('#AjaxFormSubmit').attr('disabled', 'disabled'); //Disable the submit button - can't click twice
	$('.errorlist').remove(); //Get rid of any old error uls
	//$('#AjaxFormWarning').fadeOut('slow'); //Get rid of the main error message
	$('#AjaxFormWarning').html('<img src="/media/icons/ajax-loader.gif" />').fadeIn('slow');
	$('#AjaxFormWarning').ajaxError(function() {
		$(this).html('Hay problemas con el red!').fadeIn('slow');
		$('#AjaxFormSubmit').attr('disabled', '');

	});
	return true;
}

$(document).ready(function() {
	// prepare Options Object 
	var options = {
		url: '.',
		// Here we pass the xhr flag
		dataType: 'json',
		success: processJson,
		//What to call after a reply from Django
		beforeSubmit: beforeForm
	};
	// bind form using ajaxForm 
	$('#AjaxForm').ajaxForm(options); //My form id is 'AjaxForm'
});

function processJson(jsondata) {
	//Do we have any data at all?
	if (jsondata) {
		//		e_msg = 'We received your form, thank you.';
		//		$('#AjaxFormWarning').text( e_msg ).fadeIn('slow');
		if (eval(jsondata.bad)) {
			e_msg = 'Please check your form.';
			errors = eval(jsondata.errs); //Again with the eval :)
			$.each(errors,
			function(fieldname, errmsg) {
				id = '#id_' + fieldname;
				$(id).parent().after(errmsg); //I want the error above the <p> holding the field
			});
		} else {
			create_graphs(jsondata,true,'#GraphsHeader');

		}
	} else {
		//DON'T PANIC :D
		$('#AjaxFormWarning').text('Ajax error : no data received. ').fadeIn('slow');
	}
	// re-enable the submit button, coz user has to fix stuff.
	$('#AjaxFormSubmit').attr('disabled', '');

}
