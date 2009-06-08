$.preloadImages = function() {
	for (var i = 0; i < arguments.length; i++) {
		$('<img>').attr('src', arguments[i]);
	}
};

$.preloadImages('/media/icons/ajax-loader.gif');

$(function() {
	var dayNames = [_('Sunday'),_('Monday'),_('Tuesday'),_('Wednesday'),_('Thursday'),_('Friday'),_('Saturday')];
	var dayNamesShort = [_('Sun'),_('Mon'),_('Tue'),_('Wed'),_('Thu'),_('Fri'),_('Sat')];
	var dayNamesMin = [_('Su'),_('Mo'),_('Tu'),_('We'),_('Th'),_('Fr'),_('Sa')];

	var monthNames = [_('January'),_('February'),_('March'),_('April'),_('May'),_('June'),_('July'),_('August'),_('September'),_('October'),_('November'),_('December')];
	var monthNamesShort = [_('Jan'),_('Feb'),_('Mar'),_('Apr'),_('May'),_('Jun'),_('Jul'),_('Aug'),_('Sep'),_('Oct'),_('Nov'),_('Dec')];
	var monthNamesMin = [_('Ja'),_('Fe'),_('Mar'),_('Ap'),_('May'),_('Jun'),_('Jul'),_('Ag'),_('Se'),_('Oc'),_('No'),_('De')];

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
//	$('#AjaxFormSubmit').attr('disabled', 'disabled'); //Disable the submit button - can't click twice
	$('.errorlist').remove(); //Get rid of any old error uls
	//$('#AjaxFormWarning').fadeOut('slow'); //Get rid of the main error message
	$('#AjaxFormWarning').html('<img src="/media/icons/ajax-loader.gif" />').fadeIn('slow');
	$('#AjaxFormWarning').ajaxError(function() {
		$(this).html(_('We are experiencing network errors!')).fadeIn('slow');
		$('#AjaxFormSubmit').attr('disabled', '');

	});
	return true;
}

$(document).ready(function() {
	// prepare Options Object 
	var options = {
		url: '.',
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
		if (eval(jsondata.bad)) {
			e_msg = _('Please check the form!');
			$('#AjaxFormWarning').text( e_msg ).fadeIn('slow');
			errors = eval(jsondata.errs); 
			$.each(errors,
			function(fieldname, errmsg) {
				id = '#id_' + fieldname;
				$(id).parent().after(errmsg); //I want the error above the <p> holding the field
			});
		} else {
			create_graphs(jsondata,false,'#GraphsHeader');

		}
	} else {
		$('#AjaxFormWarning').text(_('Ajax error: no data received.')).fadeIn('slow');
		$('#AjaxFormSubmit').attr('disabled', '');
	}
	// re-enable the submit button, coz user has to fix stuff.
	$('#AjaxFormSubmit').attr('disabled', '');

}
