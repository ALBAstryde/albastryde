$(document).ready(function() {
        $('ul#maintabs li').hover(function(){$(this).addClass("ui-state-hover");},function(){$(this).removeClass("ui-state-hover");});
        $('form#menu_search').submit(function() {
                searchterm=$('#menu_search_field').val();
                window.location.href='/busqueda/'+searchterm;
                return false;
        });
        $('form#page_search').submit(function() {
                searchterm=$('#page_search_field').val();
                window.location.href='/busqueda/'+searchterm;
                return false;
        });
});
$(function() {
	$("#variables").accordion();
});

