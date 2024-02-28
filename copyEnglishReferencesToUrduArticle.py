# Copy Reference from English Article to Urdu Pageimport mwparserfromhell as mwp
import sys
import pywikibot
import mwparserfromhell as mwp
from scripts import noreferences
from scripts import reflinks

# function not used to access key based on value
def search(myDict, search1):
    for key, value in myDict.items():
        if search1 in value:
            return key


def write_output(newtext, filename):
    import time
    import os
    baseDir = r'D:\Wikipedia\code_output'
    newfile = os.path.join(baseDir, filename)

    with open(newfile, 'w', encoding='utf8') as fout:
        print('Printing appended Urdu Page', time.ctime(), file=fout)
        print(newtext, file=fout)


# Extracting sfn templates and converting them in REF tags
sfnlist = []
sfn = ('sfn', '<sfn>', '</sfn>', 'sfnp', '<sfnp>', '</sfnp>', 'r')

def refTagForming(wikicode):
    i = 1
    reftags = {}

    # Surrounding sfn templates with tags
    for template in wikicode.filter_templates():
        if template.name in sfn:
            if template.name == 'sfn':
                if template not in sfnlist:
                    sfnlist.append(template)
                templ_rep = sfn[1] + str(template) + sfn[2]
            elif template.name == 'r':  # Handling new case of 'r' tag
                templ_rep = '<r>' + str(template) + '</r>'
            else:
                templ_rep = sfn[4] + str(template) + sfn[5]
            wikicode.replace(template, templ_rep)


    #alltags = wikicode.filter_tags()
    # Creating Dictionary of References, ref num as key and  vales (reference name and link  as tuple)
    for tag in wikicode.filter_tags():
        if tag.tag in ('ref', 'sfn', 'sfnp','r'):

            if tag.tag in sfn:
                refval = tag.tag
            elif tag.attributes == []:  # check if attributes list is empty
                refval = 'NoRefName'
            else:
                name = tag.attributes[0]
                refval = name.value

            if tag.contents is None:
                pass
            else:
                # creating list of second element in each tuple in dictionary reftags
                # ('sfn', '{{sfn|Jhaveri|2001|pp=149}}')
                secValTuple = [tup[1] for tup in reftags.values()]
                if tag.contents not in secValTuple:
                    reftags[i] = (refval, tag.contents)
                    i += 1

    return reftags

title = "تائیوان_کی_تاریخ"

site = pywikibot.Site('ur', 'wikipedia')
urpage = pywikibot.Page(site, title)

langlst = urpage.iterlanglinks()

interDict = {}
for i in langlst:
    lang = str(i.site).split(':')[1]
    interDict[lang] = i.title
    if lang == 'en':
        break

# If there is no inter-wiki page then exit the program
if len(interDict) == 0:
    print('Link Dictionary is empty')
    sys.exit()

eng_title = interDict['en']

site = pywikibot.Site('en', 'wikipedia')
enpage = pywikibot.Page(site, eng_title)

wikitext = enpage.get()
wikicode = mwp.parse(wikitext)


# Forming reference if tag value is either ref,sfn,sfnp
reftags = refTagForming(wikicode)

dlinks = {}
for k, v in reftags.items():
    dkey = 'و' + str(k) + 'و'
    if v[0] in sfn:
        dlinks[dkey] = str(v[1])
    else:
        dlinks[dkey] = '<ref>' + str(v[1]) + '</ref>'

urtext = urpage.text
for r in tuple(dlinks.items()):
    urtext = urtext.replace(*r)

# Removing Duplicate references by using named reference(first instance) and
# then only using named reference without content
deDupRef = reflinks.DuplicateReferences(site)
urtext = deDupRef.process(urtext)
write_output(urtext, 'AfterdeDuplicate.txt')

# Used noreferences to add Reference List in Article
norefbot = noreferences.NoReferencesBot(None)
if norefbot.lacksReferences(urtext):
    urpage.text = norefbot.addReferences(urtext)
else:
    urpage.text = urtext + '\n'

# Added for reviewing output of updated Article Text
write_output(urtext, 'FinalText.txt')

# save the page
urpage.save(summary='خودکار: اندراج حوالہ جات', minor=False)
