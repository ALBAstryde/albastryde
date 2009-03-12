import re
import unicodedata
from wiki import plotting
from urllib import quote_plus
import settings

WIKILINK_RE = r'\[\[([^\]]*)\]\]' # blah blah [[link name]] blah
STATISTICS_RE = r'\_statistics\[([^\]]*)\]' # blah blah _statistics[link name] blah
ESTADISTICAS_RE = r'\_estadisticas\[([^\]]*)\]' # blah blah _statistics[link name] blah


def ApplyMarkup(text):
	text = re.sub(WIKILINK_RE, WikilinkPattern, text)
	text = re.sub(STATISTICS_RE, StatisticsPattern, text)
	text = re.sub(ESTADISTICAS_RE, StatisticsPattern, text)
	return text

def WikilinkPattern(pattern):
	word=pattern.group(1)
        unspanish_word=unicodedata.normalize('NFKD', unicode(word)).encode('ascii','ignore')
	linkword=unspanish_word.replace(" ","-")
	text="<a href=\"/wiki/"+linkword+"\">"+word+"</a>"
        return text

def StatisticsPattern(pattern):
	raw_formula = pattern.group(1)
	formula_plot = plotting.Statisticsplot(raw_formula)
	filename = formula_plot.image_file_location

	text="<img src=\""+settings.MEDIA_URL+"/cache/"+quote_plus(formula_plot.image_file)+"\" />"
	try:
		file = open(filename)
	except IOError:
	        formula_plot.create_png()
        return text

