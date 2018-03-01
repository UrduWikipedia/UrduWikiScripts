# -*- coding: utf-8 -*-
"""File containing all standard fixes."""
#
# (C) Pywikibot team, 2008-2018
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import os.path

from pywikibot import config

parameter_help = u"""
                  Currently available predefined fixes are:

                  * HTML        - Convert HTML tags to wiki syntax, and
                                  fix XHTML.
                  * isbn        - Fix badly formatted ISBNs.
                  * syntax      - Try to fix bad wiki markup. Do not run
                                  this in automatic mode, as the bot may
                                  make mistakes.
                  * syntax-safe - Like syntax, but less risky, so you can
                                  run this in automatic mode.
                  * case-de     - fix upper/lower case errors in German
                  * grammar-de  - fix grammar and typography in German
                  * vonbis      - Ersetze Binde-/Gedankenstrich durch "bis"
                                  in German
                  * music       - Links auf Begriffsklärungen in German
                  * datum       - specific date formats in German
                  * correct-ur  - Corrections for Urdu Wikipedia and any
                                  Urdu wiki.
                  * correct-ar  - Corrections for Arabic Wikipedia and any
                                  Arabic wiki.
                  * yu-tld      - the yu top-level domain will soon be
                                  disabled, see
                  * fckeditor   - Try to convert FCKeditor HTML tags to wiki
                                  syntax.
                                  https://lists.wikimedia.org/pipermail/wikibots-l/2009-February/000290.html
"""

__doc__ = __doc__ + parameter_help

fixes = {
    # These replacements will convert HTML to wiki syntax where possible, and
    # make remaining tags XHTML compliant.
    'HTML': {
        'regex': True,
        'msg': 'pywikibot-fixes-html',
        'replacements': [
            # Everything case-insensitive (?i)
            # Keep in mind that MediaWiki automatically converts <br> to <br />
            # when rendering pages, so you might comment the next two lines out
            # to save some time/edits.
            (r'(?i)<br *>',                      r'<br />'),
            # linebreak with attributes
            (r'(?i)<br ([^>/]+?)>',            r'<br \1 />'),
            (r'(?i)<b>(.*?)</b>',              r"'''\1'''"),
            (r'(?i)<strong>(.*?)</strong>',    r"'''\1'''"),
            (r'(?i)<i>(.*?)</i>',              r"''\1''"),
            (r'(?i)<em>(.*?)</em>',            r"''\1''"),
            # horizontal line without attributes in a single line
            (r'(?i)([\r\n])<hr[ /]*>([\r\n])', r'\1----\2'),
            # horizontal line without attributes with more text in same line
            #   (r'(?i) +<hr[ /]*> +',             r'\r\n----\r\n'),
            # horizontal line with attributes; can't be done with wiki syntax
            # so we only make it XHTML compliant
            (r'(?i)<hr ([^>/]+?)>',            r'<hr \1 />'),
            # a header where only spaces are in the same line
            (r'(?i)([\r\n]) *<h1> *([^<]+?) *</h1> *([\r\n])', r'\1= \2 =\3'),
            (r'(?i)([\r\n]) *<h2> *([^<]+?) *</h2> *([\r\n])',
             r'\1== \2 ==\3'),
            (r'(?i)([\r\n]) *<h3> *([^<]+?) *</h3> *([\r\n])',
             r'\1=== \2 ===\3'),
            (r'(?i)([\r\n]) *<h4> *([^<]+?) *</h4> *([\r\n])',
             r'\1==== \2 ====\3'),
            (r'(?i)([\r\n]) *<h5> *([^<]+?) *</h5> *([\r\n])',
             r'\1===== \2 =====\3'),
            (r'(?i)([\r\n]) *<h6> *([^<]+?) *</h6> *([\r\n])',
             r'\1====== \2 ======\3'),
            # TODO: maybe we can make the bot replace <p> tags with \r\n's.
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre'
            ],
        }
    },

    # Grammar fixes for German language
    # Do NOT run this automatically!
    'grammar-de': {
        'regex': True,
        'msg': {
            'de': u'Bot: korrigiere Grammatik',
        },
        'replacements': [
            #   (u'([Ss]owohl) ([^,\.]+?), als auch', r'\1 \2 als auch'),
            #   (u'([Ww]eder) ([^,\.]+?), noch', r'\1 \2 noch'),
            #
            # Vorsicht bei Substantiven, z. B. 3-Jähriger!
            (r'(\d+)(minütig|stündig|tägig|wöchig|jährig|minütlich|stündlich'
             r'|täglich|wöchentlich|jährlich|fach|mal|malig|köpfig|teilig'
             r'|gliedrig|geteilt|elementig|dimensional|bändig|eckig|farbig'
             r'|stimmig)', r'\1-\2'),
            # zusammengesetztes Wort, Bindestrich wird durchgeschleift
            (r'(?<!\w)(\d+|\d+[.,]\d+)(\$|€|DM|£|¥|mg|g|kg|ml|cl|l|t|ms|min'
             r'|µm|mm|cm|dm|m|km|ha|°C|kB|MB|GB|TB|W|kW|MW|GW|PS|Nm|eV|kcal'
             r'|mA|mV|kV|Ω|Hz|kHz|MHz|GHz|mol|Pa|Bq|Sv|mSv)([²³]?-[\w\[])',
             r'\1-\2\3'),
            # Größenangabe ohne Leerzeichen vor Einheit
            # weggelassen wegen vieler falsch Positiver: s, A, V, C, S, J, %
            (r'(?<!\w)(\d+|\d+[.,]\d+)(\$|€|DM|£|¥|mg|g|kg|ml|cl|l|t|ms|min'
             r'|µm|mm|cm|dm|m|km|ha|°C|kB|MB|GB|TB|W|kW|MW|GW|PS|Nm|eV|kcal'
             r'|mA|mV|kV|Ω|Hz|kHz|MHz|GHz|mol|Pa|Bq|Sv|mSv)(?=\W|²|³|$)',
             r'\1 \2'),
            # Temperaturangabe mit falsch gesetztem Leerzeichen
            (r'(?<!\w)(\d+|\d+[.,]\d+)° C(?=\W|²|³|$)', r'\1 °C'),
            # Kein Leerzeichen nach Komma
            (r'([a-zäöüß](\]\])?,)((\[\[)?[a-zäöüA-ZÄÖÜ])', r'\1 \3'),
            # Leerzeichen und Komma vertauscht
            (r'([a-zäöüß](\]\])?) ,((\[\[)?[a-zäöüA-ZÄÖÜ])', r'\1, \3'),
            # Plenks (Leerzeichen vor Komma/Punkt/Ausrufezeichen/Fragezeichen)
            # Achtung bei Französisch:
            # https://de.wikipedia.org/wiki/Plenk#Franz.C3.B6sische_Sprache
            # Leerzeichen vor Doppelpunkt/Semikolon kann korrekt sein,
            # z.B. nach Quellenangaben
            (r'([a-zäöüß](\]\])?) ([,.!?]) ((\[\[)?[a-zäöüA-ZÄÖÜ])',
             r'\1\3 \4'),
            #   (u'([a-z]\.)([A-Z])', r'\1 \2'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',           # because of code examples
                'source',        # because of code examples
                'startspace',    # because of code examples
                'hyperlink',     # e.g. commas in URLs
                'gallery',       # because of filenames
                'timeline',
            ],
            'text-contains': [
                r'sic!',
                r'20min.ch',     # Schweizer News-Seite
            ],
            'inside': [
                r'<code>.*</code>',  # because of code examples
                r'{{[Zz]itat\|.*?}}',
                r'{{§\|.*?}}',   # Gesetzesparagraph
                r'§?\d+[a-z]',  # Gesetzesparagraph
                r'Ju 52/1m',  # Flugzeugbezeichnung
                r'Ju 52/3m',  # Flugzeugbezeichnung
                r'AH-1W',     # Hubschrauberbezeichnung
                r'ZPG-3W',    # Luftschiffbezeichnung
                r'8mm',       # Filmtitel
                r'802.11g',   # WLAN-Standard
                r'DOS/4GW',   # Software
                r'ntfs-3g',   # Dateisystem-Treiber
                r'/\w(,\w)*/',      # Laut-Aufzählung in der Linguistik
                # Variablen in der Mathematik
                # (unklar, ob Leerzeichen hier Pflicht sind)
                r'[xyz](,[xyz])+',
                # Definitionslisten, dort gibt es oft absichtlich Leerzeichen
                # vor Doppelpunkten
                r'(?m)^;(.*?)$',
                r'\d+h( |&nbsp;)\d+m',
                # Schreibweise für Zeiten, vor allem in Film-Infoboxen.
                # Nicht korrekt, aber dafür schön kurz.
                r'(?i)\[\[(Bild|Image|Media):.+?\|',  # Dateinamen auslassen
                r'{{bgc\|.*?}}',                      # Hintergrundfarbe
                r'<sup>\d+m</sup>',                   # bei chemischen Formeln
                r'\([A-Z][A-Za-z]*(,[A-Z][A-Za-z]*'
                r'(<sup>.*?</sup>|<sub>.*?</sub>|))+\)'
                # chemische Formel, z. B. AuPb(Pb,Sb,Bi)Te.
                # Hier sollen keine Leerzeichen hinter die Kommata.
            ],
            'title': [
                r'Arsen',  # chemische Formel
            ],
        }
    },

    # Do NOT run this automatically!
    # Recommendation: First run syntax-safe automatically, afterwards
    # run syntax manually, carefully checking that you're not breaking
    # anything.
    'syntax': {
        'regex': True,
        'msg': 'pywikibot-fixes-syntax',
        'replacements': [
            # external link in double brackets
            (r'\[\[(?P<url>https?://[^\]]+?)\]\]',   r'[\g<url>]'),
            # external link starting with double bracket
            (r'\[\[(?P<url>https?://.+?)\]',   r'[\g<url>]'),
            # external link with forgotten closing bracket
            #   (r'\[(?P<url>https?://[^\]\s]+)\r\n',  r'[\g<url>]\r\n'),
            # external link ending with double bracket.
            # do not change weblinks that contain wiki links inside
            # inside the description
            (r'\[(?P<url>https?://[^\[\]]+?)\]\](?!\])',   r'[\g<url>]'),
            # external link and description separated by a dash.
            # ATTENTION: while this is a mistake in most cases, there are some
            # valid URLs that contain dashes!
            (r'\[(?P<url>https?://[^\|\]\s]+?) *\| *(?P<label>[^\|\]]+?)\]',
             r'[\g<url> \g<label>]'),
            # wiki link closed by single bracket.
            # ATTENTION: There are some false positives, for example
            # Brainfuck code examples or MS-DOS parameter instructions.
            # There are also sometimes better ways to fix it than
            # just putting an additional ] after the link.
            (r'\[\[([^\[\]]+?)\](?!\])',  r'[[\1]]'),
            # wiki link opened by single bracket.
            # ATTENTION: same as above.
            (r'(?<!\[)\[([^\[\]]+?)\]\](?!\])',  r'[[\1]]'),
            # template closed by single bracket
            # ATTENTION: There are some false positives, especially in
            # mathematical context or program code.
            (r'{{([^{}]+?)}(?!})',       r'{{\1}}'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'source',        # because of code examples
                'startspace',    # because of code examples
            ],
            'text-contains': [
                r'http://.*?object=tx\|',                # regular dash in URL
                r'http://.*?allmusic\.com',              # regular dash in URL
                r'http://.*?allmovie\.com',              # regular dash in URL
                r'http://physics.nist.gov/',             # regular dash in URL
                r'http://www.forum-seniorenarbeit.de/',  # regular dash in URL
                r'http://kuenstlerdatenbank.ifa.de/',    # regular dash in URL
                r'&object=med',                          # regular dash in URL
                r'\[CDATA\['                             # lots of brackets
            ],
        }
    },

    # The same as syntax, but restricted to replacements that should
    # be safe to run automatically.
    'syntax-safe': {
        'regex': True,
        'msg': 'pywikibot-fixes-syntax',
        'replacements': [
            # external link in double brackets
            (r'\[\[(?P<url>https?://[^\]]+?)\]\]',   r'[\g<url>]'),
            # external link starting with double bracket
            (r'\[\[(?P<url>https?://.+?)\]',   r'[\g<url>]'),
            # external link with forgotten closing bracket
            #   (r'\[(?P<url>https?://[^\]\s]+)\r\n',   r'[\g<url>]\r\n'),
            # external link and description separated by a dash, with
            # whitespace in front of the dash, so that it is clear that
            # the dash is not a legitimate part of the URL.
            (r'\[(?P<url>https?://[^\|\] \r\n]+?) +\| *(?P<label>[^\|\]]+?)\]',
             r'[\g<url> \g<label>]'),
            # dash in external link, where the correct end of the URL can
            # be detected from the file extension. It is very unlikely that
            # this will cause mistakes.
            (r'\[(?P<url>https?://[^\|\] ]+?'
             r'(\.pdf|\.html|\.htm|\.php|\.asp|\.aspx|\.jsp)) *\|'
             r' *(?P<label>[^\|\]]+?)\]', r'[\g<url> \g<label>]'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'source',        # because of code examples
                'startspace',    # because of code examples
            ],
        }
    },

    'case-de': {  # German upper / lower case issues
        'regex': True,
        'msg': {
            'de': u'Bot: Korrigiere Groß-/Kleinschreibung',
        },
        'replacements': [
            (r'\batlantische(r|n|) Ozean', r'Atlantische\1 Ozean'),
            (r'\bdeutsche(r|n|) Bundestag\b', r'Deutsche\1 Bundestag'),
            # Aufpassen, z. B. 'deutsche Bundestagswahl'
            (r'\bdeutschen Bundestags\b', r'Deutschen Bundestags'),
            (r'\bdeutsche(r|n|) Reich\b', r'Deutsche\1 Reich'),
            # Aufpassen, z. B. 'deutsche Reichsgrenzen'
            (r'\bdeutschen Reichs\b', r'Deutschen Reichs'),
            (r'\bdritte(n|) Welt(?!krieg)', r'Dritte\1 Welt'),
            (r'\bdreißigjährige(r|n|) Krieg', r'Dreißigjährige\1 Krieg'),
            (r'\beuropäische(n|) Gemeinschaft', r'Europäische\1 Gemeinschaft'),
            (r'\beuropäische(n|) Kommission', r'Europäische\1 Kommission'),
            (r'\beuropäische(n|) Parlament', r'Europäische\1 Parlament'),
            (r'\beuropäische(n|) Union', r'Europäische\1 Union'),
            (r'\berste(r|n|) Weltkrieg', r'Erste\1 Weltkrieg'),
            (r'\bkalte(r|n|) Krieg', r'Kalte\1 Krieg'),
            (r'\bpazifische(r|n|) Ozean', r'Pazifische\1 Ozean'),
            (r'Tag der deutschen Einheit', r'Tag der Deutschen Einheit'),
            (r'\bzweite(r|n|) Weltkrieg', r'Zweite\1 Weltkrieg'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
            ],
            'text-contains': [
                r'sic!',
            ],
        }
    },

    'vonbis': {
        'regex': True,
        'msg': {
            'de': u'Bot: Ersetze Binde-/Gedankenstrich durch "bis"',
        },
        'replacements': [
            # Bindestrich, Gedankenstrich, Geviertstrich
            (r'(von \d{3,4}) *(-|&ndash;|–|&mdash;|—) *(\d{3,4})',
             r'\1 bis \3'),
        ],
    },

    # some disambiguation stuff for de:
    # python replace.py -fix:music -subcat:Album
    'music': {
        'regex': False,
        'msg': {
            'de': u'Bot: korrigiere Links auf Begriffsklärungen',
        },
        'replacements': [
            (u'[[CD]]', u'[[Audio-CD|CD]]'),
            (u'[[LP]]', u'[[Langspielplatte|LP]]'),
            (u'[[EP]]', u'[[Extended Play|EP]]'),
            (u'[[MC]]', u'[[Musikkassette|MC]]'),
            (u'[[Single]]', u'[[Single (Musik)|Single]]'),
        ],
        'exceptions': {
            'inside-tags': [
                'hyperlink',
            ]
        }
    },

    # format of dates of birth and death, for de:
    # python replace.py -fix:datum -ref:Vorlage:Personendaten
    'datum': {
        'regex': True,
        'msg': {
            'de': u'Bot: Korrigiere Datumsformat',
        },
        'replacements': [
            # space after birth sign w/ year
            #   (u'\(\*(\d{3,4})', u'(* \\1'),
            # space after death sign w/ year
            #   (u'†(\d{3,4})', u'† \\1'),
            #   (u'&dagger;(\d{3,4})', u'† \\1'),
            # space after birth sign w/ linked date
            #   (u'\(\*\[\[(\d)', u'(* [[\\1'),
            # space after death sign w/ linked date
            #   (u'†\[\[(\d)', u'† [[\\1'),
            #   (u'&dagger;\[\[(\d)', u'† [[\\1'),
            (r'\[\[(\d+\. (?:Januar|Februar|März|April|Mai|Juni|Juli|August|'
             r'September|Oktober|November|Dezember)) (\d{1,4})\]\]',
             r'[[\1]] [[\2]]'),
            # Keine führende Null beim Datum
            # (erst einmal nur bei fehlenden Leerzeichen)
            (r'0(\d+)\.(Januar|Februar|März|April|Mai|Juni|Juli|August|'
             r'September|Oktober|November|Dezember)', r'\1. \2'),
            # Kein Leerzeichen zwischen Tag und Monat
            (r'(\d+)\.(Januar|Februar|März|April|Mai|Juni|Juli|August|'
             r'September|Oktober|November|Dezember)', r'\1. \2'),
            # Kein Punkt vorm Jahr
            (r'(\d+)\. (Januar|Februar|März|April|Mai|Juni|Juli|August|'
             r'September|Oktober|November|Dezember)\.(\d{1,4})', r'\1. \2 \3'),
        ],
        'exceptions': {
            'inside': [
                r'\[\[20. Juli 1944\]\]',  # Hitler-Attentat
                r'\[\[17. Juni 1953\]\]',  # Ost-Berliner Volksaufstand
                r'\[\[1. April 2000\]\]',  # Film
                r'\[\[11. September 2001\]\]',  # Anschläge in den USA
                r'\[\[7. Juli 2005\]\]',   # Terroranschläge in Spanien
            ],
        }
    },

    'isbn': {
        'generator': [r'-search:insource:/nowiki\>ISBN:?(?:&nbsp;| *)[0-9]/',
                      '-namespace:0'],
        'regex': True,
        'msg': 'isbn-formatting',  # use i18n translations
        'replacements': [
            # Remove colon between the word ISBN and the number
            (r'ISBN: (\d+)', r'ISBN \1'),
            # superfluous word "number"
            (r'ISBN(?: [Nn]umber| [Nn]o\.?|-Nummer|-Nr\.):? (\d+)',
             r'ISBN \1'),
            # Space, minus, dot, hypen, en dash, em dash, etc. instead of
            # hyphen-minus as separator,
            # or spaces between digits and separators.
            # Note that these regular expressions also match valid ISBNs, but
            # these won't be changed.
            # These two regexes don't verify that the ISBN is of a valid format
            # but just change separators into normal hypens. The isbn script
            # does checks and similar but does only match ISBNs with digits and
            # hypens (and optionally a X/x at the end).
            (r'ISBN (978|979) *[\- −.‐-―] *(\d+) *[\- −.‐-―] *(\d+) '
             r'*[\- −.‐-―] *(\d+) *[\- −.‐-―] *(\d)(?!\d)',
             r'ISBN \1-\2-\3-\4-\5'),  # ISBN-13

            (r'ISBN (\d+) *[\- −.‐-―] *(\d+) *[\- −.‐-―] *(\d+) *'
             r'[\- −.‐-―] *(\d|X|x)(?!\d)',
             r'ISBN \1-\2-\3-\4'),  # ISBN-10
            # missing space before ISBN-10 or before ISBN-13,
            # or multiple spaces or non-breaking space.
            (r'ISBN(?: *|&nbsp;)((\d(-?)){12}\d|(\d(-?)){9}[\dXx])',
             r'ISBN \1'),
            # remove <nowiki /> tags
            (r'<nowiki>ISBN ([0-9\-xX]+)</nowiki>', r'ISBN \1'),
        ],
        'exceptions': {
            'inside-tags': [
                'comment',
                'hyperlink',
            ],
            'inside': [
                r'ISBN (97[89]-?)(\d-?){9}\d',  # matches valid ISBN-13s
                r'ISBN (\d-?){9}[\dXx]',  # matches valid ISBN-10s
            ],
        }
    },

    #Corrections for Urdu Wikipedia and any Urdu wiki.
    #python replace.py -fix:correct-ur -start:! -always

    'correct-ur': {
        'regex': True,
        'msg': {
            'ur':u'درستی املا بمطابق [[ویکیپیڈیا:املا پڑتالگر/فہرست الفاظ|فہرست املا پڑتالگر]] + ویکائی',
        },
        'replacements': [
            (ur'\bآبساز\b', ur'ہائیڈروجن'),
            (ur'\bآٹوویکی\b', ur'آٹو ویکی'),
            (ur'\b(آ|ا)جکل\b', ur'آج کل'),
            (ur'\bآڑے وقت\b', ur'اڑے وقت'),
            (ur'\bآزمایش\b', ur'آزمائش'),
            (ur'\bآزمایشات\b', ur'آزمائشیں'),
            (ur'\bآزمایشیں\b', ur'آزمائشیں'),
            (ur'\bآغوشیہ\b', ur'لیپ ٹاپ'),
            (ur'\bآلاتیات\b', ur'میکانیات'),
            (ur'\bآلاتی\b', ur'میکانیکی'),
            (ur'\bآهستہ\b', ur'آہستہ'),
            (ur'\bآئمہ\b', ur'ائمہ'),
            (ur'\bابتداء\b', ur'ابتدا'),
            (ur'\bابتدائ\b', ur'ابتدائی'),
            (ur'\bابتلاء\b', ur'ابتلا'),
            (ur'\bاتر پردیش\b', ur'اترپردیش'),
            (ur'\bاجراء\b', ur'اجرا'),
            (ur'\bادباء\b', ur'ادبا'),
            (ur'\bارتقاء\b', ur'ارتقا'),
            (ur'\bاستعفیٰ\b', ur'استعفا'),
            (ur'\bاسکو\b', ur'اس کو'),
            (ur'\bاسلئے\b', ur'اس لیے'),
            (ur'\bاسلیے\b', ur'اس لیے'),
            (ur'\bاسلیئے\b', ur'اس لیے'),
            (ur'\bاصلذر\b', ur'اصل زر'),
            (ur'\bاوللعزم\b', ur'اولو العزم'),
            (ur'\bاعلانیہ\b', ur'علانیہ'),
            (ur'\bاختراح\b', ur'اختراع'),
            (ur'\bاذدھا\b', ur'اژدہا'),
            (ur'\bاڈہ\b', ur'اڈا'),
            (ur'\bاسطرح\b', ur'اس طرح'),
            (ur'\bاسل\b', ur'اصل'),
            (ur'\bاسلاح\b', ur'اصلاح'),
            (ur'\bاصلاع\b', ur'اصلاح'),
            (ur'\bاژدھا\b', ur'اژدہا'),
            (ur'\bاذدہا\b', ur'اژدہا'),
            (ur'\bاذدھا\b', ur'اژدہا'),
            (ur'\bاژدہام\b', ur'ازدحام'),
            (ur'\bازدہام\b', ur'ازدحام'),
            (ur'\bاژدحام\b', ur'ازدحام'),
            (ur'\bافوا\b', ur'افواہ'),
            (ur'\bاژدہام\b', ur'ازدحام'),
            (ur'\bاژدھا\b', ur'اژدہا'),
            (ur'\bازدہام\b', ur'ازدحام'),
            (ur'\bاژدحام\b', ur'ازدحام'),
            (ur'\bاسلاح\b', ur'اصلاح'),
            (ur'\bاسک(ا|ی|ے)\b', ur'اس ک\1'),
            (ur'\bاصلاع\b', ur'اصلاح'),
            (ur'\bاطهر\b', ur'اطہر'),
            (ur'\bالجبرہ\b', ur'الجبرا'),
            (ur'\bالحمدللہ\b', ur'الحمد للہ'),
            (ur'\bامبار\b', ur'انبار'),
            (ur'\bامراء\b', ur'امرا'),
            (ur'\bامریکہ\b', ur'امریکا'),
            (ur'\bاملاف\b', ur'فائلیں'),
            (ur'\bاملاء\b', ur'املا'),
            (ur'\bانبیاء\b', ur'انبیا'),
            (ur'\bانتہاء\b', ur'انتہا'),
            (ur'\bانتہاء?پسندی\b', ur'انتہا پسندی'),
            (ur'\bانجینئرنگ\b', ur'انجینئری'),
            (ur'\bاندازا\b', ur'اندازہ'),
            (ur'\bانسٹیٹیوٹ\b', ur'انسٹی ٹیوٹ'),
            (ur'\(\s*\[\[انگریزی زبان\|انگریزی\]\]\s*\:\s*(.+?)\s*\)', ur'{{دیگر نام|انگریزی= \1}}'),
            (ur'\(\s*\[\[(انگریزی|انگریزی زبان)\]\]\s*\:\s*(.+?)\s*\)', ur'{{دیگر نام|انگریزی= \2}}'),
            (ur'\bاور،\b', ur'اور'),
            (ur'\bاہل وعیال\b', ur'اہل و عیال'),
            (ur'\bاھم\b', ur'اہم'),
            (ur'\bاھمیت\b', ur'اہمیت'),
            (ur'\bاهمیت\b', ur'اہمیت'),
            (ur'\bانهی\b', ur'انہی'),
            (ur'\bالهی\b', ur'الہی'),
            (ur'\bاستعفہ\b', ur'استعفا'),
            (ur'\bانکساری\b', ur'انکسار'),
            (ur'\bانگوڑہ\b', ur'انگوڑا'),
            (ur'\bاہلحدیث\b', ur'اہل حدیث'),
            (ur'\bاہلحدیثوں\b', ur'اہل حدیث'),
            (ur'\bاہل حدیثوں\b', ur'اہل حدیث'),
            (ur'\bاھمیت\b', u'اہمیت'),
            (ur'\bایشیاء\b', ur'ایشیا'),
            (ur'\bایکدوسر', ur'ایک دوسر'),
            (ur'\bبھائ\b', ur'بھائی'),
            (ur'\bباجہ\b', ur'باجا'),
            (ur'\bبارویں\b', ur'بارہویں'),
            (ur'\bبالمشافہہ\b', ur'بالمُشافہ'),
            (ur'\bبچگان(ہ|ی)\b', ur'بچکان\1'),
            (ur'\bبٹوہ\b', ur'بٹوا'),
            (ur'\bبجالاتا\b', ur'بجا لاتا'),
            (ur'\bبجالاتی\b', ur'بجا لاتی'),
            (ur'\bبجالاتے\b', ur'بجا لاتے'),
            (ur'\bبجالاتیں\b', ur'بجا لاتیں'),
            (ur'\bبد\s*امنی\b', ur'بے امنی'),
            (ur'\bبرائے کرم\b', ur'براہ کرم'),
            (ur'\bبرائے مہربانی\b', ur'براہ مہربانی'),
            (ur'\bبر\s*سر\s*اقتدار\b', ur'بر سر اقتدار'),
            (ur'\bبر\s*سر\s*پیکار\b', ur'بر سر پیکار'),
            (ur'\bبرقعہ\b', ur'برقع'),
            (ur'\bبرمجہ\b', ur'پروگرامنگ'),
            (ur'\bبرمہ\b', ur'برما'),
            (ur'\bبرنامج\b', ur'پروگرام'),
            (ur'\bبعدازاں\b', ur'بعد ازاں'),
            (ur'\bبقایہ\b', ur'بقایا'),
            (ur'\bبل پاس\b', ur'بل منظور'),
            (ur'\bبلالحاظ\b', ur'بلا لحاظ'),
            (ur'\bبلآخر\b', ur'بالآخر'),
            (ur'\bبلکل\b', ur'بالکل'),
            (ur'\bبلترتیب\b', ur'بالترتیب'),
            (ur'\bبلخصوص\b', ur'بالخصوص'),
            (ur'\bبلواسطہ\b', ur'بالواسطہ'),
            (ur'\bبمعہ\b', ur'مع'),
            (ur'\bبمع\b', ur'مع'),
            (ur'\bبناء\b', ur'بنا'),
            (ur'\bبنجارہ\b', ur'بنجارا'),
            (ur'\bبندوک\b', ur'بندوق'),
            (ur'\bبلي\b', ur'بلی'),
            (ur'\bبھائ\b', ur'بھائی'),
            (ur'\bبھروسہ\b', ur'بھروسا'),
            (ur'\bبھوسہ\b', ur'بھوسا'),
            (ur'\bبھی خواہ\b', ur'بہی خواہ'),
            (ur'\bبہوت\b', ur'بھوت'),
            (ur'\bبیروزگار', ur'بے روزگار'),
            (ur'\bبیڑہ\b', ur'بیڑا'),
            (ur'\bبے نیل و مرام\b', ur'بے نیل مرام'),
            (ur'\bبےنیل ومرام\b', ur'بے نیل مرام'),
            (ur'\bبے نیل ومرام\b', ur'بے نیل مرام'),
            (ur'\bبےنیل\b', ur'بے نیل'),
            (ur'\bپشیمانگی\b', ur'پشیمانی'),
            (ur'\bپذیرائی\b', ur'پزیرائی'),
            (ur'\bپروف ریڈنگ\b', ur'پروف خوانی'),
            (ur'\bپرواہ\b', ur'پروا'),
            (ur'\bپرواہی\b', ur'پروائی'),
            (ur'\bپروگرامات\b', ur'پروگرام'),
            (ur'\bپہیہ\b', ur'پہیا'),
            (ur'\bپهنچایا\b', ur'پہنچایا'),
            (ur'\bپاکپٹان\b', ur'پاکپتن'),
            (ur'\bپختونخواہ\b', ur'پختونخوا'),
            (ur'\bپشتونخواہ\b', ur'پشتونخوا'),
            (ur'\bپانسہ\b', ur'پانسا'),
            (ur'\bپٹاخہ\b', ur'پٹاخا'),
            (ur'\bپٹارہ\b', ur'پٹارا'),
            (ur'\bپڑگیا\b', ur'پڑ گیا'),
            (ur'\bپڑگئی\b', ur'پڑ گئی'),
            (ur'\bپڑگئے\b', ur'پڑ گئے'),
            (ur'\bپڑیگا\b', ur'پڑے گا'),
            (ur'\bپزمردہ\b', ur'پژمردہ'),
            (ur'\bپزمردگی\b', ur'پژمردگی'),
            (ur'\bپھاوڑہ\b', ur'پھاوڑا'),
            (ur'\bپھیپھڑہ\b', ur'پھیپھڑا'),
            (ur'\bپیداہش\b', ur'پیدائش'),
            (ur'\bپھندہ\b', ur'پھندا'),
            (ur'\bپیروئی\b', ur'پیروی'),
            (ur'\bپند\s*و\s*(نصیحت|نصائح|وعظ)\b', ur'پند و \1'),
            (ur'\bتجاویزات\b', ur'تجاویز'),
            (ur'\bترجیہ\b', ur'ترجیح'),
            (ur'\bترجیہات\b', ur'ترجیحات'),
            (ur'\bتسانیف\b', ur'تصانیف'),
            (ur'\bتسنیف\b', ur'تصنیف'),
            (ur'\bتشت\b', ur'طشت'),
            (ur'\bتوجیح\b', ur'توجیہ'),
            (ur'\bتوطی\b', ur'طوطی'),
            (ur'\bتمغہ\b', ur'تمغا'),
            (ur'\bتقاضہ\b', ur'تقاضا'),
            (ur'\bتماشہ\b', ur'تماشا'),
            (ur'\bتمانچہ\b', ur'طمانچہ'),
            (ur'\bتمبورہ\b', ur'تنبورہ'),
            (ur'\bتنازعہ\b', ur'تنازع'),
            (ur'\bتنباکو\b', ur'تمباکو'),
            (ur'\bتنبولی\b', ur'تمبولی'),
            (ur'\bتوبڑہ\b', ur'توبڑا'),
            (ur'\bتشبیہہ\b', ur'تشبیہ'),
            (ur'\bتقاضہ\b', ur'تقاضا'),
            (ur'\bتنبیہہ\b', ur'تنبیہ'),
            (ur'\bتوجیہہ\b', ur'توجیہ'),
            (ur'\bتہماسپ\b', ur'طہماسپ'),
            (ur'\bتہہ\b', ur'تہ'),
            (ur'\bٹکر گدا\b', ur'ٹکڑگدا'),
            (ur'\bٹانگہ\b', ur'تانگہ'),
            (ur'\bٹھیر\b', ur'ٹھہر'),
            (ur'\bٹھیکہ\b', ur'ٹھیکا'),
            (ur'\bٹھپہ\b', ur'ٹھپا'),
            (ur'\bٹیلیویژن\b', ur'ٹیلی ویژن'),
            (ur'\bٹیلی\s*ویزن\b', ur'ٹیلی ویژن'),
            (ur'\bجالہ\b', ur'جالا'),
            (ur'\bجارہے\b', ur'جا رہے'),
            (ur'\bجامعہ مسجد\b', ur'جامع مسجد'),
            (ur'\bجائیداد\b', ur'جائداد'),
            (ur'\bجسکا\b', ur'جس کا'),
            (ur'\bجسکی\b', ur'جس کی'),
            (ur'\bجسکے\b', ur'جس کے'),
            (ur'\bجسکو\b', ur'جس کو'),
            (ur'\bجو\s*کہ\b', ur'جو'),
            (ur'\bجمبش\b', ur'جنبش'),
            (ur'\bجنهوں\b', ur'جنہوں'),
            (ur'\bچولہا\b', ur'چولھا'),
            (ur'\bچاہیئے\b', ur'چاہیے'),
            (ur'\bچاکو\b', ur'چاقو'),
            (ur'\bچالاق\b', ur'چالاک'),
            (ur'\bچقور\b', ur'چکور'),
            (ur'\bچلغوزا\b', ur'چلغوزہ'),
            (ur'\bچناچہ\b', ur'چنانچہ'),
            (ur'\bچبوترہ\b', ur'چبوترا'),
            (ur'\bچٹخارہ\b', ur'چٹخارا'),
            (ur'\bچٹکلہ\b', ur'چٹکلا'),
            (ur'\bچنپا\b', ur'چمپا'),
            (ur'\bچانول\b', ur'چاول'),
            (ur'\bچراخ\b', ur'چراغ'),
            (ur'\bحامی بھر', ur'ہامی بھر'),
            (ur'\bحیدر\s+آباد\b', ur'حیدرآباد'),
            (ur'\bحیرانگی\b', ur'حیرانی'),
            (ur'\bخاکا\b', ur'خاکہ'),
            (ur'\bخرابہ\b', ur'خرابا'),
            (ur'\bخرچا\b', ur'خرچہ'),
            (ur'\bخراٹہ\b', ur'خراٹا'),
            (ur'\bخط و کتابت\b', ur'خط کتابت'),
            (ur'\bخط وکتابت\b', ur'خط کتابت'),
            (ur'\bخوائش\b', ur'خواہش'),
            (ur'\bخوجہ\b', ur'خوجا'),
            (ur'\bخودمختار', ur'خود مختار'),
            (ur'\bخوردو نوش\b', ur'خور و نوش'),
            (ur'\bخورد و نوش\b', ur'خور و نوش'),
            (ur'\bخوردونوش\b', ur'خور و نوش'),
            (ur'\bخورد ونوش\b', ur'خور و نوش'),
            (ur'\bخورونوش\b', ur'خور و نوش'),
            (ur'\bخور ونوش\b', ur'خور و نوش'),
            (ur'\bخورو نوش\b', ur'خور و نوش'),
            (ur'\bدارالحکومت\b', ur'دار الحکومت'),
            (ur'\bدارالخلافہ\b', ur'دار الخلافہ'),
            (ur'\bدارلخلافہ\b', ur'دار الخلافہ'),
            (ur'\bدارالعلوم\b', ur'دار العلوم'),
            (ur'\bدارالعوام\b', ur'دار العوام'),
            (ur'\bدارالامرا\b', ur'دار الامرا'),
            (ur'\bدارالامراء\b', ur'دار الامرا'),
            (ur'\bدار الامراء\b', ur'دار الامرا'),
            (ur'\bدر اصل\b', ur'دراصل'),
            (ur'\bدربدر', ur'در بدر'),
            (ur'\bدرستگی\b', ur'درستی'),
            (ur'\bدرگذر\b', ur'درگزر'),
            (ur'\bدروازو(ہ|ا|ے)\b', ur'درواز\1'),
            (ur'\bدر\s*و\s*دیوار', ur'در و دیوار'),
            (ur'\bدریا\s*آبادی\b', ur'دریابادی'),
            (ur'\bدھائی\b', ur'دہائی'),
            (ur'\bدوگنا\b', ur'دگنا'),
            (ur'\bدھماکہ\b', ur'دھماکا'),
            (ur'\bدوکان\b', ur'دکان'),
            (ur'\bدکاندار\b', ur'دکان دار'),
            (ur'\bدوکاندار\b', ur'دکان دار'),
            (ur'\bدمبہ\b', ur'دنبہ'),
            (ur'\bدنیاء\b', ur'دنیا'),
            (ur'\bدوسراں\b', ur'دوسرا'),
            (ur'\bدونو\b', ur'دونوں'),
            (ur'\bدوئم\b', ur'دوم'),
            (ur'\bدھیلہ\b', ur'دھیلا'),
            (ur'\bدھوکہ\b', ur'دھوکا'),
            (ur'\bدیکھیئے\b', ur'دیکھیے'),
            (ur'\bدیکھئیے\b', ur'دیکھیے'),
            (ur'\bدیئے\b', ur'دیے'),
            (ur'\bڈرامہ\b', ur'ڈراما'),
            (ur'\bڈبیہ\b', ur'ڈبیا'),
            (ur'\bڈاکیہ\b', ur'ڈاکیا'),
            (ur'\bذخار\b', ur'زخار'),
            (ur'\bذگر\b', ur'ذکر'),
            (ur'\bذمہ وار', ur'ذمہ دار'),
            (ur'\bذیادہ\b', ur'زیادہ'),
            (ur'\n#\s*(REDIRECT|رجوع[ _]?مکرر)', ur'#رجوع_مکرر'),
            (ur'\n#رجوع_مکرر(?!\s)', ur'#رجوع_مکرر '),
            (ur'\bر(د|دِّ|دِ|دّ)عمل\b', ur'ر\1 عمل'),
            (ur'\bرفقاء\b', ur'رفقا'),
            (ur'\bرموز\s*و\s*اوقاف\b', ur'رموز اوقاف'),
            (ur'\bروائت\b', ur'روایت'),
            (ur'\bروائتی\b', ur'روایتی'),
            (ur'\bرہا ئش', ur'رہائش'),
            (ur'\bرہا ئی\b', ur'رہائی'),
            (ur'(\w+)رہا', ur'\1 رہا'),
            (ur'(\w+)رہی', ur'\1 رہی'),
            (ur'رہی(\w+)', ur'رہی \1'),
            (ur'(\w+)رہے', ur'\1 رہے'),
            (ur'رہے(\w+)', ur'رہے \1'),
            (ur'\bرهی\b', ur'رہی'),
            (ur'\bرها\b', ur'رہا'),
            (ur'\bرہنمائوں\b', ur'رہنماؤں'),
            (ur'\bرهنمائوں\b', ur'رہنماؤں'),
            (ur'\bرهنما\b', ur'رہنما'),
            (ur'\bرهتے\b', ur'رہتے'),
            (ur'\bرهے\b', ur'رہے'),
            (ur'\bرھیئے\b', ur'رہیے'),
            (ur'\bرہیئے\b', ur'رہیے'),
            (ur'\bروئیداد\b', ur'روداد'),
            (ur'\bزاکر\b', ur'ذاکر'),
            (ur'\bزردا\b', ur'زردہ'),
            (ur'\bزریہ\b', ur'بٹن'),
            (ur'\bزریعہ\b', ur'ذریعہ'),
            (ur'\bزریعے\b', ur'ذریعے'),
            (ur'\bزرائع\b', ur'ذرائع'),
            (ur'\bزکات\b', ur'زکوۃ'),
            (ur'\bزنانا\b', ur'زنانہ'),
            (ur'\bزبراثقال\b', ur'اپلوڈ'),
            (ur'\bزبر اثقال\b', ur'اپلوڈ'),
            (ur'\bزیراثقال\b', ur'ڈاؤنلوڈ'),
            (ur'\bزیر اثقال\b', ur'ڈاؤنلوڈ'),
            (ur'\bزی(ر|رِ)انتظام\b', ur'زی\1 انتظام'),
            (ur'\bزیرصدارت\b', ur'زیر صدارت'),
            (ur'\bزیر\s*صدارت میں\b', ur'زیر صدارت'),
            (ur'\bسائنسدان\b', ur'سائنس دان'),
            (ur'\bسختگیر\b', ur'سخت گیر'),
            (ur'\bسرانجام\b', ur'سر انجام'),
            (ur'\bسر\s+شار\b', ur'سرشار'),
            (ur'\bسونچنا\b', ur'سوچنا'),
            (ur'\bسوجا\b', ur'سو جا'),
            (ur'\bسوجائیں\b', ur'سو جائیں'),
            (ur'\bسوجاؤ\b', ur'سو جاؤ'),
            (ur'\bسوجانا\b', ur'سو جانا'),
            (ur'\bسوجاؤں\b', ur'سو جاؤں'),
            (ur'\bسوجاؤنگا\b', ur'سو جاؤنگا'),
            (ur'\bسوجائے\b', ur'سو جائے'),
            (ur'\bسوگیا\b', ur'سو گیا'),
            (ur'\bسوگئی\b', ur'سو گئی'),
            (ur'\bسوگئے\b', ur'سو گئے'),
            (ur'\bسوگئیں\b', ur'سو گئیں'),
            (ur'\bسورہا\b', ur'سو رہا'),
            (ur'\bسورہی\b', u'سو رہی'),
            (ur'\bسورہے\b', ur'سو رہے'),
            (ur'\bسقہ\b', ur'سقا'),
            (ur'\bسندیسہ\b', ur'سندیسا'),
            (ur'\bسہرہ\b', ur'سہرا'),
            (ur'\bسترنگہ\b', ur'سترنگا'),
            (ur'\bسموسا\b', ur'سموسہ'),
            (ur'\bسرگزشت\b', ur'سرگذشت'),
            (ur'\bسفیدپوش\b', ur'سفید پوش'),
            (ur'\bسن (ولادت|پیدائش|وفات|تاسیس)\b', ur'سنہ \1'),
            (ur'\bسوئم\b', ur'سوم'),
            (ur'\bسہولیت\b', ur'سہولت'),
            (ur'\bسیاستدان\b', ur'سیاست دان'),
            (ur'\bسیاستداں\b', ur'سیاست داں'),
            (ur'\bسیاستدانوں\b', ur'سیاست دانوں'),
            (ur'\bسے', ur'سے '),
            (ur'\bسے  ', ur'سے '),
            (ur'شاءاللہ\b', ur'شاء اللہ'),
            (ur'\bشکرگ(ذ|ز)ا(ر|ری)\b', ur'شکر گزا\2'),
            (ur'\bشعراء\b', ur'شعرا'),
            (ur'\bشمارندہ\b', ur'کمپیوٹر'),
            (ur'\bشمبہ\b', ur'شنبہ'),
            (ur'\bشھر\b', ur'شہر'),
            (ur'\bشهر\b', ur'شہر'),
            (ur'\bشئی\b', ur'شے'),
            (ur'\bشئے\b', ur'شے'),
            (ur'\bصبر\s*و\s*شکر\b', ur'صبر و شکر'),
            (ur'\bصحراء\b', ur'صحرا'),
            (ur'\bصورتحال\b', ur'صورت حال'),
            (ur'\bصوفیاء\b', ur'صوفیا'),
            (ur'\bطبیعات\b', ur'طبیعیات'),
            (ur'\bطاهر\b', ur'طاہر'),
            (ur'\bطپش\b', ur'تپش'),
            (ur'\bطرزیات\b', ur'ٹیکنالوجی'),
            (ur'\bطق\b', ur'کلک'),
            (ur'\bطلاطم\b', ur'تلاطم'),
            (ur'\bطلباء\b', ur'طلبہ'),
            (ur'\bطلبا\b', ur'طلبہ'),
            (ur'\bطلبائے\b', ur'طلبۂ'),
            (ur'\bطلباے\b', ur'طلبہ'),
            (ur'\bعالم متجر\b', ur'عالم متبحر'),
            (ur'\bعبد', ur'عبد '),
            (ur'\bعبد  ', ur'عبد '),
            (ur'\bعبد ہ\b', ur'عبدہ'),
            (ur'\bعبید', ur'عبید '),
            (ur'\bعبید  ', ur'عبید '),
            (ur'\bعلاؤالدین\b', ur'علاؤ الدین'),
            (ur'\bعلاؤالدین\b', ur'علاؤ الدین'),
            (ur'\bعلیحدہ\b', ur'علاحدہ'),
            (ur'\bعلیٰحدہ\b', ur'علاحدہ'),
            (ur'\bعلماء\b', ur'علما'),
            (ur'\bعمارات کو\b', ur'عمارتوں کو'),
            (ur'\bعمبر\b', ur'عنبر'),
            (ur'\bعیدالضحی\b', ur'عید الاضحیٰ'),
            (ur'\bغلتاں\b', ur'غلطاں'),
            (ur'\bغنڈا\b', ur'غنڈہ'),
            (ur'\bغبارا\b', ur'غبارہ'),
            (ur'\bغرضیکہ\b', ur'غرض کہ'),
            (ur'\bغور\s*و\s*فکر\b', ur'غور و فکر'),
            (ur'\bغیر(?!\s)(?!۔)(?!،)(?!ت)(?!و)(?!ی)(?!\n)', ur'غیر '),
            (ur'\bغیض و غضب\b', ur'غیظ و غضب'),
            (ur'\bغیض وغضب\b', ur'غیظ و غضب'),
            (ur'\bغیظ غضب\b', ur'غیظ و غضب'),
            (ur'\bغیض غضب\b', ur'غیظ و غضب'),
            (ur'\bفاہدہ\b', ur'فائدہ'),
            (ur'\bفٹبال\b', ur'فٹ بال'),
            (ur'\bفٹبالر\b', ur'فٹ بال کھلاڑی'),
            (ur'\bفرمانبردار\b', ur'فرماں بردار'),
            (ur'\bفرمانبرداری\b', ur'فرماں برداری'),
            (ur'\bفقہاء\b', ur'فقہا'),
            (ur'\bفلحال\b', ur'فی الحال'),
            (ur'\bفلوقت\b', ur'فی الوقت'),
            (ur'\bفلاتو\b', ur'فالتو'),
            (ur'\bفلکیاتدان\b', ur'فلکیات دان'),
            (ur'\bفوتگی\b', ur'وفات'),
            (ur'\bفی البدیہ\b', ur'فی البدیہہ'),
            (ur'\bقانون پاس\b', ur'قانون منظور'),
            (ur'\bقاہم\b', ur'قائم'),
            (ur'\bقائدِاعظم\b', ur'قائدِ اعظم'),
            (ur'\bقائداعظم\b', ur'قائد اعظم'),
            (ur'\bقبل،\b', ur'قبل'),
            (ur'\bقراداد', ur'قرارداد'),
            (ur'\bقرار\s+داد\b', ur'قرارداد'),
            (ur'\bقنون\b', ur'قانون'),
            (ur'\bقہقہ\b', ur'قہقہہ'),
            (ur'\bکا ممبر\b', ur'کا رکن'),
            (ur'\bکبزہ\b', ur'قبضہ'),
            (ur'\bکردیا\b', ur'کر دیا'),
            (ur'\bکردے\b', ur'کر دے'),
            (ur'\bکردیں\b', ur'کر دیں'),
            (ur'\bکردیئے\b', ur'کر دیے'),
            (ur'\bکرکٹر\b', ur'کرکٹ کھلاڑی'),
            (ur'\bکرلیں\b', ur'کر لیں'),
            (ur'\bکررہے\b', ur'کر رہے'),
            (ur'\bکروادیں\b', ur'کروا دیں'),
            (ur'\bکلمہ شناخت\b', ur'پاس ورڈ'),
            (ur'\bکلمۂ شناخت\b', ur'پاس ورڈ'),
            (ur'\bکھنبا\b', ur'کھمبا'),
            (ur'\bکہ،\b', ur'کہ'),
            (ur'\bکئ\b', ur'کئی'),
            (ur'\bکوئ\b', ur'کوئی'),
            (ur'\bکیاگیا\b', ur'کیا گیا'),
            (ur'\bکئے\b', ur'کیے'),
            (ur'\bکیلیے\b', ur'کے لیے'),
            (ur'\bکیلیئے\b', ur'کے لیے'),
            (ur'\bکیمرہ\b', ur'کیمرا'),
            (ur'\bکٹورہ\b', ur'کٹورا'),
            (ur'\bکھاجہ\b', ur'کھاجا'),
            (ur'\bکهتے\b', ur'کہتے'),
            (ur'\bکرتہ\b', ur'کرتا'),
            (ur'\bکمہار\b', ur'کمھار'),
            (ur'\bکاروائی\b', ur'کارروائی'),
            (ur'\bکولہو\b', ur'کولھو'),
            (ur'\bکھنڈرات\b', ur'کھنڈر'),
            (ur'\bکلھاڑا\b', ur'کلہاڑا'),
            (ur'\bکلیجہ\b', ur'کلیجا'),
            (ur'\bکے بجائے\b', ur'کی بجائے'),
            (ur'\bکے', ur'کے '),
            (ur'\bکے  ', ur'کے '),
            (ur'\bکے ممبر\b', ur'کے ارکان'),
            (ur'\bگزرراہ\b', ur'گزر راہ'),
            (ur'\bگذارش\b', ur'گزارش'),
            (ur'\bگذار\b', ur'گزار'),
            (ur'\bگذاری\b', ur'گزاری'),
            (ur'\bگذارا\b', ur'گزارا'),
            (ur'\bگذارے\b', ur'گزارے'),
            (ur'\bگذاریں\b', ur'گزاریں'),
            (ur'\bگذر\b', ur'گزر'),
            (ur'\bگذرا\b', ur'گزرا'),
            (ur'\bگذری\b', ur'گزری'),
            (ur'\bگذرے\b', ur'گزرے'),
            (ur'\bگذارہ\b', ur'گزارہ'),
            (ur'\bگذرنا\b', ur'گزرنا'),
            (ur'\bگمبد\b', ur'گنبد'),
            (ur'\bگوارہ\b', ur'گوارا'),
            (ur'\bگھانس\b', ur'گھاس'),
            (ur'\bگھونسلہ\b', ur'گھونسلا'),
            (ur'\bگئ\b', ur'گئی'),
            (ur'\bلاء\b', ur'لا'),
            (ur'\bلاپرواہی\b', ur'لاپروائی'),
            (ur'\bلاچار\b', ur'ناچار'),
            (ur'\bلاھور\b', ur'لاہور'),
            (ur'\bلہذہ\b', ur'لہذا'),
            (ur'\bلہٰذہ\b', ur'لہذا'),
            (ur'\bلئے\b', ur'لیے'),
            (ur'\bلیئے\b', ur'لیے'),
            (ur'\bماشا\b', ur'ماشہ'),
            (ur'\bماشاءاللہ\b', ur'ما شاء اللہ'),
            (ur'\bماهر\b', ur'ماہر'),
            (ur'\bمایع\b', ur'مائع'),
            (ur'\bمالیدا\b', ur'مالیدہ'),
            (ur'\bمتابادل\b', ur'متبادل'),
            (ur'\bمتجر عالم\b', ur'متبحر عالم'),
            (ur'\bمتنازعہ\b', ur'متنازع'),
            (ur'\bمتصفح جال\b', ur'ویب براؤزر'),
            (ur'\bمچلکہ\b', ur'مچلکا'),
            (ur'\bمحاز\b', ur'محاذ'),
            (ur'\bمحتاجگی\b', ur'محتاجی'),
            (ur'\bمدعہ\b', ur'مدعا'),
            (ur'\bمذھب\b', ur'مذہب'),
            (ur'\bمذهبی\b', ur'مذہبی'),
            (ur'\bمربہ\b', ur'مربا'),
            (ur'\bمزگاں\b', ur'مژگاں'),
            (ur'\bمزدہ\b', ur'مژدہ'),
            (ur'\bمزہب\b', ur'مذہب'),
            (ur'\bمسالہ\b', ur'مسالا'),
            (ur'\bمستفی\b', ur'مستعفی'),
            (ur'\bمس(ر|رّ)د\b', ur'اشاریہ'),
            (ur'\bمشورا\b', ur'مشورہ'),
            (ur'\bمشھور\b', ur'مشہور'),
            (ur'\bمصرعہ\b', ur'مصرع'),
            (ur'\bمعاهدہ\b', ur'معاہدہ'),
            (ur'\bمعرکۃ الآرا\b', ur'معرکہ آرا'),
            (ur'\bمعرکۃ الآراء\b', ur'معرکہ آرا'),
            (ur'\bمعرکہ الآراء\b', ur'معرکہ آرا'),
            (ur'\bمعرکہ الآرا\b', ur'معرکہ آرا'),
            (ur'\bمعمہ\b', ur'معما'),
            (ur'\bموقعہ\b', ur'موقع'),
            (ur'\bمکتبۂ فکر\b', ur'مکتب فکر'),
            (ur'\bمکتبہ فکر\b', ur'مکتب فکر'),
            (ur'\bملف\b', ur'فائل'),
            (ur'\bممبران\b', ur'ارکان'),
            (ur'\bمنزلا\b', ur'منزلہ'),
            (ur'\bمنشاء\b', ur'منشا'),
            (ur'\bمنهوس\b', ur'منحوس'),
            (ur'\bمؤجد\b', ur'موجد'),
            (ur'\bمورثی\b', ur'موروثی'),
            (ur'\bمھربانی\b', ur'مہربانی'),
            (ur'\bمہبوت\b', ur'مبہوت'),
            (ur'\bمہندس\b', ur'انجینئر'),
            (ur'\bمیعار\b', ur'معیار'),
            (ur'\bناطہ\b', ur'ناتا'),
            (ur'\bناشتہ\b', ur'ناشتا'),
            (ur'\bناراضگی\b', ur'ناراضی'),
            (ur'\bناواقفی\b', ur'ناواقفیت'),
            (ur'\bنشاندہی\b', ur'نشان دہی'),
            (ur'\bنصیبہ\b', ur'نصیبا'),
            (ur'\bنظری[ئع]ہ\b', ur'نظریہ'),
            (ur'\bنظری[ئع]ے\b', ur'نظریے'),
            (ur'\bنقشا\b', ur'نقشہ'),
            (ur'\bنفاز\b', ur'نفاذ'),
            (ur'\bنقص امن\b', ur'نقض امن'),
            (ur'\bنقطہ چینی\b', ur'نکتہ چینی'),
            (ur'\bنقطہ چین\b', ur'نکتہ چیں'),
            (ur'\bنقطہ چیں\b', ur'نکتہ چیں'),
            (ur'\bنقطہ چینیاں\b', ur'نکتہ چینیاں'),
            (ur'\bنگہت\b', ur'نکہت'),
            (ur'ں(?=[اآٱبپتۃٹثجچحخدڈذرڑزژسشصضطظعغفقکلمنںؤوہھءیئۓًٌَُِّٰ])', ur'ں '),
            (ur'\bوابسط(ہ|گی)\b', ur'وابست\1'),
            (ur'\bوجۂ\b', ur'وجہ'),
            (ur'\bوزیراعظم\b', ur'وزیر اعظم'),
            (ur'(?<!\s)(\w+)ونگا\b', ur'\1وں گا'),
            (ur'(?<!\s)(\w+)ؤنگا\b', ur'\1ؤں گا'),
            (ur'(?<!\s)(\w+)ؤنگا\b', ur'\1ؤں گا'),
            (ur'\bوطیرہ\b', ur'وتیرہ'),
            (ur'\bوکلاء\b', ur'وکلا'),
            (ur'\bوکیپیڈیا\b', ur'ویکیپیڈیا'),
            (ur'\bہاء\b', ur'ہا'),
            (ur'\bہرجا\b', ur'ہرجہ'),
            (ur'\bھمارا\b', ur'ہمارا'),
            (ur'\bھمارے\b', ur'ہمارے'),
            (ur'\bھمیں\b', ur'ہمیں'),
            (ur'\bهے\b', ur'ہے'),
            (ur'\bھاں\b', ur'ہاں'),
            (ur'\bھاتھ\b', ur'ہاتھ'),
            (ur'\bھاتھی\b', ur'ہاتھی'),
            (ur'\bھیبت\b', ur'ہیبت'),
            (ur'\bھلاک\b', ur'ہلاک'),
            (ur'\bھزار\b', ur'ہزار'),
            (ur'\bهجرت\b', ur'ہجرت'),
            (ur'\bهاتھ\b', ur'ہاتھ'),
            (ur'\bهزاروں\b', ur'ہزاروں'),
            (ur'\bهزار\b', ur'ہزار'),
            (ur'\bہندسیات\b', ur'انجینئری'),
            (ur'\bهی\b', ur'ہی'),
            (ur'\bهوں\b', ur'ہوں'),
            (ur'\bہؤا\b', ur'ہوا'),
            (ur'\bہوسکا\b', ur'ہو سکا'),
            (ur'\bہوسکے\b', ur'ہو سکے'),
            (ur'\bہوسکی\b', ur'ہو سکی'),
            (ur'\bہوگیا\b', ur'ہو گیا'),
            (ur'\bہوگئی\b', ur'ہو گئی'),
            (ur'\bہوگئے\b', ur'ہو گئے'),
            (ur'ھئے\b', ur'ھیے'),
            (ur'\bکرلیا\b', ur'کر لیا'),
            (ur'\bیهاں\b', ur'یہاں'),
            (ur'\bیهیں\b', ur'یہیں'),
            (ur'\bابولحسن\b', ur'ابو الحسن'),
            (ur'\bابولفضل\b', ur'ابو الفضل'),
            (ur'\bپنچائیت\b', ur'پنچائت'),
            (ur'\bسرائیت\b', ur'سرایت'),
            (ur'\bپذیر\b', ur'پزیر'),
            (ur'\bقوائد\b', ur'قواعد'),
            (ur'\bگوارہ\b', ur'گوارا'),
            (ur'\bگئ\b', ur'گئی'),
            (ur'\bمتابادل\b', ur'متبادل'),
            (ur'\bمستفی\b', ur'مستعفی'),
            (ur'\bمطمع نظر\b', ur'مطمح نظر'),
            (ur'\bممبران\b', ur'ارکان'),
            (ur'\bنھیں\b', ur'نہیں'),
            (ur'\bھم\b', ur'ہم'),
            (ur'\b(ھ|ہ)مجاء?\b', ur'ہم جا'),
            (ur'\bھمیں\b', ur'ہمیں'),
            (ur'\bھے\b', ur'ہے'),
            (ur'\bھاں\b', ur'ہاں'),
            (ur'\bھاتھ\b', ur'ہاتھ'),
            (ur'ۓ\b', ur'ئے'),
            (ur'\bھیں\b', ur'ہیں'),
            (ur'\bھی\b', ur'ہی'),
            (ur'\bمصنع لطیف\b', ur'سافٹ ویئر'),
            (ur'\bجالبین\b', ur'انٹرنیٹ'),
            (ur'\bہئیت\b', ur'ہیئت'),
            (ur'\bحبالہ محیط عالم\b', ur'ورلڈ وائڈ ویب'),
            (ur'\bسافٹویئر\b', ur'سافٹ ویئر'),
            (ur'\bلکھنو\b', ur'لکھنؤ'),
            (ur'\bاخراجہ\b', ur'نسخہ'),
            (ur'ے(?=[اآٱبپتۃٹثجچحخدڈذرڑزژسشصضطظعغفقکلمنںؤوہھءیئۓًٌَُِّٰ])', ur'ے '),
            (ur'\bیکسانیت\b', ur'یکسانی'),
            (ur'\b\s+،\s+\b', ur'، '),
            (ur'\b\s+۔\s+\b', ur'۔ '),
            (u' ؟', u'؟'),
            (u' !', u'!'),
            (ur'،\s+اور\b', ur' اور'),
            (ur'،\s+یا\b', ur' یا'),
            (ur'\n\(\d+\)', ur'#'),
            (ur'\n([*#]+)(?!\s)(?![*#]+)', ur'\1 '),
            (ur'\n([#*]+)\s{2,}', ur'\1 '),
            (ur'\n[•●⚫⬤]', ur'*'),
            (ur'==\s*مزید\s*دیکھیں\s*==', ur'== مزید دیکھیے =='),
            (ur'(<ref>.+?</ref>)\s*۔', ur'۔\1'),
            (ur'(<ref>.+?</ref>)\s*،', ur'،\1'),
            (u'۔ <ref', u'۔<ref'),
            (ur'([اآٱبپتۃٹثجچحخدڈذرڑزژسشصضطظعغفقکلمنںؤوہھءیئۓًٌَُِّٰ])\.', ur'\1۔'),
            (ur'([اآٱبپتۃٹثجچحخدڈذرڑزژسشصضطظعغفقکلمنںؤوہھءیئۓًٌَُِّٰ])\,', ur'\1،'),
            (ur'۔([اآٱبپتۃٹثجچحخدڈذرڑزژسشصضطظعغفقکلمنںؤوہھءیئۓًٌَُِّٰ])', ur'۔ \1'),
            (ur'\bھوتا\b', ur'ہوتا'),                     
        ],
        'exceptions': {
            'inside-tags': [
                'interwiki',
                'math',
                'link',
                'template',
            ],
        }
    },


    # Corrections for Arabic Wikipedia and any Arabic wiki.
    #   python replace.py -fix:correct-ar -start:! -always

    'correct-ar': {
        'regex': True,
        'msg': {
            'ar': u'تدقيق إملائي',
        },
        'replacements': [
            # FIXME: Do not replace comma in non-Arabic text,
            # interwiki, image links or <math> syntax.
            #   (u' ,', u' ،'),
            # TODO: Basic explanation in English what it does
            (r'\bإمرأة\b', 'امرأة'),
            (r'\bالى\b', 'إلى'),
            (r'\bإسم\b', 'اسم'),
            (r'\bالأن\b', 'الآن'),
            (r'\bالة\b', 'آلة'),
            (r'\bفى\b', 'في'),
            (r'\bإبن\b', 'ابن'),
            (r'\bإبنة\b', 'ابنة'),
            (r'\bإقتصاد\b', 'اقتصاد'),
            (r'\bإجتماع\b', 'اجتماع'),
            (r'\bانجيل\b', 'إنجيل'),
            (r'\bاجماع\b', 'إجماع'),
            (r'\bاكتوبر\b', 'أكتوبر'),
            (r'\bإستخراج\b', 'استخراج'),
            (r'\bإستعمال\b', 'استعمال'),
            (r'\bإستبدال\b', 'استبدال'),
            (r'\bإشتراك\b', 'اشتراك'),
            (r'\bإستعادة\b', 'استعادة'),
            (r'\bإستقلال\b', 'استقلال'),
            (r'\bإنتقال\b', 'انتقال'),
            (r'\bإتحاد\b', 'اتحاد'),
            (r'\bاملاء\b', 'إملاء'),
            (r'\bإستخدام\b', 'استخدام'),
            (r'\bأحدى\b', 'إحدى'),
            (r'\bلاكن\b', 'لكن'),
            (r'\bإثنان\b', 'اثنان'),
            (r'\bإحتياط\b', 'احتياط'),
            (r'\bإقتباس\b', 'اقتباس'),
            (r'\bادارة\b', 'إدارة'),
            (r'\bابناء\b', 'أبناء'),
            (r'\bالانصار\b', 'الأنصار'),
            (r'\bاشارة\b', 'إشارة'),
            (r'\bإقرأ\b', 'اقرأ'),
            (r'\bإمتياز\b', 'امتياز'),
            (r'\bارق\b', 'أرق'),
            (r'\bاللة\b', 'الله'),
            (r'\bإختبار\b', 'اختبار'),
            (r'== ?روابط خارجية ?==', '== وصلات خارجية =='),
            (r'\bارسال\b', 'إرسال'),
            (r'\bإتصالات\b', 'اتصالات'),
            (r'\bابو\b', 'أبو'),
            (r'\bابا\b', 'أبا'),
            (r'\bاخو\b', 'أخو'),
            (r'\bاخا\b', 'أخا'),
            (r'\bاخي\b', 'أخي'),
            (r'\bاحد\b', 'أحد'),
            (r'\bاربعاء\b', 'أربعاء'),
            (r'\bاول\b', 'أول'),
            (r'\b(ال|)اهم\b', r'\1أهم'),
            (r'\b(ال|)اثقل\b', r'\1أثقل'),
            (r'\b(ال|)امجد\b', r'\1أمجد'),
            (r'\b(ال|)اوسط\b', r'\1أوسط'),
            (r'\b(ال|)اشقر\b', r'\1أشقر'),
            (r'\b(ال|)انور\b', r'\1أنور'),
            (r'\b(ال|)اصعب\b', r'\1أصعب'),
            (r'\b(ال|)اسهل\b', r'\1أسهل'),
            (r'\b(ال|)اجمل\b', r'\1أجمل'),
            (r'\b(ال|)اقبح\b', r'\1أقبح'),
            (r'\b(ال|)اطول\b', r'\1أطول'),
            (r'\b(ال|)اقصر\b', r'\1أقصر'),
            (r'\b(ال|)اسمن\b', r'\1أسمن'),
            (r'\b(ال|)اذكى\b', r'\1أذكى'),
            (r'\b(ال|)اكثر\b', r'\1أكثر'),
            (r'\b(ال|)افضل\b', r'\1أفضل'),
            (r'\b(ال|)اكبر\b', r'\1أكبر'),
            (r'\b(ال|)اشهر\b', r'\1أشهر'),
            (r'\b(ال|)ابطأ\b', r'\1أبطأ'),
            (r'\b(ال|)اماني\b', r'\1أماني'),
            (r'\b(ال|)احلام\b', r'\1أحلام'),
            (r'\b(ال|)اسماء\b', r'\1أسماء'),
            (r'\b(ال|)اسامة\b', r'\1أسامة'),
            (r'\bابراهيم\b', 'إبراهيم'),
            (r'\bاسماعيل\b', 'إسماعيل'),
            (r'\bايوب\b', 'أيوب'),
            (r'\bايمن\b', 'أيمن'),
            (r'\bاوزبكستان\b', 'أوزبكستان'),
            (r'\bاذربيجان\b', 'أذربيجان'),
            (r'\bافغانستان\b', 'أفغانستان'),
            (r'\bانجلترا\b', 'إنجلترا'),
            (r'\bايطاليا\b', 'إيطاليا'),
            (r'\bاوربا\b', 'أوروبا'),
            (r'\bأوربا\b', 'أوروبا'),
            (r'\bاوغندة\b', 'أوغندة'),
            (r'\b(ال|)ا(لماني|فريقي|سترالي)(ا|ة|تان|ان|ين|ي|ون|و|ات|)\b',
             r'\1أ\2\3'),
            (r'\b(ال|)ا(وروب|مريك)(ا|ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b',
             r'\1أ\2\3'),
            (r'\b(ال|)ا(ردن|رجنتين|وغند|سبان|وكران|فغان)'
             r'(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b',
             r'\1أ\2\3'),
            (r'\b(ال|)ا(سرائيل|يران|مارات|نكليز|نجليز)'
             r'(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b',
             r'\1إ\2\3'),
            (r'\b(ال|)(ا|أ)(رثوذكس|رثوذوكس)(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b',
             r'\1أرثوذكس\4'),
            (r'\bإست(عمل|خدم|مر|مد|مال|عاض|قام|حال|جاب|قال|زاد|عان|طال)(ت|ا|وا|)\b',
             r'است\1\2'),
            (r'\bإست(حال|قال|طال|زاد|عان|قام|راح|جاب|عاض|مال)ة\b', r'است\1ة'),
        ],
        'exceptions': {
            'inside-tags': [
                'interwiki',
                'math',
                'ref',
            ],
        }
    },
    # TODO: Support dynamic replacement from Special pages to the localized one
    'specialpages': {
        'regex': False,
        'msg': {
            'en': u'Robot: Fixing special page capitalisation',
            'fa': u'ربات: تصحیح بزرگی و کوچکی حروف صفحه‌های ویژه',
        },
        'replacements': [
            (u'Special:Allpages',        u'Special:AllPages'),
            (u'Special:Blockip',         u'Special:BlockIP'),
            (u'Special:Blankpage',       u'Special:BlankPage'),
            (u'Special:Filepath',        u'Special:FilePath'),
            (u'Special:Globalusers',     u'Special:GlobalUsers'),
            (u'Special:Imagelist',       u'Special:ImageList'),
            (u'Special:Ipblocklist',     u'Special:IPBlockList'),
            (u'Special:Listgrouprights', u'Special:ListGroupRights'),
            (u'Special:Listusers',       u'Special:ListUsers'),
            (u'Special:Newimages',       u'Special:NewImages'),
            (u'Special:Prefixindex',     u'Special:PrefixIndex'),
            (u'Special:Protectedpages',  u'Special:ProtectedPages'),
            (u'Special:Recentchanges',   u'Special:RecentChanges'),
            (u'Special:Specialpages',    u'Special:SpecialPages'),
            (u'Special:Unlockdb',        u'Special:UnlockDB'),
            (u'Special:Userlogin',       u'Special:UserLogin'),
            (u'Special:Userlogout',      u'Special:UserLogout'),
            (u'Special:Whatlinkshere',   u'Special:WhatLinksHere'),
        ],
    },
    # yu top-level domain will soon be disabled, see
    # http://lists.wikimedia.org/pipermail/wikibots-l/2009-February/000290.html
    # The following are domains that are often-used.
    'yu-tld': {
        'regex': False,
        'nocase': True,
        'msg': {
            'de':  u'Bot: Ersetze Links auf .yu-Domains',
            'en':  u'Robot: Replacing links to .yu domains',
            'fa':  u'ربات: جایگزینی پیوندها به دامنه‌ها با پسوند yu',
            'fr':  ('Robot: Correction des liens pointant vers le domaine '
                    '.yu, qui expire en 2009'),
            'ksh': u'Bot: de ahle .yu-Domains loufe us, dröm ußjetuusch',
        },
        'replacements': [
            (u'www.budva.cg.yu',             u'www.budva.rs'),
            (u'spc.org.yu',                  u'spc.rs'),
            (u'www.oks.org.yu',              u'www.oks.org.rs'),
            (u'www.kikinda.org.yu',          u'www.kikinda.rs'),
            (u'www.ds.org.yu',               u'www.ds.org.rs'),
            (u'www.nbs.yu',                  u'www.nbs.rs'),
            (u'www.serbia.sr.gov.yu',        u'www.srbija.gov.rs'),
            (u'eunet.yu',                    u'eunet.rs'),
            (u'www.zastava-arms.co.yu',      u'www.zastava-arms.co.rs'),
            (u'www.airportnis.co.yu',        u'www.airportnis.rs'),
            # Archive links don't seem to work
            # (u'www.danas.co.yu',             u'www.danas.rs'),
            (u'www.belex.co.yu',             u'www.belex.rs'),
            (u'beograd.org.yu',              u'beograd.rs'),
            (u'www.vlada.cg.yu',             u'www.vlada.me'),
            (u'webrzs.statserb.sr.gov.yu',   u'webrzs.stat.gov.rs'),
            (u'www.statserb.sr.gov.yu',      u'webrzs.stat.gov.rs'),
            (u'www.rastko.org.yu',           u'www.rastko.org.rs'),
            (u'www.reprezentacija.co.yu',    u'www.reprezentacija.rs'),
            (u'www.blic.co.yu',              u'www.blic.co.rs'),
            (u'www.beograd.org.yu',          u'www.beograd.org.rs'),
            (u'arhiva.glas-javnosti.co.yu',  u'arhiva.glas-javnosti.rs'),
            (u'www.srpsko-nasledje.co.yu',   u'www.srpsko-nasledje.co.rs'),
            (u'www.dnevnik.co.yu',           u'www.dnevnik.rs'),
            (u'www.srbija.sr.gov.yu',        u'www.srbija.gov.rs'),
            (u'www.kurir-info.co.yu/Arhiva', u'arhiva.kurir-info.rs/Arhiva'),
            (u'www.kurir-info.co.yu/arhiva', u'arhiva.kurir-info.rs/arhiva'),
            (u'www.kurir-info.co.yu',        u'www.kurir-info.rs'),
            (u'arhiva.kurir-info.co.yu',     u'arhiva.kurir-info.rs'),
            (u'www.prvaliga.co.yu',          u'www.prvaliga.rs'),
            (u'www.mitropolija.cg.yu',       u'www.mitropolija.me'),
            (u'www.spc.yu/sr',               u'www.spc.rs/sr'),
            (u'www.sk.co.yu',                u'www.sk.co.rs'),
            (u'www.ekoforum.org.yu',         u'www.ekoforum.org'),
            (u'www.svevlad.org.yu',          u'www.svevlad.org.rs'),
            (u'www.posta.co.yu',             u'www.posta.rs'),
            (u'www.glas-javnosti.co.yu',     u'www.glas-javnosti.rs'),
            (u'www.fscg.cg.yu',              u'www.fscg.co.me'),
            (u'ww1.rts.co.yu/euro',          u'ww1.rts.co.rs/euro'),
            (u'www.rtv.co.yu',               u'www.rtv.rs'),
            (u'www.politika.co.yu',          u'www.politika.rs'),
            (u'www.mfa.gov.yu',              u'www.mfa.gov.rs'),
            (u'www.drzavnauprava.sr.gov.yu', u'www.drzavnauprava.gov.rs'),
        ],
    },
    # These replacements will convert HTML tag from FCK-editor to wiki syntax.
    #
    'fckeditor': {
        'regex': True,
        'msg': 'pywikibot-fixes-fckeditor',
        'replacements': [
            # replace <br> with a new line
            (r'(?i)<br>',                      r'\n'),
            # replace &nbsp; with a space
            (r'(?i)&nbsp;',                      r' '),
        ],
    },
}


def _load_file(filename):
    """Load the fixes from the given filename."""
    if os.path.exists(filename):
        # load binary, to let compile decode it according to the file header
        with open(filename, 'rb') as f:
            exec(compile(f.read(), filename, 'exec'), globals())
        return True
    else:
        return False


# Load the user fixes file.
filename = config.datafilepath('user-fixes.py')
if _load_file(filename):
    user_fixes_loaded = True
else:
    user_fixes_loaded = False
