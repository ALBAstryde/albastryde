function badBrowser(){
	if($.browser.msie){ return true;}
	
	return false;
}

function getBadBrowser(c_name)
{
	if (document.cookie.length>0)
	{
	c_start=document.cookie.indexOf(c_name + "=");
	if (c_start!=-1)
		{ 
		c_start=c_start + c_name.length+1; 
		c_end=document.cookie.indexOf(";",c_start);
		if (c_end==-1) c_end=document.cookie.length;
		return unescape(document.cookie.substring(c_start,c_end));
		} 
	}
	return "";
}	

function setBadBrowser(c_name,value,expiredays)
{
	var exdate=new Date();
	exdate.setDate(exdate.getDate()+expiredays);
	document.cookie=c_name+ "=" +escape(value) + ((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
}

if(badBrowser() && getBadBrowser('browserWarning') != 'seen' ){
	$(function(){
		$("<div id='browserWarning'>"+_('ALBAstryde is a powerful application that requires a modern and professional browser. Unfortunately your current browser does not seem to fulfill the minimum criteria. However, there are many free ones that do, available on the internet. Please switch to')+" <a href='http://getfirefox.com'>FireFox</a>, <a href='http://www.google.com/chrome'>Chrome</a> "+ _('or')+ " <a href='http://www.apple.com/safari/'>Safari</a>. "+_('Thanks')+"!&nbsp;&nbsp;&nbsp;[<a href='#' id='warningClose'>"+_('close')+"</a>] </div> ")
			.css({
				backgroundColor: '#fcfdde',
				'width': '100%',
				'border-top': 'solid 1px #000',
				'border-bottom': 'solid 1px #000',
				'text-align': 'center',
				padding:'5px 0px 5px 0px'
			})
			.prependTo("body");
		
		$('#warningClose').click(function(){
			setBadBrowser('browserWarning','seen');
			$('#browserWarning').slideUp('slow');
			return false;
		});
	});	
}
