$.preloadImages = function() {
	for (var i = 0; i < arguments.length; i++) {
		$('<img>').attr('src', arguments[i]);
	}
};

$.preloadImages('/media/icons/ajax-loader.gif');

$(function() {
	var dayNames = ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'];
	var dayNamesShort = ['Dom','Lun','Mar','Mie','Jue','Vie','Sab'];
	var dayNamesMin = ['Do','Lu','Ma','Mi','Ju','Vi','Sa'];

	var monthNames = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
	var monthNamesShort = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
	var monthNamesMin = ['En','Fe','Mar','Ab','May','Jun','Jul','Ag','Se','Oc','No','Di'];

	$('#id_Desde').datepicker({
		dayNames: dayNames,
		dayNamesShort: dayNamesShort,
		dayNamesMin: dayNamesMin,
		monthNames: monthNames,
		monthNamesShort: monthNamesShort,
		monthNamesMin: monthNamesMin,
		
		dateFormat: 'dd.mm.yy',
		changeYear: true,
		minDate: new Date('01/01/1920'),
		maxDate: (new Date()).addDays( - 1),
		onSelect : function(selectedDate) {
			d = new Date(selectedDate.substring(3,5)+'/'+selectedDate.substring(0,2)+'/'+selectedDate.substring(6,10)).addDays(1);
			$('#id_Hasta').datepicker('option','minDate',d);			
		}
	});
	$('#id_Hasta').datepicker({
		dayNames: dayNames,
		dayNamesShort: dayNamesShort,
		dayNamesMin: dayNamesMin,
		monthNames: monthNames,
		monthNamesShort: monthNamesShort,
		monthNamesMin: monthNamesMin,

		dateFormat: 'dd.mm.yy',
		changeYear: true,
		minDate: new Date('01/02/1920'),
		maxDate: new Date(),
		onSelect : function(selectedDate) {
			d = new Date(selectedDate.substring(3,5)+'/'+selectedDate.substring(0,2)+'/'+selectedDate.substring(6,10)).addDays(-1);
			$('#id_Desde').datepicker('option','maxDate',d);			
		}
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
			e_msg = 'Por favor compruebe su formulario.';
			$('#AjaxFormWarning').text( e_msg ).fadeIn('slow');
			errors = eval(jsondata.errs); //Again with the eval :)
			$.each(errors,
			function(fieldname, errmsg) {
				id = '#id_' + fieldname;
				$(id).parent().after(errmsg); //I want the error above the <p> holding the field
			});
		} else {
			create_graphs(jsondata,false,'#GraphsHeader');

		}
	} else {
		//DON'T PANIC :D
		$('#AjaxFormWarning').text('Ajax error : no data received. ').fadeIn('slow');
	}
	// re-enable the submit button, coz user has to fix stuff.
	$('#AjaxFormSubmit').attr('disabled', '');

}
