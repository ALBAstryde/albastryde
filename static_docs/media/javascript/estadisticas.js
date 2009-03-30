$.preloadImages = function()
{
  for(var i = 0; i<arguments.length; i++)
  {
    $("<img>").attr("src", arguments[i]);
  }
};

$.preloadImages("/media/icons/ajax-loader.gif","/media/icons/reset.png");

            $(function()
            {
                                $('#id_start_date').datePicker(
                                        {
                                                startDate: '01/01/1920',
                                                endDate: (new Date()).addDays(-1).asString()
                                        }
                                );
                                $('#id_end_date').datePicker(
                                        {
                                                startDate: '02/01/1920',
                                                endDate: (new Date()).asString()
                                        }
                                );
$('#id_start_date').bind(
                'dpClosed',
                function(e, selectedDates)
                {
                        var d = selectedDates[0];
                        if (d) {
                                d = new Date(d);
                                $('#id_end_date').dpSetStartDate(d.addDays(1).asString());
                        }
                }
        );
        $('#id_end_date').bind(
                'dpClosed',
                function(e, selectedDates)
                {
                        var d = selectedDates[0];
                        if (d) {
                                d = new Date(d);
                                $('#id_start_date').dpSetEndDate(d.addDays(-1).asString());
                        }
                }
        );

            });

$(document).ready(function() {
var producto_height = $('#producto-chooser').height();
var mercado_height = $('#mercado-chooser').height();
var mercado_width = $('#mercado-chooser').width();
var producto_width = $("#producto-chooser").width();
var submit_height= $("#form-submitter").height();
var contents_width = $("#contents").width();

$("#mercado-chooser").css( { "left": (producto_width + 10) + "px"});
$("#from-chooser").css( { "left": (producto_width + mercado_width + 20) + "px"});
$("#until-chooser").css( { "left": (producto_width + mercado_width + 20) + "px"});
$("#form-submitter").css( { "left": (producto_width + 10) + "px", "top": (mercado_height+10) + "px" });
$("#dbformfiller").css( { "height": (Math.max(mercado_height+submit_height+10,producto_height) + 10) + "px" });

});
