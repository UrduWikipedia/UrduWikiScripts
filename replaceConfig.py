# -*- coding: utf-8  -*-

from __future__ import unicode_literals



"""

Configuration file for hewikiReplaceBot

-replacementsPage           list of replacements maintained by the community

-defaultSummary             prefix for summary.

-safeTemplates              templates that the bot most ignore

-safeTemplatesCategories    list of categories of templates the bot most ignore

-nobotRgx                   regex for extracting replacements ids the bot shouldn't execute in the specific page

-fileUsageRgx               Regex for file usage

-redirectRgx                Regex to identify redirects

-namespaces                 List of namespace the bot is allowed to work on

-whitelist_editors          List of editors allowed to edit the replacementsPage

"""

replacementsPage = 'ویکیپیڈیا:متداول املائی غلطیوں کی فہرستیں/برائے خودکار درستی'

defaultSummary = 'خودکار: [[وپ:خودکار درستی|درستی املا]] ← '

safeTemplates = ['ציטוט', 'ציטוטון', 'חלונית', 'מסגרת', 'הדגשה', 'קמץ קטן']

safeTemplatesCategories = ['תבניות קישורים חיצוניים', 'תבניות ציטוט']

nobotRgx = "\{\{ללא בוט\|([0-9]+)\}\}"

fileUsageRgx = '\[\[:?(File|Image|تصویر|ملف|فائل)\s*:\s*.*?[\|\]]'

redirectRgx = '#\s*(رجوع\_مکرر|REDIRECT)\s*\[\['

linkRgx = '\[\[(.*?)(\|.*?)?\]\]'

tempRgx = '\{\{(.*?)(\|.*?)?\}\}'

namespaces = [0, 4, 12, 14, 100, 118]

whitelist_editors = ['Yethrosh']

