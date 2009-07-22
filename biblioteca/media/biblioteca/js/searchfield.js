/* 

	SearchField 
	written by Alen Grakalic, provided by Css Globe (cssglobe.com)
	please visit http://cssglobe.com/post/1202/style-your-websites-search-field-with-jscss/ for more info
	
*/

this.searchfield = function(){
	
	// CONFIG 
	
	// this is id of the search field you want to add this script to. 
	// You can use your own id just make sure that it matches the search field in your html file.
	var id = "searchfield";
	
	// Text you want to set as a default value of your search field.
	var defaultText = "Busque por palabra clave...";	
	
	// set to either true or false
	// when set to true it will generate search suggestions list for search field based on content of variable below
	var suggestion = true;
	
	// static list of suggestion options, separated by comma
	// replace with your own
	var suggestionText = "abono, absoluto, accesible, agricultura, agro, alternativo, agua, ancho, alimento, amplio, animales, agricola, agropecuario, agroindustria, acuifero, bono, backup, banda ancha, banner, banana, buitre, bitmap, blog, blogger, bacalao, bookmark, bomba, bollo, browser, cache, cartucho, cartera, cascada , chat, chrome, click, client, clon, compatibilidad, datos, contenidos , contextual, convergencia, cookie, costo-por-click, costo-por-lanzamiento, crusar, cross-browser, cyber-espacio, distro, defecto, degradado, doblado, designado, directorio, diputados, dilatar, div, division, divina, documento tipo declaracion, doctype, documento, dominio, DNS server, dedo, donar, donacion, dolido, descargar, doble nucleo, dinamico HTML, e-commerce, email, elemento, encriptacion, favicon.ico, Filiar, FTP client, firewall, Fireworks, Flash, Flash Generador, flow chart, fold, font, frio, formulario, folklore, frame, fragil, frontal, gato, global , granulado, Grafico vectorial, Grafico de Interface, hack, hablar, higuero, hexadecimal, hits, host, hosting, hotspot, HTML, hueco, hierba, hueco, hyperlink, impermiable, i-mode, imagen, impresion, include, informacion, ir, inicialisacion, integracion, interactivo television, interface, internet, intercpcion, intranet, inicio, Internet Protocol, IP address, IP number, Internet Service Provider, JavaScript, Juntar, label, landing page, legacy content, link: absolute, relative, root, link farm, link rot, definition, ordered, unordered, listserv, logfiles, logfile analysis, look-and-feel, lossless compression, lossy compression, macron, mailing lists, markup, meta element, metadata, meta tag, mine-sweeping, MP3, MySQL, natural language, navigation, open source, optimise, optimisation, opt-in/opt-out, PageRank (PR), parasite economy, design pattern, perceived affordance, permission-based marketing, phishing, PHP: Hypertext Preprocessor, Portable Document Format, web portal, Pretty Good Privacy, pixel, plug-in, pop-up window, pop-under, Portable Network Graphic, prosumer, QuickTime, quirks mode, reciprocal links, referrer, referrer log, Really Simple Syndication, relative link, Realtime Transport Protocol, robot, robots file, robots.txt, rollover, disjointed rollover, root, root directory, root link, scan, scanning, schematic, SCM, SCP, search engine, search engine marketing, search engine optimisation, Section 508, Secure Sockets Certificate, semantic markup, server, sever-side/client-side, server-side include, session, session tracking, Shockwave, shopping-cart, shortcut icon, Simple Object Access Protocol, site feed, sitemap, smart tags, Synchronised Multimedia Integration Language, sniffer, spam, spim, spider, splash page, splash screen, spyware, standardista, standards-compliant/strict mode, status bar, sticky, streaming, streaming media, structured query language, stylesheet, system font, tags, tags/tagging, target, template, top-level navigation, topic path, traffic, transform gracefully, transparent GIF, trackback, typosquatter, Unicode, Unicode Transformation Format, Unified Modeling Language, Uniform Resource Identifier, Uniform Resource Locator, uploading, usability, user session, code standards, form input, vector, vector-based file, version control, viral marketing, virus, visual editor, web, Web 2.0, web accessibility, web-authoring, web browser, web font, typeface, web-log, web server logs, websafe colours, palette, web standards, WebTV, what-you-see-is-what-you-get, wireframe, Wireless Application Protocol, Wireless Markup Language, Worldwide Web, eXtensible Markup Language, XML schema"; 
	
	// END CONFIG (do not edit below this line, well unless you really, really want to change something :) )
	
	// Peace, 
	// Alen

	var field = document.getElementById(id);	
	var classInactive = "sf_inactive";
	var classActive = "sf_active";
	var classText = "sf_text";
	var classSuggestion = "sf_suggestion";
	this.safari = ((parseInt(navigator.productSub)>=20020000)&&(navigator.vendor.indexOf("Apple Computer")!=-1));
	if(field && !safari){
		field.value = defaultText;
		field.c = field.className;		
		field.className = field.c + " " + classInactive;
		field.onfocus = function(){
			this.className = this.c + " "  + classActive;
			this.value = (this.value == "" || this.value == defaultText) ?  "" : this.value;
		};
		field.onblur = function(){
			this.className = (this.value != "" && this.value != defaultText) ? this.c + " " +  classText : this.c + " " +  classInactive;
			this.value = (this.value != "" && this.value != defaultText) ?  this.value : defaultText;
			clearList();
		};
		if (suggestion){
			
			var selectedIndex = 0;
						
			field.setAttribute("autocomplete", "off");
			var div = document.createElement("div");
			var list = document.createElement("ul");
			list.style.display = "none";
			div.className = classSuggestion;
			list.style.width = field.offsetWidth + "px";
			div.appendChild(list);
			field.parentNode.appendChild(div);	

			field.onkeypress = function(e){
				
				var key = getKeyCode(e);
		
				if(key == 13){ // enter
					selectList();
					selectedIndex = 0;
					return false;
				};	
			};
				
			field.onkeyup = function(e){
			
				var key = getKeyCode(e);
		
				switch(key){
				case 13:
					return false;
					break;			
				case 27:  // esc
					field.value = "";
					selectedIndex = 0;
					clearList();
					break;				
				case 38: // up
					navList("up");
					break;
				case 40: // down
					navList("down");		
					break;
				default:
					startList();			
					break;
				};
			};
			
			this.startList = function(){
				var arr = getListItems(field.value);
				if(field.value.length > 0){
					createList(arr);
				} else {
					clearList();
				};	
			};
			
			this.getListItems = function(value){
				var arr = new Array();
				var src = suggestionText;
				var src = src.replace(/, /g, ",");
				var arrSrc = src.split(",");
				for(i=0;i<arrSrc.length;i++){
					if(arrSrc[i].substring(0,value.length).toLowerCase() == value.toLowerCase()){
						arr.push(arrSrc[i]);
					};
				};				
				return arr;
			};
			
			this.createList = function(arr){				
				resetList();			
				if(arr.length > 0) {
					for(i=0;i<arr.length;i++){				
						li = document.createElement("li");
						a = document.createElement("a");
						a.href = "javascript:void(0);";
						a.i = i+1;
						a.innerHTML = arr[i];
						li.i = i+1;
						li.onmouseover = function(){
							navListItem(this.i);
						};
						a.onmousedown = function(){
							selectedIndex = this.i;
							selectList(this.i);		
							return false;
						};					
						li.appendChild(a);
						list.setAttribute("tabindex", "-1");
						list.appendChild(li);	
					};	
					list.style.display = "block";				
				} else {
					clearList();
				};
			};	
			
			this.resetList = function(){
				var li = list.getElementsByTagName("li");
				var len = li.length;
				for(var i=0;i<len;i++){
					list.removeChild(li[0]);
				};
			};
			
			this.navList = function(dir){			
				selectedIndex += (dir == "down") ? 1 : -1;
				li = list.getElementsByTagName("li");
				if (selectedIndex < 1) selectedIndex =  li.length;
				if (selectedIndex > li.length) selectedIndex =  1;
				navListItem(selectedIndex);
			};
			
			this.navListItem = function(index){	
				selectedIndex = index;
				li = list.getElementsByTagName("li");
				for(var i=0;i<li.length;i++){
					li[i].className = (i==(selectedIndex-1)) ? "selected" : "";
				};
			};
			
			this.selectList = function(){
				li = list.getElementsByTagName("li");	
				a = li[selectedIndex-1].getElementsByTagName("a")[0];
				field.value = a.innerHTML;
				clearList();
			};			
			
		};
	};
	
	this.clearList = function(){
		if(list){
			list.style.display = "none";
			selectedIndex = 0;
		};
	};		
	this.getKeyCode = function(e){
		var code;
		if (!e) var e = window.event;
		if (e.keyCode) code = e.keyCode;
		return code;
	};
	
};

// script initiates on page load. 

this.addEvent = function(obj,type,fn){
	if(obj.attachEvent){
		obj['e'+type+fn] = fn;
		obj[type+fn] = function(){obj['e'+type+fn](window.event );}
		obj.attachEvent('on'+type, obj[type+fn]);
	} else {
		obj.addEventListener(type,fn,false);
	};
};
addEvent(window,"load",searchfield);

