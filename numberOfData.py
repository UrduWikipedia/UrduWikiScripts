# -*- coding: utf-8 -*-

#!/usr/bin/python

# -*- coding: utf-8 -*-

#

# (C) https://it.wikipedia.org/wiki/Utente:Rotpunkt, 2018, under the MIT License

# 

import datetime

from pywikibot import date

from pywikibot.data.wikistats import WikiStats

import pywikibot

def formatStat(args):

	return '''| {prefix} = {{{{#switch:{{{{{{2}}}}}}	| NUMBEROFARTICLES | ARTICLES = {good}

	| NUMBEROFFILES | FILES = {images}

	| NUMBEROFPAGES | PAGES = {total}

	| NUMBEROFUSERS | USERS = {users}

	| NUMBEROFACTIVEUSERS | ACTIVEUSERS = {activeusers}

	| NUMBEROFADMINS | ADMINS = {admins}

	| NUMBEROFEDITS | EDITS = {edits}

	| 0 }}}}\n'''.format(**args)

def main():

	ws = WikiStats()

	stats = ws.sorted('wikipedia', 'good')

	# rimuove mo.wikipedia.org redirect a ro.wikipedia.org

	stats = [stat for stat in stats if stat['prefix'] != 'mo']

	now = datetime.datetime.now()

	text = u'<!-- یہاں نئی زبان شامل کرنے سے قبل تبادلہ خیال صفحہ پر گفتگو کر لیں۔ -->\n<onlyinclude>{{#switch:{{{1}}}\n'

	text += '| data = %d %s %d\n' % (now.day, date.formats['MonthName']['ur'](now.month), now.year)

	total = { 'good': 0, 'images': 0, 'total': 0, 'users': 0, 'activeusers': 0, 'admins': 0, 'edits': 0 }

	for stat in stats:

		text += formatStat(stat)

		for key in total:

			total[key] += int(stat[key])

	total['prefix'] = 'total'

	text += formatStat(total)

	text += u'| 0 }}</onlyinclude>\n<noinclude>\n{{دستاویز}}\n</noinclude>\n'

	pywikibot.handleArgs()

	site = pywikibot.Site()

	page = pywikibot.Page(site, 'Template:NUMBEROF/data')

	page.put(text, 'خودکار: تجدید شماریات')

if __name__ == '__main__':

	main()
