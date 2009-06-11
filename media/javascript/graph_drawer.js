//Check if two arrays' contents are the same
//returns true if they are, otherwise false
equals = function(a,b)
{
  //Check if the arrays are undefined/null
  if(!a || !b) {
    return false;
}
  //first compare their lengths
  if(a.length == b.length)
  {
    //go thru all the vars
    for(var i = 0; i < a.length;i++)
    {
      //if the var is an array, we need to make a recursive check
      //otherwise we'll just compare the values
      if(typeof a[i] == 'object') {
        if(!equals(a[i],b[i])) {
          return false;
	}
      }
      else if(a[i] != b[i]) {
        return false;
      }
    }
    return true;
  }
  else {
  return false;
  }
};

var e_msg, errors;
JOHANNES6=[];
function create_graphs(jsondata, wiki_mode, graphsheader) {
	var query_id, id, headline, has_comments, plot, comments, datapoint_dictionary, graph_height, raw_graphs, converted_graphs, dollargraphs, eurographs, normalized_graphs, normalized_dollargraphs, normalized_eurographs, graphs;
	var color_counter = 0,
	comment_counter = 0,
	graph_wiki = false,
	graph_close = false,
	graph_link = false,
	graph_export = false,
	labelCanvas = false,
	all_variables={},
	all_place={},
	all_main_variable={},
	table_data={},	
	total_yaxis=1,
	first_date=parseInt(new Date().getTime()/1000,10),
	last_date=-2000000000,
	frequency_list=['daily','monthly','annualy'];
	if (wiki_mode) {
		editor_mode = false;
	} else {
		editor_mode = true;
	}
	if (jsondata.comments) {
		comments = jsondata.comments;
		has_comments = true;
	} else {
		comments = {};
		has_comments = false;
	}
	raw_graphs = eval(jsondata.graphs).sort();
	converted_graphs = convert_graphs_after_transport(raw_graphs);
	if (converted_graphs.length === 0) {
		e_msg = _('There is no data available for the selection!');
		$('#AjaxFormWarning').text(e_msg).fadeIn('slow');
		$('#AjaxFormSubmit').attr('disabled', '');
		return true;
	}
	datapoint_dictionary = calculate_datapoint_dictionary(converted_graphs);
	first_date_obj=new Date(first_date*1000);
	last_date_obj=new Date(last_date*1000);
	first_date_year=first_date_obj.getFullYear();
	first_date_month=first_date_obj.getMonth();
	first_date_month++;
	first_date_day=first_date_obj.getDate();
	last_date_year=last_date_obj.getFullYear();
	last_date_month=last_date_obj.getMonth();
	last_date_month++;
	last_date_day=last_date_obj.getDate();
	if ((first_date_day==1) && (last_date_day==1)) {
		if ((first_date_month==1) && (last_date_month==1)) {
			first_day_string = String(first_date_year);
			last_day_string = String(last_date_year);
		} else {
			first_date_string= String(first_date_year)+'-'+String(first_date_month);
			last_date_string= String(last_date_year)+'-'+String(last_date_month);
		}
	} else {
		first_date_string= String(first_date_year)+'-'+String(first_date_month)+'-'+String(first_date_day);
		last_date_string= String(last_date_year)+'-'+String(last_date_month)+'-'+String(last_date_day);
	}
	headline = '';
	$.each(all_main_variable,function(e,v) {
		headline +=e+', ';
	});

	headline = headline.substring(0,headline.length-2) + ' ' + _('in') + ' ';
	$.each(all_place,function(e,v) {
		headline +=e+', ';
	});
	headline = headline.substring(0,headline.length-2) + ' ('+first_date_string+' &ndash; '+last_date_string+')';
	var yaxis=[];
	for (i=0;i<converted_graphs.yaxis.length;i++) { 
		yaxis.push(converted_graphs.yaxis[i]);
	}
// create media data for tables and median graphs

	$.each(all_variables,function(type,frequencies) {
		var does_not_exist,all_tables_list;
		table_data[type]={};
		$.each(frequencies,function(frequency,variables) {
			table_data[type][frequency]={};
			all_tables_list=[];
			$.each(variables,function(variable,variable_values) {
//				table_data[type][frequency][variable]={};
				$.each(variable_values,function(variable_value,graph_numbers) {
				  	does_not_exist=true;
					for (i=0;i<all_tables_list.length;i++) {
						if (equals(all_tables_list[i][1],graph_numbers)) {
							all_tables_list[i][0].push([variable,variable_value]);
							does_not_exist=false;
							break;
						}
					}
					if (does_not_exist) {
						all_tables_list.push([[[variable,variable_value]],graph_numbers]);
					}
				});
			});
			JOHANNES7=all_tables_list;
			for (i=0;i<all_tables_list.length;i++) {
				var graphs_to_be_filled=[];
				for (f in all_tables_list[i][1]) {
					graphs_to_be_filled.push(converted_graphs[all_tables_list[i][1][f]]);
				}
				table_data[type][frequency][all_tables_list[i][0]] = calculate_estimated_data(graphs_to_be_filled);
				if (all_tables_list[i][1].length > 1) {
					var median_graph=calculate_mediangraph(table_data[type][frequency][all_tables_list[i][0]],all_tables_list[i][0]);
					converted_graphs = converted_graphs.concat(median_graph);
					JOHANNES9=all_tables_list[i][1];
				}
			}
				
		});
	});

	converted_graphs.yaxis=[];
	for (i=0;i<yaxis.length;i++) { 
		converted_graphs.yaxis.push(yaxis[i]);
	}
	query_id = String(new Date().getTime());
	e_msg = _('New graph generated!');

	//Show the message
	$('#AjaxFormWarning').text(e_msg).fadeIn('slow');

	$('span#' + query_id + 'graph_wiki').live('click',
	function(e) {
		$('#'+query_id+'graph_wiki_dialog').dialog('open');
	});
	$('span#' + query_id + 'graph_link').live('click',
	function(e) {
		$('#'+query_id+'graph_link_dialog').dialog('open');
	});
	$('span#' + query_id + 'graph_export').live('click',
	function(e) {
		$('#'+query_id+'graph_export_dialog').dialog('open');
	});
	$('span#' + query_id + 'graph_tables').live('click',
	function(e) {
		$('#'+query_id+'graph_tables_dialog').dialog('open');
	});
	$('span#' + query_id + 'graph_close').live('click',
	function(e) {
		reset_comments();
		unbind_all();
		$('#' + query_id).fadeOut(300,
		function() {
			$(this).remove();
		});
		destroy_all_globals();
	});

	//Calculate other graphs	
	normalized_graphs = calculate_normalizedgraphs(converted_graphs);
	if ('precio' in all_variables) {
		dollargraphs = calculate_currencygraphs(eval(jsondata.dollar), converted_graphs);
		eurographs = calculate_currencygraphs(eval(jsondata.euro), converted_graphs);
		normalized_dollargraphs = calculate_normalizedgraphs(dollargraphs);
		normalized_eurographs = calculate_normalizedgraphs(eurographs);
//		for (frequency in frequency_list) {
//			table_data[frequency_list[frequency]].USD=calculate_currencytables(eval(jsondata.dollar),table_data[frequency_list[frequency]].Cordoba);
//			table_data[frequency_list[frequency]].Euro=calculate_currencytables(eval(jsondata.euro),table_data[frequency_list[frequency]].Cordoba);
//		}
	}
	var graph_html;
	if (editor_mode) {
		graph_html = draw_graph_structure();
	} else {
		graph_html = draw_small_graph_structure();
	}
	$(graphsheader).after(graph_html);
	graphs = converted_graphs;
	make_graphs();
	draw_graph_link_dialog();
	draw_graph_wiki_dialog();
	draw_graph_export_dialog();
	draw_graph_tables_dialog();
	if ($.browser.msie) {
		$('div.graph').remove();
	}

	function draw_graph_export_dialog() {
		var export_data = csv_export(raw_graphs);
		var dialog_id = query_id+'graph_export_dialog';
		var dialog_text = '<div id="' + dialog_id + '">';
		dialog_text += _('To open these data in another program, copy the text below into a text editor. Then save it with the ending".csv". This file can now be openes with Open Office and similar programs.');
		dialog_text += '<br />';
		dialog_text += '<textarea rows="10" cols="80">';
		dialog_text += export_data;
		dialog_text += '</textarea>';
		dialog_text += '</div>';
		var dialog_options = {};
		dialog_options.title = _('Export data');
		dialog_options.autoOpen = false;
		dialog_options.width = 700;
		$('#' + query_id).append(dialog_text);
		$('#' + dialog_id).dialog(dialog_options);
	}

	function draw_graph_link_dialog() {
		var dialog_id = query_id+'graph_link_dialog';
		var dialog_text = '<div id="' + dialog_id + '">';
		dialog_text += _('To share this link, email');
		dialog_text += ' <a href="/estadisticas/' + jsondata.query_link + '">';
		dialog_text += _('this link');
		dialog_text += '</a></div>';
		var dialog_options = {};
		dialog_options.autoOpen = false;
		dialog_options.title = _('Permanent link');
		$('#' + query_id).append(dialog_text);
		$('#' + dialog_id).dialog(dialog_options);
	}

	function draw_graph_wiki_dialog() {
		var dialog_id = query_id+'graph_wiki_dialog';
		var dialog_text = '<div id="' + dialog_id + '">';
		dialog_text += _('Code to include in the wiki');
		dialog_text += '<br /><b>_estadisticas[' + jsondata.wiki_code + ']</b></div>';
		var dialog_options = {};
		dialog_options.autoOpen = false;
		dialog_options.title = _('Code for the wiki');
		$('#' + query_id).append(dialog_text);
		$('#' + dialog_id).dialog(dialog_options);
	}

	function draw_graph_tables_dialog() {
		var dialog_id = query_id+'graph_tables_dialog';
		var table_html = create_tables(dialog_id);
		var dialog_text = '<div id="' + dialog_id + '">';
		dialog_text += table_html;
		dialog_text += '</div>';
		var dialog_options = {};
		dialog_options.title = 'Tablas';
		dialog_options.draggable = false;
		dialog_options.autoOpen = false;
		dialog_options.width = '100%';
		$('#' + query_id).append(dialog_text);
		$('#' + dialog_id+'currencytabs').tabs();
		$('.' + dialog_id+'tabletabs').tabs();
		$('#' + dialog_id).dialog(dialog_options);
	}

	function convert_graphs_after_transport(graphs) {
		var new_graphs = [], unit_types = {};
		$.each(graphs,
		function(graph_index,graph_value) {
			var new_graph = {
				'unit': this.unit,
				'frequency': this.frequency,
				'type': this.type,
				'included_variables': this.included_variables,
				'place_js': this.place_js,
				'main_variable_js': this.main_variable_js,
				'normalize_factor_js': this.normalize_factor_js,
				'color': color_counter,
				'data': [],
				'clickable': {},
				'hoverable': {},
				'bars': {},
				'lines': {},
				'points': {},
				'top_value':0
			},
			data = [],
			max_data,
			minData,
			min_data_dic,
			intervals;
			

			//create dictionary of lists of all variables used by some graph or other (mercado, producto, lluvia estacion, etc.)
			if (! (new_graph.type in all_variables)) {
				all_variables[new_graph.type]={};
			}
			if (! (new_graph.frequency in all_variables[new_graph.type])) {
				all_variables[new_graph.type][new_graph.frequency]={};
			}
			$.each(this.included_variables,function(e,v) {
				if (! (e in all_variables[new_graph.type][new_graph.frequency])) {
					all_variables[new_graph.type][new_graph.frequency][e]={};
				}
				if (! (v in all_variables[new_graph.type][new_graph.frequency][e])) {
					all_variables[new_graph.type][new_graph.frequency][e][v]=[];
				}
				all_variables[new_graph.type][new_graph.frequency][e][v].push(graph_index);
			});
			JOHANNES1=all_variables;

			if ('unit_legend_js' in this) {
				new_graph.unit_legend_js=this.unit_legend_js;
			} else {
				new_graph.unit_legend_js='new_graph.unit+" "+_(new_graph.frequency)';
			}
			new_graph.label = eval(new_graph.main_variable_js) + ' '+_('in')+' ' + eval(new_graph.place_js) + ' (' + eval(new_graph.unit_legend_js)+')';
			if (! (this.unit in unit_types)) {
				unit_types[this.unit] = true;
			}
			intervals = typeof(this.data[0][0])=='object' ? true : false;
			new_graph.intervals=intervals;
			new_graph.start_date = intervals ? this.data[0][0][0] : this.data[0][0];
			if ('min_data_dic' in this) {
				minData=[];
				max_data = this.data;
				min_data_dic = this.min_data_dic;
				$.each(max_data,
				function() {
					var pk, max_value, min_value, time, time_start;
					time = this[0];
					time_start = intervals ? time[0] : time;
					max_value = parseFloat(this[1]);
					if (max_value > new_graph.top_value) {
						new_graph.top_value = max_value;
						new_graph.top_date = time_start;
					}
					pk = this[2];
					if (String(time_start) in min_data_dic) {
						min_value = min_data_dic[String(time_start)];
					} else {
						min_value = max_value;
					}
					minData.push([time, min_value]);
				});
				new_graph.data = max_data;
				new_graph.minData = minData;
			} else if ('min_data' in this) {
				new_graph.data = this.data;
				new_graph.minData = this.minData;
				$.each(this.data,function() {
					var time, max_value, time_start;
					time = this[0];
					time_start = intervals ? time[0] : time;
					max_value = parseFloat(this[1]);
					if (max_value > new_graph.top_value) {
						new_graph.top_value = max_value;
						new_graph.top_date = time_start;
					}
				});
			} else {
				new_graph.data = this.data;
				minData = false;
				$.each(this.data,function() {
					var time, time_start, max_value;
					time = this[0];
					time_start = intervals ? time[0] : time;
					max_value = parseFloat(this[1]);
					if (max_value > new_graph.top_value) {
						new_graph.top_value = max_value;
						new_graph.top_date = time_start;
					}
				});

			}
			if ( !(eval(this.place_js) in all_place)) {
				all_place[eval(this.place_js)]=true;
			}
			if ( !(eval(this.main_variable_js) in all_main_variable)) {
				all_main_variable[eval(this.main_variable_js)]=true;
			}
			new_graph.end_date = intervals ? new_graph.data[new_graph.data.length-1][0][1] : new_graph.data[new_graph.data.length-1][0];
			if (new_graph.start_date < first_date) {
				first_date=new_graph.start_date;
			}
			if (new_graph.end_date > last_date) {
				last_date=new_graph.end_date;
			}
			var graph_yaxis = 1;
			var yaxis_finder = 1;
			for (var item in unit_types) {
				if (item == this.unit) {
					new_graph.yaxis = yaxis_finder;
					if (yaxis_finder > total_yaxis) {
						total_yaxis=yaxis_finder;
					}
				}
				yaxis_finder += 1;
			}

			if (this.source == 'computed') {
				new_graph.hoverable=false;
				new_graph.clickable=false;
				new_graph.points.show=false;
				new_graph.points.drawCall=false;
			}
			new_graph.start_value = new_graph.data[0][1];
			if (new_graph.start_value === 0) {
				if (new_graph.top_value > 0) {
					new_graph.start_value = new_graph.top_value;
				} else {
					new_graph.start_value=1;
				}
			}
			if (new_graph.top_value === 0) {
				new_graph.top_value=1;
			}
			if (this.display == 'bars') {
				new_graph.bars = {
					'show': true
				};
				if (this.frequency == 'daily') {
					new_graph.bars.barWidth=86400;
				} else if (this.frequency == 'monthly') {
					new_graph.bars.barWidth=2628000;
				} else if (this.frequency == 'annualy') {
					new_graph.bars.barWidth=31536000;
				} else if (parseInt(this.frequency,10) > 0 ) {
					new_graph.bars.barWidth=parseInt(this.frequency,10);
				} else {
					new_graph.bars.barWidth=1;
				}
			} else {
				new_graph.lines = {
					'show': true
				};
				if (minData) {
					new_graph.minData = minData;
					new_graph.lines.fill = true;
				}
			}

			new_graphs.push(new_graph);
			color_counter += 1;
		});
		var yaxis = ['',''];
		var yaxis_finder = 0;
		for (var item in unit_types) {
			yaxis[yaxis_finder] = item;
			yaxis_finder++;
		}
		new_graphs.yaxis = yaxis;
		return new_graphs;
	}

	function calculate_currencytables(currency_dic, cordobatables) {
		var new_currencytables = [];
		var new_unit=currency_dic.unit;
		$.each(cordobatables,
		function() {
			var new_data, new_tablerow, i, j;
			var frequency=this[2][0]['frequency'];
			if (this[2][0]['unit']=='cordoba') {
				new_tablerow=[];
				new_tablerow[0]=this[0];
				new_tablerow[1]=this[1];
				new_tablerow[2]=[];
				for (i in this[2]) {
					new_tablerow[2][i]={};
					new_tablerow[2][i]['datatype']=this[2][i]['datatype'];
					new_tablerow[2][i]['independent']=this[2][i]['independent'];
					new_tablerow[2][i]['unit']=new_unit;
				}
				new_tablerow[3]=[];
				for (i in this[3]) {
					new_tablerow[3][i]=[];
					new_tablerow[3][i][0]=this[3][i][0];
					new_tablerow[3][i][1]=[];
					for (j in this[3][i][1]) {
						new_tablerow[3][i][1][j]=[];
						new_tablerow[3][i][1][j][0]=currency_dic[frequency][String(parseInt(this[3][i][0],10))] * this[3][i][1][j][0];
						new_tablerow[3][i][1][j][1]=this[3][i][1][j][1];
					}
				}
				new_currencytables.push(new_tablerow);
			}
		});
		return new_currencytables;
	}

	function calculate_currencygraphs(currency_dic, cordobagraphs) {
		var new_graphs = [], unit_types = {};
		$.each(cordobagraphs,
		function() {
			var new_data,
			frequency=this.frequency,
			new_graph = {
				'type': this.type,
				'yaxis': this.yaxis,
				'points': this.points,
				'lines': this.lines,
				'bars': this.bars,
				'frequency': this.frequency,
				'place_js': this.place_js,
				'main_variable_js': this.main_variable_js,
				'normalize_factor_js': this.normalize_factor_js,
				'unit_legend_js': this.unit_legend_js,
				'included_variables': this.included_variables,
				'color': this.color,
				'start_date': this.start_date,
				'top_date': this.top_date,
				'shadowSize': this.shadowSize,
				'clickable': this.clickable,
				'hoverable': this.hoverable,
				'intervals': this.intervals
			},
			intervals=this.intervals;
			if ('advanced_label' in this) {
				new_graph.advanced_label = this.advanced_label;
			}
			if (this.unit == 'C$') {
				new_graph.start_value = currency_dic[this.frequency][String(this.start_date)] * this.start_value;
				new_graph.top_value = currency_dic[this.frequency][String(this.top_date)] * this.top_value;
				new_data = [];
				$.each(this.data,
				function() {
					var time=this[0],
					cordoba = this[1],
					pk = this[2],
					time_start;
					time_start = intervals ? time[0] : time;
					var currency = currency_dic[frequency][String(time_start)];
					var currency_value = parseFloat(cordoba) * parseFloat(currency);
					new_data.push([time, currency_value, pk]);
				});
				new_graph.data = new_data;
				if ('minData' in this) {
					var minData = [];
					$.each(this.minData,
					function() {
						var time = this[0],
						cordoba = this[1],
						pk = this[2],
						time_start;
						time_start = intervals ? time[0] : time;
						var currency = currency_dic[frequency][String(time_start)];
						var currency_value = parseFloat(cordoba) * parseFloat(currency);
						minData.push([time, currency_value, pk]);
					});
					new_graph.minData = minData;
				}
				new_graph.unit = currency_dic.unit;
			} else {
				new_graph.start_value = this.start_value;
				new_graph.top_value = this.top_value;
				new_graph.data = this.data;
				if ('minData' in this) {
					new_graph.minData = this.minData;
				}
				new_graph.unit = this.unit;
			}
			if ('advanced_label' in this) {
				new_graph.label = this.advanced_label + ' (' + new_graph.unit + ' ' +_(new_graph.frequency)+')';
			} else {
				new_graph.label = eval(this.main_variable_js) + ' '+_('in')+' ' + eval(this.place_js) + ' (' + eval(this.unit_legend_js)+')';
			}
			if (! (new_graph.unit in unit_types)) {
				unit_types[new_graph.unit] = true;
			}
			new_graphs.push(new_graph);
		});
		var yaxis_finder = 0;
		new_graphs.yaxis=[];
		for (var item in unit_types) {
			new_graphs.yaxis[yaxis_finder] = item;
			yaxis_finder += 1;
		}
		return new_graphs.sort();
	}

	function calculate_mediangraph(median_data,median_variables) {
		var graph_series, date_item, new_data, date_value, value_value, total_value, value_item, new_graph, graph;
		new_graph = {
			'points': {
				'show': false
			},
			'lines': {
				'show': true,
				'fill': false
			},
			'hoverable': false,
			'clickable': false,
			'unit': median_data[0]['unit'],
			'frequency': median_data[0]['frequency'],
			'type': median_data[0]['type'],
			'yaxis': median_data[0]['yaxis'],
			'included_variables':{},
			'color': color_counter,
			'top_value':0,
			'start_date': median_data[0]['data'][0],
			'place_js': median_data[0].place_js,
			'main_variable_js': median_data[0].main_variable_js,
			'unit_legend_js': median_data[0].unit_legend_js
			};
		
		color_counter += 1;
		var is_included;
		$.each(median_data[0].included_variables,function(included_variable,included_variable_value) {
		  	is_included=false;
			for (i=0;i<median_variables.length;i++) {
				if ((included_variable=median_variables[i][0]) && (included_variable_value=median_variables[i][1])) {
					is_included=true;
				}
			}
			if (is_included===true) {
				new_graph.included_variables[included_variable]=included_variable_value;
			} else {
				new_graph.included_variables[included_variable]=_('median');
			}
		});

JOHANNES3=[new_graph,median_data];//XXX
		new_graph.data=[];
		for (date_item=0;date_item<median_data[0]['data'].length;date_item++) {
			date_value=median_data[0]['data'][date_item][0];
			total_value=0;
			for (graph=0;graph<median_data.length;graph++) {
				total_value+=median_data[graph]['data'][date_item][1];
				if ('minData' in median_data[graph]) {
					total_value+=median_data[graph]['minData'][date_item][1];
				} else {
					total_value+=median_data[graph]['data'][date_item][1];
				}
			}
			value_item=total_value/(median_data.length*2);
			if (value_item > new_graph.top_value) {
				new_graph.top_value=value_item;
			}
//			value_item=total_value;
			new_graph.data.push([date_value,value_item]);
		}
		new_graph.start_value=new_graph.data[0][1];
		new_graph.label = _('median');
		for (median_variable=0;median_variable<median_variables.length;median_variable++) {
			new_graph.label+=' '+median_variables[median_variable][0]+ ': '+median_variables[median_variable][1];
		}
		new_graph.label += ' (' + eval(new_graph.unit_legend_js)+')';//		new_graph.data=median_data[0].data;//erase!XXX

		return new_graph;
	}

	function calculate_estimated_data(graphs_list) {
		var filled_graph_list = [];
		var graph_dic = {};
		var to_time, from_time, from_value, to_value, last_time, last_value, search_from_counter, search_to_counter, slope, current_time, current_slope_list, time_delta, independent_value;
		var graph_time_dic, graph_counter, empty_values, time_string, value_string, time_item, counter, i;
		var graph_time_data_list, date_item, graph_item, median_variable_item, header_list;
		graph_time_dic = {};
		var empty_data_list;
		header_list = [];
		var disactivated_columns={};
		
		for (graph_item = 0; graph_item < graphs_list.length; graph_item++) {
			for (date_item in graphs_list[graph_item]['data']) {
				time_string = graphs_list[graph_item]['data'][date_item][0];
				if (typeof(time_string)=='object') {
					date = time_string[0]+(time_string[1] - time_string[0]);
				} else {
					date = time_string;
				}
				if (! (date in graph_time_dic)) {
				  	empty_data_list=new Array(graphs_list.length*2);
					for (i=0;i< empty_data_list.length;i++) {
						empty_data_list[i]=[null,false];
					}				
					graph_time_dic[date]=[time_string,empty_data_list];
				}
				value_string = graphs_list[graph_item]['data'][date_item][1];
				graph_time_dic[date][1][graph_item*2]=[value_string,true];
			}
			if ('minData' in graphs_list[graph_item]) {
				for (date_item in graphs_list[graph_item]['minData']) {
					time_string = graphs_list[graph_item]['minData'][date_item][0];
					if (typeof(time_string)=='object') {
						date = time_string[0]+(time_string[1] - time_string[0]);
					} else {
						date = time_string;
					}
					if (! (date in graph_time_dic)) {
						graph_time_dic[date]=[time_string,empty_data_list.slice()];
					}
					value_string = graphs_list[graph_item]['minData'][date_item][1];
					graph_time_dic[date][1][graph_item*2+1]=[value_string,true];
				}			
			} else {
				disactivated_columns[graph_item*2+1]=true;
			}
		}
		graph_time_data_list = [];
		for (time_item in graph_time_dic) {
			graph_time_data_list.push([time_item, graph_time_dic[time_item][0],graph_time_dic[time_item][1]]);
		}
		current_slope_list=new Array(graphs_list.length*2);
		for (i=0;i< current_slope_list.length;i++) {
			current_slope_list[i]=null;
		}
		graph_time_data_list = graph_time_data_list.sort();
		for (counter = 0; counter < graph_time_data_list.length; counter++) {
			for (i=0;i< graph_time_data_list[counter][2].length;i++) {
			    if (!(i in disactivated_columns)) {
				if (graph_time_data_list[counter][2][i][0] === null) {
					if (counter === 0) {
						from_time = to_time = from_value = to_value = null;
						for (search_from_counter = 0; search_from_counter < graph_time_data_list.length; search_from_counter++) {
							if (! (graph_time_data_list[search_from_counter][2][i][0] === null)) {
								from_time = graph_time_data_list[search_from_counter][0];
								from_value = graph_time_data_list[search_from_counter][2][i][0];
								for (search_to_counter = search_from_counter + 1; search_to_counter < graph_time_data_list.length; search_to_counter++) {
									if (! (graph_time_data_list[search_to_counter][2][i][0] === null)) {
										to_time = graph_time_data_list[search_to_counter][0];
										to_value = graph_time_data_list[search_to_counter][2][i][0];
										break;
									}
								}
								break;
							}
						}
						slope = current_slope_list[i] = (to_value - from_value) / (to_time - from_time);
						time_delta = from_time - (graph_time_data_list[0][0]);
						graph_time_data_list[0][2][i][0] = from_value - (time_delta * slope);//wouldn't this be plus?
					} else {//if  (((current_slope_list[i]) === null) || (isNaN(current_slope_list[i])==false)) {
						if (current_slope_list[i] === null) {
							from_time = graph_time_data_list[counter - 1][0];
							from_value = graph_time_data_list[counter - 1][2][i][0];
							to_time = null;
							to_value = null;
							for (finder = counter; finder < graph_time_data_list.length; finder++) {
								if (! (graph_time_data_list[finder][2][i][0] === null)) {
									to_time = graph_time_data_list[finder][0];
									to_value = graph_time_data_list[finder][2][i][0];
									break;
								}
							}
							if (to_value === null) {
								from_time = graph_time_data_list[counter - 2][0];
								from_value = graph_time_data_list[counter - 2][2][i][0];
								to_time = graph_time_data_list[counter - 1][0];
								to_value = graph_time_data_list[counter - 1][2][i][0];
							}
							current_slope_list[i] = (to_value - from_value) / (to_time - from_time);
						}
						last_time = graph_time_data_list[counter - 1][0];
						current_time = graph_time_data_list[counter][0];
						time_delta = current_time - last_time;
						last_value = graph_time_data_list[counter - 1][2][i][0];
						slope = current_slope_list[i];
//						JOHANNES6.push(current_slope_list.splice(0));
						graph_time_data_list[counter][2][i][0] = last_value + (time_delta * slope);
					}
				} else {
					current_slope_list[i] = null;
				}
			    }
			}
		}
		new_graphs_list=[];
		var new_graph;
		$.each(graphs_list, function(graph_index,graph_value) {
			var new_graph = {
				'unit': this.unit,
				'type': this.type,
				'yaxis': this.yaxis,
				'bars': this.bars,
				'frequency': this.frequency,
				'place_js': this.place_js,
				'main_variable_js': this.main_variable_js,
				'unit_legend_js': this.unit_legend_js,
				'legend': this.legend,
				'points': this.points,
				'lines': this.lines,
				'color': this.color,
				'relevance': this.relevance,
				'shadowSize': this.shadowSize,
				'included_variables': this.included_variables,
				'clickable': this.clickable,
				'hoverable': this.hoverable,
				'intervals': this.intervals
			};
			new_graph.data=[];
			for (i=0;i<graph_time_data_list.length;i++) {
				new_graph.data.push([graph_time_data_list[i][1],graph_time_data_list[i][2][graph_index*2][0],graph_time_data_list[i][2][graph_index*2][1]]);
			}
			if ('minData' in this) {
			  	new_graph.minData=[];
				for (i=0;i<graph_time_data_list.length;i++) {
					new_graph.minData.push([graph_time_data_list[i][1],graph_time_data_list[i][2][graph_index*2+1][0],graph_time_data_list[i][2][graph_index*2+1][1]]);
				}
			}
			new_graphs_list.push(new_graph);
		});
		return new_graphs_list;
	}

	function calculate_normalizedgraphs(unitgraphs) {
		var new_graphs = [];
		$.each(unitgraphs,
		function() {
			var new_data = [],
			new_graph=this,
			normalize_factor = eval(this.normalize_factor_js);
			new_graph = {
				'unit': this.unit,
				'type': 'normalizado',
				'yaxis': 1,
				'bars': this.bars,
				'frequency': this.frequency,
				'place_js': this.place_js,
				'main_variable_js': this.main_variable_js,
				'unit_legend_js': this.unit_legend_js,
				'points': this.points,
				'lines': this.lines,
				'color': this.color,
				'relevance': this.relevance,
				'shadowSize': this.shadowSize,
				'included_variables': this.included_variables,
				'clickable': this.clickable,
				'hoverable': this.hoverable,
				'intervals': this.intervals
			};
			if ('advanced_label' in this) {
				new_graph.label = this.advanced_label + ' (100% = ' + String(start_value) + ' ' + this.unit + 's '+_(new_graph.frequency)+')';
			} else {
				new_graph.label = eval(new_graph.main_variable_js) + ' '+_('in')+' ' + eval(new_graph.place_js) + ' (100% = ' + String(normalize_factor)+ ' ' + eval(new_graph.unit_legend_js)+')';
			}
			new_graph.unit='%';
			$.each(this.data,
			function() {
				var time = this[0],
				unit_value = this[1],
				pk = this[2],
				normalized_value = parseFloat(unit_value) / parseFloat(normalize_factor) * 100;
				new_data.push([time, normalized_value, pk]);
			});
			new_graph.data = new_data;
			if ('minData' in this) {
				var minData = [];
				$.each(this.minData,
				function() {
					var time = this[0],
					unit_value = this[1],
					pk = this[2],
					normalized_value = parseFloat(unit_value) / parseFloat(normalize_factor) * 100;
					minData.push([time, normalized_value, pk]);
				});
				new_graph.minData = minData;
			}
			new_graphs.push(new_graph);
		});
		new_graphs.yaxis = ['%',''];
		return new_graphs;
	}
	function makeLabelCanvas(width, height) {
		var c = document.createElement('canvas');
		c.width = width;
		c.height = height;
		c.id = query_id + 'labelcanvas';
		if ($.browser.msie) { // excanvas hack
			c = window.G_vmlCanvasManager.initElement(c);
		}
		return c;
	}
	function drawPoint(ctx, x, y, radius, fillStyle, plotOffset, dataitem, series) {
		var unique_pk = dataitem[2],
		comment_pk;
		if ((has_comments) && unique_pk in comments) {
			if (! (labelCanvas)) {
				var canvasHeight = $('#' + query_id + 'stats canvas:first').outerHeight();
				var canvasWidth = $('#' + query_id + 'stats canvas:first').outerWidth();
				var canvas = $(makeLabelCanvas(canvasWidth, canvasHeight)).css({
					position: 'absolute',
					left: 0,
					top: 0
				}).insertAfter('#' + query_id + 'stats canvas:first').get(0);
				labelCanvas = canvas.getContext('2d');
				labelCanvas.translate(plotOffset.left, plotOffset.top);
				labelCanvas.lineWidth = ctx.lineWidth;
			}
			labelCanvas.strokeStyle = ctx.strokeStyle;
			ctx.zIndex = 2;
			labelCanvas.beginPath();

			labelCanvas.arc(x, y, radius * 3, 0, 2 * Math.PI, true);
			var seconddigit = comment_counter % 26;
			var firstdigit = Math.floor(comment_counter / 26);
			if (firstdigit > 26) {
				firstdigit = firstdigit % 26;
			}
			var label = '';
			if (firstdigit > 0) {
				label += String.fromCharCode(firstdigit + 96);
			}
			label += String.fromCharCode(seconddigit + 97);
			comment_counter += 1;
			var comments_text = '';
			if (editor_mode) {
				for (comment_pk in comments[unique_pk]) {
					comments_text += comments[unique_pk][comment_pk][0];
					comments_text += '<br /><span class="signature">' + comments[unique_pk][comment_pk][1] + '</span><br />';
					if (comments[unique_pk][comment_pk][2] === true) {
						comments_text += '<span class="editline" id="' + query_id + '_' + unique_pk + '"><span class="link" id="' + unique_pk + '+' + comment_pk + '+' + query_id + '"><span class="ui-icon ui-icon-pencil"></span></span></span>';
					}
					$('#' + query_id + 'comments').append('<h3><a href="#">' + label + '</a></h3><div>' + comments_text + '</div>');
				}
			} else {
				comments_text += '<tr><td valign="top"><b>' + label + '</b></td>';
				var first_comment = true;
				for (comment_pk in comments[unique_pk]) {
					if (! (first_comment)) {
						comments_text += '<tr><td>&nbsp;</td>';
					}
					comments_text += '<td>' + comments[unique_pk][comment_pk][0] + '</td></tr>';
					$('#' + query_id + 'comments').append(comments_text);
					first_comment = false;
				}
			}

			$('<div class="pointLabel" id="' + query_id + '_' + unique_pk + 'label">' + label + '</div>').insertAfter('#' + query_id + 'labelcanvas');
			var editButtons = $('span.editline#' + query_id + '_' + unique_pk + ' span.link');
			editButtons.bind('click',
			function() {
				var total_pk, this_unique_pk, this_comment_pk;
				total_pk = $(this).attr('id').split('+');
				this_unique_pk = total_pk[0];
				this_comment_pk = total_pk[1];
				create_comment_form(this_unique_pk, this_comment_pk);
			});
			var pointDiv = $('#' + query_id + '_' + unique_pk + 'label');
			var labelwidth = pointDiv.outerWidth();
			var leftOffset = plotOffset.left - (labelwidth / 2) + 0.5;
			pointDiv.css({
				top: y,
				left: leftOffset + x
			});
			if (fillStyle) {
				labelCanvas.fillStyle = fillStyle;
				labelCanvas.fill();
			}

			labelCanvas.stroke();
		} else {
			ctx.zIndex = 1;
			ctx.beginPath();
			ctx.arc(x, y, radius, 0, 2 * Math.PI, true);
			if (fillStyle) {
				ctx.fillStyle = fillStyle;
				ctx.fill();
			}
			ctx.stroke();
		}
	}

	function create_comment_form(unique_pk, comment_pk) {
		var comment, form_info;
		var pk_array = unique_pk.split('_');
		var content_type = pk_array[0];
		var object_pk = pk_array[1];
		var timestamp = parseInt(new Date().getTime().toString().substring(0, 10), 10);
		if (comment_pk) {
			var comment_text = comments[unique_pk][comment_pk][0];
		}
		var label = datapoint_dictionary[unique_pk][3];
		if (label.length === 0) {
			label = _('product');
		}
		var value = datapoint_dictionary[unique_pk][1];
		var raw_date = datapoint_dictionary[unique_pk][0];
		var date = date_string(raw_date);

		var dialog_options = {};
		var dialog_id = Date.now();
		var dialog_text = '';

		dialog_options.close = function () {
			$('#'+dialog_id).dialog('destroy');
			$('#'+dialog_id).remove();
		};
		dialog_options.width = 700;
		dialog_text += '<div id="' + dialog_id + '">';
		if (comment_pk) {
			dialog_options.title = _('Edit Comment')+': ';
		} else {
			dialog_options.title = _('New Comment')+': ';
		}
		dialog_options.title += label + ': ' + value + ' (' + date + ')';
		dialog_text += '<form name="newcomment" id="' + dialog_id + 'newcomment" method="post">';
		if (comment_pk) {
			dialog_text += '<input type="hidden" name="comment_pk" id="' + dialog_id + 'comment_pk" value="' + comment_pk + '">';
		}
		dialog_text += '<input type="hidden" name="timestamp" id="' + dialog_id + 'timestamp_field" value="' + timestamp + '">';
		dialog_text += '<input type="hidden" name="honeypot" id="' + dialog_id + 'honeypot_field" value="">';
		dialog_text += '<textarea id="' + dialog_id + 'comment_field" name="comment" rows="10" cols="80" name="comment" class="vLargeTextField">';
		if (comment_text) {
			dialog_text += comment_text;
		}
		dialog_text += '</textarea>';
		dialog_text += '<div id ="' + dialog_id + 'formDivMessage">&nbsp;</div></form></div>';
		dialog_options.buttons = {
			'Guardar': function() {
				comment = $('#' + dialog_id + 'comment_field').val();
				form_info = {
					object_pk: object_pk,
					content_type: content_type,
					comment: comment
				};
				if (comment_pk) {
					form_info.comment_pk = comment_pk;
				}
				form_info.timestamp = $('#' + dialog_id + 'timestamp_field').val();
				form_info.honeypot = $('#' + dialog_id + 'honeypot_field').val();
				returnFormResponse(form_info, 'Guardando...', 'Guardado con exito!');
			}
		};
		if (comment_pk) {
			dialog_options.buttons.Borrar = function() {
				form_info = {
					object_pk: object_pk,
					content_type: content_type,
					remove: true,
					comment_pk: comment_pk
				};
				form_info.timestamp = $('#' + dialog_id + 'timestamp_field').val();
				form_info.honeypot = $('#' + dialog_id + 'honeypot_field').val();
				returnFormResponse(form_info, 'Borrando...', 'Borrado con exito!');
			};
		}
		$('#' + query_id).append(dialog_text);
		$('#' + dialog_id).dialog(dialog_options);
		form_info = {};
		function returnFormResponse(fI, processMessage, successMessage) {
			$('#' + dialog_id + 'formDivMessage').html(processMessage);
			$.post('/ajax/comment/post/', fI,
			function(data) {
				if (data.status == 'success') {
					if ('remove' in data) {
						delete comments[unique_pk][data.pk];
						var datapoint_comments_length = 0;
						for (var k in comments[unique_pk]) {
							datapoint_comments_length++;
						}
						if (datapoint_comments_length === 0) {
							delete comments[unique_pk];
						}
					} else {
						if (! (unique_pk in comments)) {
							comments[unique_pk] = {};
							has_comments = true;
						}
						comments[unique_pk][data.pk] = [comment, user_name, true, data.public];
					}
					redraw_graph();
					$('#' + dialog_id + 'formDivMessage').html(successMessage);
					$('#' + dialog_id).fadeOut(300,
					function() {
						$('#' + dialog_id).dialog('close');
					});
				} else {
					$('#' + dialog_id + 'formDivMessage').html(_('We encountered an error!'));
				}
				// The success or failure check will go here. . .
			},
			'json');
		}
	}

	function build_comment_accordion() {
		$('#' + query_id + 'comments').accordion();
	}

	function reset_comments() {
		labelCanvas = false;
		comment_counter = 0;
		$('#' + query_id + 'comments').accordion('destroy');
		$('#' + query_id + 'comments').empty();
		$('#' + query_id + 'labelcanvas').remove();
		$('#' + query_id + ' div.pointLabel').remove();
	}

	function redraw_graph() {
		reset_comments();
		plot.draw();
		build_comment_accordion();
	}

	function calculate_datapoint_dictionary(graphs) {
		var new_datapoint_dictionary = {};
		for (var series = 0; series < graphs.length; ++series) {
			for (var datapoint = 0; datapoint < graphs[series].data.length; ++datapoint) {
				var identifier = graphs[series]['data'][datapoint][2];
				new_datapoint_dictionary[identifier] = [graphs[series]['data'][datapoint][0], graphs[series]['data'][datapoint][1], graphs[series]['unit'], graphs[series]['label']];
			}
		}
		return new_datapoint_dictionary;
	}

	function draw_graph_structure() {
		var total_width = $(graphsheader).innerWidth() - 5;
		var graph_html = '';
		graph_html += '<div class="ui-dialog ui-widget ui-widget-content ui-corner-all undefined" style="width:' + total_width + 'px;" id="' + query_id + '">';
		graph_html += draw_inner_graph_structure(total_width);
		graph_html += '</div>';
		return graph_html;
	}

	function draw_inner_graph_structure(total_width) {
		var show_comments = false;
		var graph_width = total_width - 90;
		if (has_comments || user_can_add) {
			show_comments = true;
			graph_width = total_width - 200;
		}
		var graph_html = '';
		graph_html += '<div class="ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix">';
		graph_html += '<span id="ui-dialog-title-dialog" class="ui-dialog-title">';
		graph_html += headline;
		graph_html += '</span>';
		var iconpositions = ['one', 'two', 'three', 'four', 'five'];
		var current_icon = 0;
		if (! (wiki_mode)) {
			graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_close"><span class="ui-icon ui-icon-closethick">'+_('close')+'</span></span>';
			current_icon++;
			graph_close = true;
		} else {
			graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_switchmode"><span class="ui-icon ui-icon-arrowthick-2-ne-sw">'+_('view')+'</span></span>';
			current_icon++;
			graph_close = true;
		}
		if (jsondata.wiki_code) {
			if (can_edit_wiki) {
				graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_wiki"><span class="ui-icon ui-icon-script">'+_('wiki code')+'</span></span>';
				current_icon++;
				graph_wiki = true;
			}
		}
		if (jsondata.query_link) {
			graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_link"><span class="ui-icon ui-icon-mail-closed">'+_('link')+'</span></span>';
			current_icon++;
			graph_link = true;
		}
		graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_tables"><span class="ui-icon ui-icon-calculator">'+_('tables')+'</span></span>';
		current_icon++;
		graph_table = true;
		graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_export"><span class="ui-icon ui-icon-document">'+_('export')+'</span></span>';
		current_icon++;
		graph_export = true;

		graph_html += '</div>';
		graph_html += '<div style="height: auto; min-height: 400px; width: auto;" class="ui-dialog-content ui-widget-content" id="' + query_id + 'body">';
		graph_html += '<table cellspacing="0" cellpadding="0" class="layout-grid">';
		graph_html += '<tr><td valign="top" width="' + graph_width + 'px">';
		graph_html += '<div id="' + query_id + 'stats" style="height:400px;"></div>';
		graph_html += '<div id="' + query_id + 'statsoverview" style="height:50px;"></div>';
		graph_html += '<select id="' + query_id + 'xtype" class="' + query_id + 'graphkind">';
		graph_html += '<option selected="selected" value="real">'+_('Real')+'</option>';
		graph_html += '<option value="normalized">'+_('Normalized')+'</option></select>';
		if ('precio' in all_variables) {
			graph_html += '<select id="' + query_id + 'xunits" class="' + query_id + 'graphkind"><option selected="selected" value="cordobas">Cordobas</option>';
			graph_html += '<option value="dollars">USD</option><option value="euros">Euros</option></select>';
		}
		graph_html += '<div id="' + query_id + 'legend"></div>';
		graph_html += '</td>';
		if (show_comments) {
			graph_html += '<td width="200px" valign="top">';
			graph_html += '<b>'+_('Comments')+'</b>';
			graph_html += '<div id="' + query_id + 'comments"></div>';
			graph_html += '</td>';
		}
		graph_html += '</tr></table>';
		graph_html += '</div>';
		return graph_html;
	}

	function draw_small_graph_structure() {
		var total_width = (($(graphsheader).innerWidth() - 95) / 2);
		var graph_html = '';
		graph_html += '<div class="ui-dialog ui-widget ui-widget-content ui-corner-all undefined" style="width:' + total_width + 'px;float: right; margin-right: 0.5em;" id="' + query_id + '">';
		graph_html += draw_small_inner_graph_structure(total_width);
		graph_html += '</div>';
		return graph_html;
	}

	function draw_small_inner_graph_structure(total_width) {
		var show_comments = false;
		if (has_comments || user_can_add) {
			show_comments = true;
		}
		var graph_html = '';
		graph_html += '<div class="ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix">';
		graph_html += '<span id="ui-dialog-title-dialog" class="ui-dialog-title">';
		graph_html += headline;
		graph_html += '</span>';
		var iconpositions = ['one', 'two', 'three', 'four'];
		var current_icon = 0;
		if (! (wiki_mode)) {
			graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_close"><span class="ui-icon ui-icon-closethick">'+_('close')+'</span></span>';
			current_icon++;
			graph_close = true;
		}
		graph_html += '<span class="ui-dialog-titlebar-' + iconpositions[current_icon] + ' ui-corner-all link" id="' + query_id + 'graph_switchmode"><span class="ui-icon ui-icon-arrowthick-2-ne-sw">'+_('edit')+'</span></span>';
		current_icon++;
		graph_html += '</div>';
		graph_html += '<div style="height: auto; min-height: 400px; width: ' + (total_width - 45) + 'px;" class="ui-dialog-content ui-widget-content" id="' + query_id + 'body">';
		graph_html += '<div id="' + query_id + 'stats" style="height:400px"></div>';
		graph_html += '<table class="legend">';
		if (show_comments) {
			graph_html += '<tr><td width="50%" valign="top">';
			graph_html += '<table id="' + query_id + 'comments" style="font-size: smaller; color: rgb(84, 84, 84);"></table>';
			graph_html += '</td><td width="50%" valign="top">';
		} else {
			graph_html += '<td width="100%" valign="top">';
		}
		graph_html += '<div id="' + query_id + 'legend"></div>';
		graph_html += '</td></tr></table>';
		graph_html += '</div>';
		return graph_html;
	}

	function date_string(unixtimestamp) {
		if (typeof(unixtimestamp) == 'object') {
			unixtimestamp = unixtimestamp[0];
		}
		var raw_date = new Date(unixtimestamp*1000);
		var day = raw_date.getUTCDate();
		if (day < 10) {
			day = '0' + day;
		}
		var month = raw_date.getUTCMonth() + 1;
		if (month < 10) {
			month = '0' + month;
		}
		var year = raw_date.getUTCFullYear();
		var formated_date_string = year + '-' + month + '-' + day;
		return formated_date_string;
	}


	function create_tables(dialog_id) {
		var html, header_variable, variable, data_variable, data_series_variable,single_value,total_value,calculated,total_datalines,total_value_per_dataline;
		html='';
		html+='<div id="'+dialog_id+'currencytabs">';
		html+='<ul>';
		for (type in table_data) {
			for (frequency in table_data[type]) {
				for (variable in table_data[type][frequency]) {
					for (variable_value in table_data[type][frequency][variable]) {
						html+='<li><a href="#'+dialog_id+type+frequency+variable+variable_value+'">'+type+': '+variable+' = '+variable_value+' ('+_(frequency)+')</li>';
					}
				}
			}
		}
		html+='</ul>';
		for (type in table_data) {
			for (frequency in table_data[type]) {
				for (variable in table_data[type][frequency]) {
					for (variable_value in table_data[type][frequency][variable]) {
						html += '<div id="'+dialog_id+type+frequency+variable+variable_value+'">';
						html += '<table style="font-size: smaller; color: rgb(84, 84, 84);"><tr><td><div style="border: 1px solid rgb(204, 204, 204); padding: 1px;"><div style="border: 5px solid #C1609D; overflow: hidden; width: 4px; height: 0pt;"/></div></div></td><td>'+_('estimated value')+'</td></tr></table>';
						html += '<table>';
						html += '<tr>';
						html += '<th>&nbsp;</th>';
					}
				}
			}
		}
		html +='</div>';
		return html;
	}

	function csv_export(graphs) {
		var html = '';
		var headerline = '',
		new_headerline;
		for (var series = 0; series < graphs.length; ++series) {
			var datapoint;
			if ('max_data' in graphs[series]) {
				for (datapoint = 0; datapoint < graphs[series].max_data.length; ++datapoint) {
					if (datapoint === 0) {
						new_headerline = _('date')+', '+_('min')+', '+_('max')+', '+_('unit')+', '+_('type');
						$.each(graphs[series].included_variables,function(e,v) {
							new_headerline += ', '+_(e);
						});
						if (! (new_headerline == headerline)) {
							html += '\n';
							html += new_headerline + '\n';
							headerline = new_headerline;
						}
					}
					var date = graphs[series]['max_data'][datapoint][0];
					var date_str = date_string(date);
					var max = graphs[series]['max_data'][datapoint][1];
					var min;
					if (String(date) in graphs[series].min_data_dic) {
						min = graphs[series]['min_data_dic'][String(date)];
					} else {
						min = max;
					}
					html += date_str + ', ' + min + ', ' + max + ', ' + graphs[series].unit + ', ' + graphs[series].type;
					$.each(graphs[series].included_variables,function(e,v) {
						html += ', '+v;
					});
					html += '\n';
				}
			} else {
				for (datapoint = 0; datapoint < graphs[series].data.length; ++datapoint) {
					if (datapoint === 0) {
						new_headerline = _('date')+', '+_('value')+', '+_('unit')+', '+_('type');
						$.each(graphs[series].included_variables,function(e,v) {
							new_headerline += ', '+_(e);
						});
						if (! (new_headerline == headerline)) {
							html += '\n';
							html += new_headerline + '\n';
							headerline = new_headerline;
						}
					}
					date = date_string(graphs[series]['data'][datapoint][0]);
					html += date + ', ' + graphs[series]['data'][datapoint][1] + ', ' + graphs[series].unit + ', ' + graphs[series].type;
					$.each(graphs[series].included_variables,function(e,v) {
						new_headerline += ', '+v;
					});
					html += '\n';
				}
			}
		}
		return html;
	}
	function unbind_some() {
		$('#' + query_id + 'stats').unbind('plotselected');
		$('#' + query_id + 'stats').unbind('plotclick');
		$('#' + query_id + 'statsoverview').unbind('plotselected');
		$('div#' + query_id + 'legend input.dataseries').die('click');
		return true;
	}
	function unbind_all() {
		$('#'+query_id+'graph_export_dialog').dialog('destroy');
		$('#'+query_id+'graph_wiki_dialog').dialog('destroy');
		$('#'+query_id+'graph_link_dialog').dialog('destroy');
		$('#'+query_id+'graph_tables_dialog').dialog('destroy');
		$('#' + query_id + 'graph_wiki').die('click');
		$('#' + query_id + 'graph_link').die('click');
		$('#' + query_id + 'graph_close').die('click');
		$('#' + query_id + 'graph_export').die('click');
		unbind_some();
		return true;
	}
	function destroy_some_globals() {
		$('#' + query_id + 'graph_switchmode').unbind('click');
		$('#' + query_id + 'reset').die('click');
	}

	function destroy_all_globals() {
		destroy_some_globals();
		query_id = id = headline = comment_counter = plot = has_comments = comments = datapoint_dictionary = graph_height = null;
		raw_graphs = converted_graphs = dollargraphs = eurographs = normalized_graphs = normalized_dollargraphs = normalized_eurographs = null;
	}

	function ranges_to_axis_dic(ranges) {
		var axis_dic = {
			xaxis: [{
				min: ranges.xaxis[0].from,
				max: ranges.xaxis[0].to
			}],
			yaxis: [
			]};
		for (i in ranges.yaxis) {
			axis_dic.yaxis.push({
				min: ranges.yaxis[i].from,
				max: ranges.yaxis[i].to
			});
		}
		return axis_dic;
	}

	function axis_dic_to_ranges(axis_dic) {
		var ranges = {
			xaxis: [{
				from: axis_dic.xaxis[0].min,
				to: axis_dic.xaxis[0].max
			}]
		};
		if ('yaxis' in axis_dic) {
			ranges.yaxis = [{
				from: axis_dic.yaxis[0].min,
				to: axis_dic.yaxis[0].max
			}];
			//ranges.yaxis=[];
			//for (i in axis_dic.yaxis) {
			//	ranges.yaxis.push({
			//		from: axis_dic.yaxis[i].min,
			//		to: axis_dic.yaxis[i].max
			//	});
			//}
		}
		return ranges;
	}

	function make_graphs() {
		var axis_dic = false;
		var options, overview_options, overview;
		options = {
			xaxis: [{
				mode: 'unixtime',
				minTickSize: [1, 'day'],
				monthNames: [_('Jan'), _("Feb"), _("Mar"), _("Apr"), _("May"), _("Jun"), _("Jul"), _("Aug"), _("Sep"), _("Oct"), _("Nov"), _("Dec")]
			}],
			yaxis: [],
			legend: {
				container: '#' + query_id + 'legend'
			},
			points: {
				show: true,
				drawCall: drawPoint
			},
			selection: {
				mode: 'xy'
			}
		};
		for (i=0;i<total_yaxis;i++) {
			eval('options.yaxis.push({tickFormatter: function(v, axis) {return v.toFixed(axis.tickDecimals) + graphs.yaxis['+String(i)+'];}});');
		}
		if (editor_mode) {
			options.legend.checkboxes = true;
		} else {
			options.legend.checkboxes = false;
		}
		if ((user_logged_in) && (editor_mode)) {
			options.grid = {
				hoverable: true,
				clickable: true
			};
		}
		plot = $.plot($('#' + query_id + 'stats'), graphs, options);
		if (editor_mode) {
			overview_options = {
				lines: {
					lineWidth: 1
				},
				points: {
					show: false
				},
				legend: {
					show: false
				},
				shadowSize: 0,
				xaxis: [{
					ticks: [],
					mode: 'unixtime'
				}],
				yaxis: [{
					ticks: []
				},
				{
					ticks: []
				}],
				selection: {
					mode: 'xy'
				}
			};
			options.legend.show = false; // don't redraw legend on graph redraw
			overview = $.plot($('#' + query_id + 'statsoverview'), graphs, overview_options);
			build_comment_accordion();
		}
		graph_height = $('#' + query_id).height();

		function draw_resetbutton() {
			var reset_button_right;
			//find position of tick labels:
			$('#' + query_id + ' .tickLabels .tickLabel').each(function() {
				if ($(this).css('text-align') == 'right') {
					reset_button_right = parseInt($(this).css('right'), 10) - 25;
				} //not perfect, because I'm going through all tick labels
			});
			$('#' + query_id + 'stats').append('<span id="' + query_id + 'reset" class="resetbutton link" style="right:' + reset_button_right + 'px;" ><span class="ui-icon ui-icon-arrow-4-diag"></span></span>');
		}

		$('#' + query_id + 'stats').bind('plotselected',
		function(event, ranges) {
			reset_comments();
			// clamp the zooming to prevent eternal zoom
			if (ranges.xaxis[0].to - ranges.xaxis[0].from < 0.00001) {
				ranges.xaxis[0].to = ranges.xaxis[0].from + 0.00001;
			}
			if (ranges.yaxis[0].to - ranges.yaxis[0].from < 0.00001) {
				ranges.yaxis[0].to = ranges.yaxis[0].from + 0.00001;
			}
			// do the zooming
			axis_dic = ranges_to_axis_dic(ranges);
			plot = $.plot($('#' + query_id + 'stats'), graphs, $.extend(true, {},
			options, axis_dic));
			// don't fire event on the overview to prevent eternal loop
			draw_resetbutton();
			if (editor_mode) {
				overview.clearSelection(true);
				overview.setSelection(ranges, true);
				build_comment_accordion();
			}
		});
		if (editor_mode) {
			$('select.' + query_id + 'graphkind').change(function() {
				var xunits;
				var xunits_selector = $('select#' + query_id + 'xunits');
				if (xunits_selector.length > 0) {
					xunits = xunits_selector.val();
				} else {
					xunits = 'other';
				}
				var xtype = $('select#' + query_id + 'xtype').val();
				if ((xunits == 'cordobas' || xunits == 'other') && xtype == 'real') {
					graphs = converted_graphs;
				} else if (xunits == 'dollars' && xtype == 'real') {
					graphs = dollargraphs;
				} else if (xunits == 'euros' && xtype == 'real') {
					graphs = eurographs;
				} else if ((xunits == 'cordobas' || xunits == 'other') && xtype == 'normalized') {
					graphs = normalized_graphs;
				} else if (xunits == 'dollars' && xtype == 'normalized') {
					graphs = normalized_dollargraphs;
				} else if (xunits == 'euros' && xtype == 'normalized') {
					graphs = normalized_eurographs;
				} else {
					graphs = converted_graphs;
				}
				options.legend.show = true; //redraw legend for new type graph
				reset_comments();
				overview = $.plot($('#' + query_id + 'statsoverview'), graphs, overview_options);
				if (axis_dic) {
					delete axis_dic.yaxis;
					//if ('y2axis' in axis_dic) {
					//	delete axis_dic.y2axis;
					//}
					plot = $.plot($('#' + query_id + 'stats'), graphs, $.extend(true, {},
					options, axis_dic));
					axis_dic = plot.getAxes();
					overview.setSelection(axis_dic_to_ranges(axis_dic));
				} else {
					plot = $.plot($('#' + query_id + 'stats'), graphs, options);
				}
				build_comment_accordion();
				options.legend.show = false; // don't redraw legend on graph redraw
			});

			$('#' + query_id + 'statsoverview').bind('plotselected',
			function(event, ranges) {
				reset_comments();
				plot.setSelection(ranges);
				build_comment_accordion();
			});

			$('div#' + query_id + 'legend input.dataseries').live('click',
			function() {
				var state = $(this).attr('checked');
				var color_value = parseInt($(this).attr('name'), 10);
				for (i in converted_graphs) {
					if (converted_graphs[i].color == color_value) {
						converted_graphs[i].show = state;
					}
				}
				for (i in eurographs) {
					if (eurographs[i].color == color_value) {
						eurographs[i].show = state;
					}
				}
				for (i in dollargraphs) {
					if (dollargraphs[i].color == color_value) {
						dollargraphs[i].show = state;
					}
				}
				for (i in normalized_graphs) {
					if (normalized_graphs[i].color == color_value) {
						normalized_graphs[i].show = state;
					}
				}
				for (i in normalized_eurographs) {
					if (normalized_eurographs[i].color == color_value) {
						normalized_eurographs[i].show = state;
					}
				}
				for (i in normalized_dollargraphs) {
					if (normalized_dollargraphs[i].color == color_value) {
						normalized_dollargraphs[i].show = state;
					}
				}
				reset_comments();
				overview = $.plot($('#' + query_id + 'statsoverview'), graphs, overview_options);
				if (axis_dic) {
					plot = $.plot($('#' + query_id + 'stats'), graphs, $.extend(true, {},
					options, axis_dic));
					var ranges = axis_dic_to_ranges(axis_dic);
					overview.setSelection(ranges, true);
				} else {
					plot = $.plot($('#' + query_id + 'stats'), graphs, options);
				}
				build_comment_accordion();
				if (axis_dic) {
					draw_resetbutton();
				}
			});
			$('#' + query_id + 'stats').bind('plotclick',
			function(event, pos, item) {
				if (item) {
					create_comment_form(item.datapoint[2]);
				}
			});
		}
		$('#' + query_id + 'reset').live('click',
		function() {
			reset_comments();
			axis_dic = false;
			plot = $.plot($('#' + query_id + 'stats'), graphs, options);
			if (editor_mode) {
				overview.clearSelection(true);
				build_comment_accordion();
			}
		});
		$('#' + query_id + 'graph_switchmode').bind('click',
		function() {
			var total_width;
			if (editor_mode) {
				total_width = (($(graphsheader).innerWidth() - 95) / 2);
			} else {
				total_width = $(graphsheader).innerWidth() - 20;
			}
			$('#' + query_id).animate({
				width: total_width + 'px'
			},
			3000);
			reset_comments();
			axis_dic = false;
			var new_text;
			if (editor_mode) {
				editor_mode = false;
				new_text = draw_small_inner_graph_structure(total_width);
			} else {
				editor_mode = true;
				new_text = draw_inner_graph_structure(total_width);
			}
			unbind_some();
			destroy_some_globals();
			$('#' + query_id).empty();
			$('#' + query_id).css('width', total_width + 'px');
			$('#' + query_id).append(new_text);
			make_graphs();
		});

	}

}
