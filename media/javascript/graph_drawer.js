var e_msg, errors;

function create_graphs(jsondata,close_button,graphsheader) {
	var query_id, id, headline, comment_counter, has_comments, plot, comment_form_open, comments, datapoint_dictionary, graph_height, graph_margin_bottom;
	var raw_graphs, converted_graphs, dollargraphs, eurographs, normalized_graphs, normalized_dollargraphs, normalized_eurographs,color_counter=0,all_lluvias,all_mercados,all_productos;
	comment_form_open = false;
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
		e_msg = "No hay datos para la seleccion!";
		$('#AjaxFormWarning').text(e_msg).fadeIn("slow");
		$('#AjaxFormSubmit').attr("disabled", "");
		return true;
	}
	datapoint_dictionary = calculate_datapoint_dictionary(converted_graphs);
	headline = jsondata.headline;
	var yaxis=converted_graphs.yaxis,y2axis=converted_graphs.y2axis;
	if (all_productos.length>1) {
		var median_producto_graphs=calculate_mediangraphs(converted_graphs,'producto');
		converted_graphs=converted_graphs.concat(median_producto_graphs);
	}
	if (all_mercados.length>1) {
		var median_mercado_graphs=calculate_mediangraphs(converted_graphs,'mercado');
		converted_graphs=converted_graphs.concat(median_mercado_graphs);
		if (all_productos.length>1) {
			for (i in median_mercado_graphs) {
				median_mercado_graphs[i].producto='1';
				median_mercado_graphs[i].relevance='main';
			}
			var median_mercado_producto_graphs=calculate_mediangraphs(median_mercado_graphs,'producto');
			if (median_mercado_producto_graphs.length>0) {
				median_mercado_producto_graphs[0].advanced_label='mediano de todos los mercados y todos los productos';
				median_mercado_producto_graphs[0].label='mediano de todos los mercados y todos los productos (cordoba)';
				median_mercado_producto_graphs[0].producto=null;
				converted_graphs=converted_graphs.concat(median_mercado_producto_graphs);
			}
		}
	}
	converted_graphs.yaxis=yaxis;
	converted_graphs.y2axis=y2axis;
	query_id = String(new Date().getTime());
	var graph_html = draw_graph_structure(query_id, headline, has_comments, user_can_add, user_logged_in);
	$(graphsheader).after(graph_html);

	make_graphs(converted_graphs);
	e_msg = "Nuevo gráfico generado.";

	//Show the message
	$('#AjaxFormWarning').text(e_msg).fadeIn("slow");

	//Calculate other graphs	
	normalized_graphs = calculate_normalizedgraphs(converted_graphs);

	if (all_productos.length>0) {
		dollargraphs = calculate_currencygraphs(eval(jsondata.dollar), converted_graphs);
		eurographs = calculate_currencygraphs(eval(jsondata.euro), converted_graphs);
		normalized_dollargraphs = calculate_normalizedgraphs(dollargraphs);
		normalized_eurographs = calculate_normalizedgraphs(eurographs);
	}

	$("select." + query_id + "graphkind").change(function() {
		var xunits;
		var xunits_selector = $("select#" + query_id + "xunits");
		if (xunits_selector.length > 0) {
			xunits = xunits_selector.val();
		} else {
			xunits = 'other';
		}
		var xtype = $("select#" + query_id + "xtype").val();
		if ((xunits == 'cordobas' || xunits == 'other') && xtype == 'real') {
			make_graphs(converted_graphs);
		} else if (xunits == 'dollars' && xtype == 'real') {
			make_graphs(dollargraphs);
		} else if (xunits == 'euros' && xtype == 'real') {
			make_graphs(eurographs);
		} else if ((xunits == 'cordobas' || xunits == 'other') && xtype == 'normalized') {
			make_graphs(normalized_graphs);
		} else if (xunits == 'dollars' && xtype == 'normalized') {
			make_graphs(normalized_dollargraphs);
		} else if (xunits == 'euros' && xtype == 'normalized') {
			make_graphs(normalized_eurographs);
		} else {
			make_graphs(converted_graphs);
		}
	});

	if ($.browser.msie) {
		$("div.graph").remove();
	}

	function convert_graphs_after_transport(graphs) {
		var new_graphs, tipos_graficos;
		new_graphs = [];
		tipos_graficos = {};
		all_productos = [];
		all_mercados = [];
		all_lluvias = [];
		$.each(graphs,
		function() {
			var data = [],
			new_data = [],
			new_fill_data = [],
			new_shadow_data = [],
			max_data = [],
			min_data_dic = {},
			tipo,
			unit,
			producto,
			mercado,
			lluvia,
			label,
			start_value,
			start_date;
			if ('data' in this) {
				data = this.data;
			} else {
				max_data = this.max_data;
				min_data_dic = this.min_data_dic;
			}
			unit = this.unit;
			tipo = this.tipo;
			if (tipo == 'precio') {
				producto = this.producto;
				mercado = this.mercado;
				if (!(producto in all_productos)) {
					all_productos.push(producto);
				}
				if (!(mercado in all_mercados)) {
					all_mercados.push(mercado);
				}
				label = producto + ' en ' + mercado + ' (' + unit + ')';
			} else if (tipo == 'lluvia') {
				lluvia = this.lluvia;
				if (!(lluvia in all_lluvias)) {
					all_lluvias.push(lluvia);
				}
				label = 'lluvia en ' + lluvia + ' (' + unit + ')';
			} else {
				label = '';
			}
			if (! (tipo in tipos_graficos)) {
				tipos_graficos[tipo] = unit;
			}
			if (data.length > 0) {
				start_value = data[0][1];
				start_date = data[0][0];
				$.each(data,
				function() {
					var pk, value, time, new_time;
					time = this[0];
					new_time = time * 1000000; //add 7 zeroes to end of time string
					value = this[1];
					pk = this[2];
					new_data.push([new_time, value, pk]);
				});
			} else {
				start_value = max_data[0][1];
				start_date = max_data[0][0];
				var new_max_data = [],
				new_min_data = [];
				$.each(max_data,
				function() {
					var pk, max_value, min_value, time, new_time;
					time = this[0];
					new_time = time * 1000000; //add 7 zeroes to end of time string
					max_value = this[1];
					pk = this[2];
					if (String(time) in min_data_dic) {
						min_value = min_data_dic[String(time)];
					} else {
						min_value = max_value;
					}
					new_min_data.push([new_time, min_value, pk]);
					new_max_data.push([new_time, max_value, pk]);
				});
				new_fill_data = new_min_data.concat(new_max_data.reverse());
				new_shadow_data = new_min_data;
				new_data = new_max_data.reverse();
			}
			var graph_yaxis = 1;
			var yaxis_finder = 1;
			for (var item in tipos_graficos) {
				if (item == tipo) {
					graph_yaxis = yaxis_finder;
				}
				yaxis_finder += 1;
			}
			var new_graph = {
				'label': label,
				'data': new_data,
				'unit': unit,
				'yaxis': graph_yaxis,
				'tipo': tipo,
				'relevance': 'main',
				'color': color_counter,
				'clickable': {},
				'hoverable': {},
				'bars': {},
				'lines': {},
				'points': {},
				'start_value': start_value,
				'start_date': start_date
			};
			if (tipo == 'precio') {
				new_graph.lines = {
					'show': true
				};
				new_graph.producto = producto;
				new_graph.mercado = mercado;
			} else if (tipo == 'lluvia') {
				new_graph.bars = {
					'show': true,
					'barWidth': 86400000
				};
				new_graph.lluvia = lluvia;
			}
			if (new_fill_data.length > 0) {
				new_graph.shadowSize = 0;
				var new_fill_graph = {
					'data': new_fill_data,
					'unit': unit,
					'yaxis': yaxis,
					'tipo': tipo,
					'relevance': 'fill',
					'color': color_counter,
					'hoverable': false,
					'clickable': false,
					'shadowSize': 0,
					'bars': {},
					'points': {
						'show': false
					},
					'lines': {
						'fill': true
					},
					'start_value': start_value,
					'start_date': start_date
				};
				new_graphs.push(new_fill_graph);
				var new_shadow_graph = {
					'data': new_shadow_data,
					'unit': unit,
					'yaxis': yaxis,
					'tipo': tipo,
					'relevance': 'shadow',
					'color': color_counter,
					'hoverable': false,
					'clickable': false,
					'bars': {},
					'points': {
						'show': false
					},
					'lines': {},
					'shadowSize': 3,
					'start_value': start_value,
					'start_date': start_date
				};
				new_graphs.push(new_shadow_graph);
			}
			new_graphs.push(new_graph);
			color_counter += 1;
		});
		var yaxis = '',
		y2axis = '';
		var yaxis_finder = 1;
		for (var item in tipos_graficos) {
			if (yaxis_finder == 1) {
				yaxis = tipos_graficos[item];
			} else if (yaxis_finder == 2) {
				y2axis = tipos_graficos[item];
			}
			yaxis_finder += 1;
		}
		new_graphs.yaxis = yaxis;
		new_graphs.y2axis = y2axis;
		return new_graphs;
	}

	function calculate_currencygraphs(currency_dic, cordobagraphs) {
		var new_graphs = [];
		var tipos_graficos = {};
		$.each(cordobagraphs,
		function() {
			var label = '',
			mercado, producto, lluvia, current_data, current_unit;
			var data = this.data;
			var unit = this.unit;
			var tipo = this.tipo;
			var color = this.color;
			var lines = this.lines;
			var points = this.points;
			var bars = this.bars;
			var relevance = this.relevance;
			var clickable = this.clickable;
			var hoverable = this.hoverable;
			var shadowSize = this.shadowSize;
			var start_date = this.start_date;
			var start_value = currency_dic[String(start_date)] * this.start_value;
			if (unit == 'cordoba') {
				var currency_data = [];
				$.each(data,
				function() {
					var time = this[0];
					var cordoba = this[1];
					var pk = this[2];
					var currency = currency_dic[String(time / 1000000)]; //convert to transfer time format to get currency timestamp
					var currency_value = parseFloat(cordoba) * parseFloat(currency);
					currency_data.push([time, currency_value, pk]);
				});

				current_data = currency_data;
				current_unit = currency_dic.unit;
			} else {
				current_data = data;
				current_unit = unit;
			}
			if (tipo == 'precio') {
				producto = this.producto;
				mercado = this.mercado;
				if (relevance == 'main') {
					label = producto + ' en ' + mercado + ' (' + current_unit + ')';
				}
			} else if (tipo == 'lluvia') {
				lluvia = this.lluvia;
				if (relevance == 'main') {
					label = 'lluvia en ' + lluvia + ' (' + current_unit + ')';
				}
			}
			if ('advanced_label' in this) {
				label = this.advanced_label+' ('+current_unit+')';
			}
			if (! (tipo in tipos_graficos)) {
				tipos_graficos[tipo] = current_unit;
			}
			var yaxis = 1;
			var yaxis_finder = 1;
			for (var item in tipos_graficos) {
				if (item == tipo) {
					yaxis = yaxis_finder;
				}
				yaxis_finder += 1;
			}
			var new_graph = {
				'label': label,
				'data': current_data,
				'unit': current_unit,
				'tipo': tipo,
				'yaxis': yaxis,
				'points': points,
				'lines': lines,
				'bars': bars,
				'color': color,
				'relevance': relevance,
				'start_date': start_date,
				'start_value': start_value,
				'shadowSize': shadowSize,
				'clickable': clickable,
				'hoverable': hoverable
			};
			if (tipo == 'precio') {
				new_graph.producto = producto;
				new_graph.mercado = mercado;
			} else if (tipo == 'lluvia') {
				new_graph.lluvia = lluvia;
			}
			if ('advanced_label' in this) {
				new_graph.advanced_label=this.advanced_label;
			}
			new_graphs.push(new_graph);
		});
		var yaxis = "",
		y2axis = "";
		var yaxis_finder = 1;
		for (var item in tipos_graficos) {
			if (yaxis_finder == 1) {
				yaxis = tipos_graficos[item];
			} else if (yaxis_finder == 2) {
				y2axis = tipos_graficos[item];
			}
			yaxis_finder += 1;
		}
		new_graphs.yaxis = yaxis;
		new_graphs.y2axis = y2axis;
		return new_graphs.sort();
	}
	function calculate_mediangraphs(cordobagraphs,median_variable) {
		var graph_dic= {};
		$.each(cordobagraphs, function() {
			if ((median_variable in this) && (this.relevance=='main')) {
				if (this[median_variable] in graph_dic) {
					graph_dic[this[median_variable]].push(this);
				} else {
					graph_dic[this[median_variable]]=[this];
				}
			}
		});
		var new_graphs_list=[],graph_time_dic,graph_counter,empty_values,data_string,value_string,graph_counter,time_item,counter,search_counter,i,median_value,start_value,start_date;
		var graph_time_data,graph_time_data_list,date_item,graph_item,median_variable_item,new_graph,total_value;
		for (median_variable_item in graph_dic) {
			if (graph_dic[median_variable_item].length > 1) {
				graph_time_dic={};
				graph_counter=0;
				empty_values=0;
				for (graph_item in graph_dic[median_variable_item]) {
					for (date_item in graph_dic[median_variable_item][graph_item]['data']) {
						data_string=graph_dic[median_variable_item][graph_item]['data'][date_item][0];
						value_string=graph_dic[median_variable_item][graph_item]['data'][date_item][1];
						if (data_string in graph_time_dic) {
							empty_values=graph_counter - graph_time_dic[data_string].length;
						} else {
							if (graph_counter===0) {
								graph_time_dic[data_string]=[value_string];
								empty_values=-1;
							} else {
								graph_time_dic[data_string]=[null];
								empty_values=graph_counter-1;
							}
						}
						if (empty_values>-1) {
							for ( i = 0 ; i < empty_values ; i++ ) {
								graph_time_dic[data_string].push(null);
							}
							graph_time_dic[data_string].push(value_string);
						}
					}
					graph_counter+=1;
				}
				graph_counter-=1;
				for (time_item in graph_time_dic) { // filling in zeroes (null) at end
					empty_values=(graph_counter+1)-graph_time_dic[time_item].length;
					for ( i = 0 ; i < empty_values ; i++ ) {
						graph_time_dic[time_item].push(null);
					}
				} 
				graph_time_data_list=[];
				for (time_item in graph_time_dic) {
					graph_time_data_list.push([time_item,graph_time_dic[time_item]]);
				}
				graph_time_data_list=graph_time_data_list.sort();
				graph_time_data=[];
				for ( counter = 0 ; counter < graph_time_data_list.length ; counter++ ) {
					total_value=0;
					for (i in graph_time_data_list[counter][1]) {
						if (graph_time_data_list[counter][1][i]==null) {
							if (counter===0) {
								for ( search_counter = 0; search_counter < graph_time_data_list.length ; search_counter++) {
									if (!(graph_time_data_list[search_counter][1][i]==null)) {
										graph_time_data_list[0][1][i]=graph_time_data_list[search_counter][1][i];									
										break;
									}
								}
							} else {
								graph_time_data_list[counter][1][i]=graph_time_data_list[counter-1][1][i];
							}
						} 
						total_value+=graph_time_data_list[counter][1][i];						
					} 
					median_value=total_value/(graph_counter+1);
					graph_time_data.push([parseInt(graph_time_data_list[counter][0]),median_value]);
					if (counter===0) {
						start_value=median_value;
						start_date=parseInt(graph_time_data_list[counter][0])/1000000;
					}
				}
				var model_graph=graph_dic[median_variable_item][0];
				new_graph={
					'points': {
                                		'show': false
                                	},
                                	'lines': {
						'show':true,
                                		'fill': false
                                	},
					'hoverable': false,
					'clickable': false,		
					'start_date': start_date,		
					'start_value': start_value,		
					'unit': model_graph.unit,
					'tipo': model_graph.tipo,
					'yaxis': model_graph.yaxis,
					'relevance': 'mediano',
					'color': color_counter
				};
				color_counter += 1;
				new_graph.data=graph_time_data;
				new_graph[median_variable]=median_variable_item;
				new_graph.label=median_variable_item+" mediano ("+model_graph.unit+")";
				new_graph.advanced_label=median_variable_item+" mediano";
				new_graphs_list.push(new_graph);
			}
		}
		return new_graphs_list;
		
	}

	function calculate_normalizedgraphs(unitgraphs) {
		var new_graphs = [];
		$.each(unitgraphs,
		function() {
			var new_data = [],
			producto,
			mercado,
			lluvia;
			var label = '';
			var data = this.data;
			var unit = this.unit;
			var tipo = this.tipo;
			var color = this.color;
			var bars = this.bars;
			var lines = this.lines;
			var points = this.points;
			var relevance = this.relevance;
			var shadowSize = this.shadowSize;
			var clickable = this.clickable;
			var hoverable = this.hoverable;
			var start_value = this.start_value;
			if ((relevance == 'main') || (relevance == 'mediano')){
				if ('advanced_label' in this) {
					label = this.advanced_label+' (1 = ' + String(start_value) + ' ' + unit +'s)';
				} else if (tipo == 'precio') {
					producto = this.producto;
					mercado = this.mercado;
					if (relevance == 'main') {
						label = producto + ' en ' + mercado + ' (1 = ' + String(start_value) + ' ' + unit + 's)';
					}
				} else if (tipo == 'lluvia') {
					lluvia = this.lluvia;
					if (relevance == 'main') {
						label = 'lluvia en ' + lluvia + ' (1 = ' + String(start_value) + ' ' + unit + 's)';
					}
				}

			}
			$.each(data,
			function() {
				var time = this[0];
				var unit_value = this[1];
				var pk = this[2];
				var normalized_value = parseFloat(unit_value) / parseFloat(start_value) * 100;
				new_data.push([time, normalized_value, pk]);
			});
			var new_graph = {
				'label': label,
				'data': new_data,
				'unit': '%',
				'tipo': 'normalizado',
				'yaxis': 1,
				'bars': bars,
				'points': points,
				'lines': lines,
				'color': color,
				'relevance': relevance,
				'shadowSize': shadowSize,
				'clickable': clickable,
				'hoverable': hoverable
			};
			new_graphs.push(new_graph);
		});
		new_graphs.yaxis = '%';
		new_graphs.y2axis = '';
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
	var labelCanvas = false;
	function drawPoint(ctx, x, y, radius, fillStyle, plotOffset, dataitem, series) {
		var unique_pk = dataitem[2];
		if (eval(has_comments) && unique_pk in comments) {
			if (! (labelCanvas)) {
				var canvasHeight = $('#' + query_id + 'stats canvas:first').outerHeight();
				var canvasWidth = $('#' + query_id + 'stats canvas:first').outerWidth();
				var canvas = $(makeLabelCanvas(canvasWidth, canvasHeight)).css({
					position: 'absolute',
					left: 0,
					top: 0
				}).insertAfter('#' + query_id + 'stats canvas:first').get(0);
				labelCanvas = canvas.getContext("2d");
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
			var comments_text = "";
			for (var comment_pk in comments[unique_pk]) {
				if (comments[unique_pk][comment_pk][3] === true) {
					comments_text += '<div class="publicComment">';
				} else {
					comments_text += '<div class="nonpublicComment">';
				}
				if (comments[unique_pk][comment_pk][2] === true) {
					comments_text += '<p class="editline"><span class="link" id="' + unique_pk + '+' + comment_pk + '+' + query_id + '">Editar</span></p>';
				}
				comments_text += "<p>" + comments[unique_pk][comment_pk][0] + "</p>";
				comments_text += "<p class=\"signature\">" + comments[unique_pk][comment_pk][1] + "</p>";
				comments_text += '</div>';
			}

			$("#" + query_id + "comments").append("<tr class=\"comment\" id=\"" + query_id + "_" + unique_pk + "comments\"><td valign=\"top\"><b>" + label + "</b></td><td valign=\"top\">" + comments_text + "</td></tr>");
			$('<div class="pointLabel" id="' + query_id + '_' + unique_pk + 'label">' + label + '</div>').insertAfter('#' + query_id + 'labelcanvas');
			var editButtons = $('#' + query_id + '_' + unique_pk + 'comments p.editline span');
			editButtons.bind("click",
			function() {
				var total_pk, this_unique_pk, this_comment_pk;
				if (! (comment_form_open)) {
					total_pk = $(this).attr('id').split('+');
					this_unique_pk = total_pk[0];
					this_comment_pk = total_pk[1];
					create_comment_form(this_unique_pk, this_comment_pk);
				}
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
		var comment, content_type, form_info, object_pk, pk_array, timestamp;
		comment_form_open = true;
		timestamp = parseInt(new Date().getTime().toString().substring(0, 10), 10);
		if (comment_pk) {
			var comment_text = comments[unique_pk][comment_pk][0];
		}
		var label = datapoint_dictionary[unique_pk][3];
		if (label.length === 0) {
			label = 'producto';
		}
		var value = datapoint_dictionary[unique_pk][1];
		var raw_date = datapoint_dictionary[unique_pk][0];
		var date = date_string(raw_date);

		var s = '';
		s += '<div class="formDiv" id="' + query_id + 'formDiv">';
		if (comment_pk) {
			s += '  <strong>Editar Comentario</strong><br /><br />';
		} else {
			s += '  <strong>Nuevo Comentario</strong><br /><br />';
		}
		s += '  <strong>' + label + ': ' + value + ' (' + date + ')</strong><br /><br />';
		s += '  <form name="newcomment" id="' + query_id + 'newcomment" method="post">';
		if (comment_pk) {
			s += '  <input type="hidden" name="comment_pk" id="' + query_id + 'comment_pk" value="' + comment_pk + '">';
		}
		s += '  <input type="hidden" name="timestamp" id="' + query_id + 'timestamp_field" value="' + timestamp + '">';
		s += '  <input type="hidden" name="honeypot" id="' + query_id + 'honeypot_field" value="">';
		s += '  <textarea id="' + query_id + 'comment_field" name="comment" rows="10" cols="40" name="comment" class="vLargeTextField">';
		if (comment_text) {
			s += comment_text;
		}
		s += '</textarea>';
		s += '  <div id ="' + query_id + 'formDivMessage">&nbsp;</div>';
		s += '  <input type="button" name="btnSave" id="' + query_id + 'btnSave" value="Guardar"><input type="button" name="btnCancel" id="' + query_id + 'btnCancel" value="Cancelar">';
		if (comment_pk) {
			s += '  <input type="button" name="btnDelete" id="' + query_id + 'btnDelete" value="Borrar">';
		}
		s += '  </form>';
		s += '</div>';
		pk_array = unique_pk.split('_');
		content_type = pk_array[0];
		object_pk = pk_array[1];
		$("#" + query_id).append(s);
		$("#" + query_id + "btnSave").unbind(); // so other form doesn't get submitted
		form_info = {};
		$("#" + query_id + "btnCancel").click(function() {
			$("#" + query_id + "formDivMessage").html('Cancelando...');
			$("#" + query_id + "formDiv").fadeOut(300,
			function() {
				$(this).remove();
			});
			comment_form_open = false;
		});
		if (comment_pk) {
			$("#" + query_id + "btnDelete").click(function() {
				form_info = {
					object_pk: object_pk,
					content_type: content_type,
					remove: true,
					comment_pk: comment_pk
				};
				form_info.timestamp = $("#" + query_id + "timestamp_field").val();
				form_info.honeypot = $("#" + query_id + "honeypot_field").val();
				returnFormResponse(form_info, 'Borrando...', 'Borrado con exito!');
			});

		}
		$("#" + query_id + "btnSave").click(function() {
			comment = $("#" + query_id + "comment_field").val();
			form_info = {
				object_pk: object_pk,
				content_type: content_type,
				comment: comment
			};
			if (comment_pk) {
				form_info.comment_pk = comment_pk;
			}
			form_info.timestamp = $("#" + query_id + "timestamp_field").val();
			form_info.honeypot = $("#" + query_id + "honeypot_field").val();
			returnFormResponse(form_info, 'Guardando...', 'Guardado con exito!');
		});
		function returnFormResponse(fI, processMessage, successMessage) {
			$("#" + query_id + "btnSave").attr('disabled', 'disabled');
			$("#" + query_id + "btnDelete").attr('disabled', 'disabled');
			$("#" + query_id + "formDivMessage").html(processMessage);
			$.post('/ajax/comment/post/', fI,
			function(data) {
				if (data.status == "success") {
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
					$("#" + query_id + "formDivMessage").html(successMessage);
					$("#" + query_id + "formDiv").fadeOut(300,
					function() {
						$(this).remove();
					});
					comment_form_open = false;
				} else {
					$("#" + query_id + "formDivMessage").html('Hubo un error!');
					$("#" + query_id + "btnSave").attr('disabled', '');
					$("#" + query_id + "btnDelete").attr('disabled', '');
				}
				// The success or failure check will go here. . .
			},
			"json");
		}
	}
	graph_margin_bottom = 0;
	function correct_graphheight() {
		var comments_height;
		comments_height = $("#" + query_id + "comments").height();
		if (comments_height > graph_height) {
			graph_margin_bottom = comments_height - graph_height;
			$("#" + query_id).css('margin-bottom', graph_margin_bottom + 'px');
		} else if (graph_margin_bottom > 0) {
			graph_margin_bottom = 0;
			$("#" + query_id).css('margin-bottom', 0);
		}
	}
	function reset_comments(query_id) {
		labelCanvas = false;
		comment_counter = 0;
		$("#" + query_id + " tr.comment").remove();
		$("#" + query_id + "labelcanvas").remove();
		$("#" + query_id + " div.pointLabel").remove();
	}
	function redraw_graph() {
		reset_comments(query_id);
		plot.draw();
		correct_graphheight();
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
	function draw_graph_structure(query_id, headline, has_comments, user_can_add, user_logged_in) {
		var graph_margin = '';
		var comment_list = '';
		if (eval(has_comments) || user_can_add) {
			graph_margin = "200";
			comment_list = "<table id=\"" + query_id + "comments\" style=\"width:200px; position:absolute;right:0;top:0;\"><tr>";
			comment_list += "<th style=\"width:15px;\">&nbsp;</th><th style=\"width:185px;\">Comentarios</th></tr></table>";
		}
		var graph_html = '';
		graph_html += '<div id="' + query_id + '" class="graph" style="position:relative;">';
		graph_html += '<h2 id="' + query_id + 'headline" >';
		if (close_button) {
			graph_html += '<img id="' + query_id + 'close" src="/media/icons/close.png" /> ';
		}
		graph_html += headline;
		//                graph_html+=' <img id="'+query_id+'tablelink" src="/media/icons/spreadsheet.png"  />';
		//		graph_html+='<img src="/media/icons/print.png" />';
		graph_html += '</h2>';
		if (jsondata.query_link) {
			graph_html += '<p><a href="/estadisticas/'+jsondata.query_link+'" target+"_blank">enlace permanente</a></p>';
		}
		if (jsondata.wiki_code) {
			if (can_edit_wiki) {
				graph_html += '<p>Codigo para incluir en pagina de wiki:<br /><b>_estadisticas['+jsondata.wiki_code+']</b></p>';
			}
		}
		//		var icon_width=0;
		//                graph_html+="<img id=\""+query_id+"print\" src=\"/media/icons/print.png\"/ style=\"position:absolute;left:"+icon_width+"px;top:0px;\" />";
		//		icon_width+=18;
		//		if (user_logged_in) {
		//                	graph_html+="<img id=\""+query_id+"email\" src=\"/media/icons/email.png\"/ style=\"position:absolute;left:"+icon_width+"px;top:0px;\" />";
		//			icon_width+=18;
		//		}
		//		icon_width+=18;
		graph_html += "<div id=\"" + query_id + "stats\" style=\"height:400px; margin-right:" + graph_margin + "px;\"></div>";
		graph_html += comment_list;
		graph_html += "<div id=\"" + query_id + "statsoverview\" style=\"height:50px; margin-right:" + graph_margin + "px;\"></div>";
		graph_html += "<img id=\"" + query_id + "reset\" src=\"/media/icons/reset.png\" />";
		graph_html += "<select id=\"" + query_id + "xtype\" class=\"" + query_id + "graphkind\">";
		graph_html += "<option selected=\"selected\" value=\"real\">Real</option>";
		graph_html += "<option value=\"normalized\">Normalizado</option></select>";
		graph_html += " <span id=\"" + query_id + "csvexport\" class=\"link\">Exportar datos</span>";
		if (all_productos.length>0) {
			graph_html += '<br />Precios: ';
			graph_html += '<select id="' + query_id + 'xunits" class="' + query_id + 'graphkind"><option selected="selected" value="cordobas">Cordobas</option>';
			graph_html += '<option value="dollars">USD</option><option value="euros">Euros</option></select>';
			//if (all_productos.length>1) {
			//graph_html += '<input type="checkbox" id="'+query_id+'show_median_productos" class="graphkind" /> mediano de todos los productos';
			//}	
			//if (all_mercados.length>1) {
			//graph_html += '<input type="checkbox" id="'+query_id+'show_median_mercados" class="graphkind" /> mediano de todos los mercados';
			//}	
			//if ((all_mercados.length>1) && (all_productos.length>1)) {
			//graph_html += '<input type="checkbox" id="'+query_id+'show_median_productos_and_mercados" class="graphkind" /> mediano de todos los mercados y productos';
			//}	
			//graph_html += '<br />';
		}
		graph_html += "<div id=\"" + query_id + "legend\" style=\"margin-right:" + graph_margin + "px;\"></div></div>";
		return graph_html;
	}

	function date_string(timestamp) {
		var raw_date = new Date(timestamp);
		var day = raw_date.getUTCDate();
		if (day < 10) {
			day = "0" + day;
		}
		var month = raw_date.getUTCMonth() + 1;
		if (month < 10) {
			month = "0" + month;
		}
		var year = raw_date.getUTCFullYear();
		var formated_date_string = year + '-' + month + '-' + day;
		return formated_date_string;
	}
	function print_html(graphs) {
		return "";
	}

	function csv_export(graphs) {
		var html = "";
		var headerline = '',
		new_headerline;
		for (var series = 0; series < graphs.length; ++series) {
			var datapoint;
			if ('max_data' in graphs[series]) {
				for (datapoint = 0; datapoint < graphs[series].max_data.length; ++datapoint) {
					if (datapoint === 0) {
						new_headerline = 'fecha, min, max, unidad, tipo';
						if (graphs[series].tipo == 'precio') {
							new_headerline += ', mercado, producto';
						} else if (graphs[series].tipo == 'lluvia') {
							new_headerline += ', estacion de lluvia';
						}
						if (! (new_headerline == headerline)) {
							html += '\n';
							html += new_headerline + '\n';
							headerline = new_headerline;
						}
					}
					var date = graphs[series]['max_data'][datapoint][0];
					var date_str = date_string(date * 1000000);
					var max = graphs[series]['max_data'][datapoint][1];
					var min;
					if (String(date) in graphs[series].min_data_dic) {
						min = graphs[series]['min_data_dic'][String(date)];
					} else {
						min = max;
					}
					html += date_str + ', ' + min + ', ' + max + ', "' + graphs[series].unit + '", "' + graphs[series].tipo + '"';
					if (graphs[series].tipo == 'precio') {
						html += ', "' + graphs[series].mercado + '", "' + graphs[series].producto + '"';
					} else if (graphs[series].tipo == 'lluvia') {
						html += ', "' + graphs[series].lluvia + '"';
					}
					html += '\n';
				}
			} else {
				for (datapoint = 0; datapoint < graphs[series].data.length; ++datapoint) {
					if (datapoint === 0) {
						new_headerline = 'fecha, valor, unidad, tipo';
						if (graphs[series].tipo == 'precio') {
							new_headerline += ', mercado, producto';
						} else if (graphs[series].tipo == 'lluvia') {
							new_headerline += ', estacion de lluvia';
						}
						if (! (new_headerline == headerline)) {
							html += '\n';
							html += new_headerline + '\n';
							headerline = new_headerline;
						}
					}
					date = date_string(graphs[series]['data'][datapoint][0] * 1000000);
					html += date + ', ' + graphs[series]['data'][datapoint][1] + ', "' + graphs[series].unit + '", "' + graphs[series].tipo + '"';
					if (graphs[series].tipo == 'precio') {
						html += ', "' + graphs[series].mercado + '", "' + graphs[series].producto + '"';
					} else if (graphs[series].tipo == 'lluvia') {
						html += ', "' + graphs[series].lluvia + '"';
					}
					html += '\n';
				}
			}
		}
		return html;
	}
	function unbind_all(query_id) {
		$("#" + query_id + "stats").unbind("plotselected");
		$("#" + query_id + "statsoverview").unbind("plotselected");
		$("img#" + query_id + "reset").unbind("click");
		$("img#" + query_id + "print").unbind("click");
		$("img#" + query_id + "email").unbind("click");
		$("img#" + query_id + "close").unbind("click");
		$("span#" + query_id + "csvexport").unbind("click");
		return true;
	}
	function destroy_all_globals() {
		query_id = id = headline = comment_counter = has_comments = plot = comment_form_open = comments = datapoint_dictionary = graph_height = graph_margin_bottom = null;
		raw_graphs = converted_graphs = dollargraphs = eurographs = normalized_graphs = normalized_dollargraphs = normalized_eurographs = null;
	}
	function make_graphs(graphs) {
		reset_comments(query_id);
		//first unbind all earlier bindings
		unbind_all(query_id);
		current_graphs=graphs;
		var options, overview;
		options = {
			xaxis: {
				mode: "time",
				minTickSize: [1, "day"]
			},
			yaxis: {
				tickFormatter: function(v, axis) {
					return v.toFixed(axis.tickDecimals) + graphs.yaxis;
				}
			},
			y2axis: {
				tickFormatter: function(v, axis) {
					return v.toFixed(axis.tickDecimals) + graphs.y2axis;
				}
			},
			legend: {
				container: "#" + query_id + "legend"
			},
			points: {
				show: true,
				drawCall: drawPoint
			},
			selection: {
				mode: "xy"
			}
		};
		if (user_logged_in) {
			options.grid = {
				hoverable: true,
				clickable: true
			};
		}
		plot = $.plot($("#" + query_id + "stats"), graphs, options);
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
			xaxis: {
				ticks: [],
				mode: "time"
			},
			yaxis: {
				ticks: []
			},
			selection: {
				mode: "xy"
			}
		};
		overview = $.plot($("#" + query_id + "statsoverview"), graphs, overview_options);
		graph_height = $("#" + query_id).height();
		correct_graphheight();
		$("#" + query_id + "stats").bind("plotselected",
		function(event, ranges) {
			reset_comments(query_id);
			// clamp the zooming to prevent eternal zoom
			if (ranges.xaxis.to - ranges.xaxis.from < 0.00001) {
				ranges.xaxis.to = ranges.xaxis.from + 0.00001;
			}
			if (ranges.yaxis.to - ranges.yaxis.from < 0.00001) {
				ranges.yaxis.to = ranges.yaxis.from + 0.00001;
			}
			if ('y2axis' in ranges) {
				if (ranges.y2axis.to - ranges.y2axis.from < 0.00001) {
					ranges.yaxis.to = ranges.yaxis.from + 0.00001;
				}
			}
			// do the zooming
			var axis_dic = {
				xaxis: {
					min: ranges.xaxis.from,
					max: ranges.xaxis.to
				},
				yaxis: {
					min: ranges.yaxis.from,
					max: ranges.yaxis.to
				}
			};
			if ('y2axis' in ranges) {
				axis_dic.y2axis = {
					min: ranges.y2axis.from,
					max: ranges.y2axis.to
				};
			}

			plot = $.plot($("#" + query_id + "stats"), graphs, $.extend(true, {},
			options, axis_dic));
			// don't fire event on the overview to prevent eternal loop
			overview.clearSelection(true);
			overview.setSelection(ranges, true);
			correct_graphheight();
		});
		$("#" + query_id + "statsoverview").bind("plotselected",
		function(event, ranges) {
			reset_comments(query_id);
			plot.setSelection(ranges);
			correct_graphheight();
		});
		$("div#"+ query_id +"legend input.dataseries").live("click",function() {
			var state=$(this).attr('checked');
			var color_value=parseInt($(this).attr('name'));
			for (i in graphs) {
				if (graphs[i].color==color_value) {
					graphs[i].show=state;
				}
			}
			//current_graphs=graphs;
			reset_comments(query_id);
			plot = $.plot($("#" + query_id + "stats"), graphs, options);
			overview.clearSelection(true);
			overview = $.plot($("#" + query_id + "statsoverview"), graphs, overview_options);
			correct_graphheight();
			//alert(color_value+': '+state);
		});
		$("img#" + query_id + "reset").click(function() {
			reset_comments(query_id);
			plot = $.plot($("#" + query_id + "stats"), graphs, options);
			overview.clearSelection(true);
			correct_graphheight();
		});
		$("img#" + query_id + "close").click(function() {
			reset_comments(query_id);
			unbind_all(query_id);
			$("#" + query_id).fadeOut(300,
			function() {
				$(this).remove();
			});
			destroy_all_globals();
		});
		$("span#" + query_id + "csvexport").click(function(e) {
			// si el usuario ha utilizado una tecla de control
			// no hacemos nada
			if (e.ctrlKey || e.shiftKey || e.metaKey) {
				return;
			}
			// abrimos la ventana
			var w = window.open('', '_blank', '');
			if (w && !w.closed) {
				w.document.open("text/csv", "replace");
				w.document.write(csv_export(raw_graphs));
				w.document.close();
				// si efectivamente hemos logrado abrirla
				// la ponemos en foco
				w.focus();
				// y cancelamos el comportamiento por defecto
				// del enlace
				e.preventDefault();
			}

		});
		$("img#" + query_id + "print").click(function(e) {
			// si el usuario ha utilizado una tecla de control
			// no hacemos nada
			if (e.ctrlKey || e.shiftKey || e.metaKey) {
				return;
			}
			// abrimos la ventana
			var w = window.open('', query_id + '.csv', '');
			if (w && !w.closed) {
				w.document.write(print_html(graphs));
				w.document.close();
				// si efectivamente hemos logrado abrirla
				// la ponemos en foco
				w.focus();
				// y cancelamos el comportamiento por defecto
				// del enlace
				e.preventDefault();
			}

		});
		$("#" + query_id + "stats").bind("plotclick",
		function(event, pos, item) {
			if ((item) && (!(comment_form_open))) {
				create_comment_form(item.datapoint[2]);
			}
		});

	}

}
