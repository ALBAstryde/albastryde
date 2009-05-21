# -*- coding: utf-8 -*-
import unicodedata
from django.utils import simplejson
import re
from graph.translator import translate_query_string
from graph.builder import build_graph
from django.contrib.auth.models import AnonymousUser
from django.http import QueryDict

WIKILINK_RE = r'\[\[([^\]]*)\]\]' # blah blah [[link name]] blah
STATISTICS_RE = r'\_statistics\[([^\]]*)\]' # blah blah _statistics[link name] blah
ESTADISTICAS_RE = r'\_estadisticas\[([^\]]*)\]' # blah blah _estadisticas[link name] blah


class albamarkup:
	def __init__(self,text):
		self.user=AnonymousUser()
		self.graph_counter=0
		self.json_data=""
		text = re.sub(WIKILINK_RE, self.WikilinkPattern, text)
		text = re.sub(STATISTICS_RE, self.StatisticsPattern, text)
		text = re.sub(ESTADISTICAS_RE, self.StatisticsPattern, text)
		self.returntext=text

	def WikilinkPattern(self,pattern):
		word=pattern.group(1)
        	unspanish_word=unicodedata.normalize('NFKD', unicode(word)).encode('ascii','ignore')
		linkword=unspanish_word.replace(" ","-")
		text="<a href=\"/wiki/"+linkword+"\">"+word+"</a>"
        	return text

	def StatisticsPattern(self,pattern):
		query = pattern.group(1)
		translated_query=QueryDict(translate_query_string(query))
		text='[div id="graph'+str(self.graph_counter)+'" class="graph"][/div]'
		rdict = build_graph(translated_query,self.user)
		json = simplejson.dumps(rdict, ensure_ascii=False)
 		self.json_data+='graph'+str(self.graph_counter)+'='+json+';'
		self.graph_counter += 1
	       	return text
