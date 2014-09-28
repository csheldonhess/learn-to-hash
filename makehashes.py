# coding: utf-8

import unicodedata
import string
import hashlib

def uber_hasher(listoffunctions, listofmetadata):
    metahashlist = []
    for metadata in listofmetadata:
        listofhashes = []    
        for function in listoffunctions:
            listofhashes.append(normalize_string(function(metadata)))
        metahashlist.append(listofhashes)
    return(metahashlist) # a list of lists; each internal list goes w/ a chunk of metadata

def normalize_string(astring): # takes a unicode string or a list of strings
    # docs.python.org/2/library/unicodedata.html
    # TODO: this may not work for some unicode characters; I dealt w/
    # special cases I know about; are there others?
    # (when it fails to transliterate, it replaces with '')
    astring = astring.replace(u'æ',u'ae')
    astring = astring.replace(u'Æ',u'Ae')
    astring = astring.replace(u'ß', u'ss') # assumes good transliteration
    bstring = unicodedata.normalize('NFKD', astring).encode('ascii','ignore')
    bstring = bstring.lower()
    exclude = set(string.punctuation)
    exclude.add(' ')
    exclude.add('\n')
    bstring = ''.join(ch for ch in bstring if ch not in exclude)
    bstring = hashlib.md5(bstring).hexdigest()
    return bstring # returns a hash of the string or list

def grab_title(metadata): # takes a dictionary
    title = metadata['title']
    return title  # returns a unicode string

def grab_description(metadata): #takes a dictionary
    description = metadata['description']
    return description # returns a unicode string, possibly VERY long

def grab_contributors(metadata): # takes a dictionary
    contributors = metadata['contributors'] # this is a list
    namelist = ''
    for contributor in contributors:
        # strip middle names/initials - not going to work for honorifics, degrees
        # can we please just have surname and givenname split out?
        name = contributor['name'].split()
        fullname = name[0] + name[len(name)-1]
        namelist += fullname
    return namelist # returns a list of strings
    
if __name__ == '__main__':
    longtext = '''Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots
        in a piece of classical Latin literature from 45 BC, making it over 2000 years old. 
        Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one
        of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going 
        through the cites of the word in classical literature, discovered the undoubtable source. 
        Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" 
        (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on 
        the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, 
        "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.'''

    somedata = [{
        'title': u'OMG Penguins! Whoödly whoodly wû!',
        'contributors': [{ 
            'name': u'Mr. Popper',
            'email': u'pop@popper.pop',
        }, {
            'name': u'Abæcūs E Fįnch',
            'email': u'',
        }],
        'description': u'What if a much of a which of a wind gave truth to the summer\'s lie? Kvothe the Raven nevermore.',
    }, 
        {
        'title': u'All aböüt Ducks, yeah buddy; duçks are amazing.',
        'contributors': [{ 
            'name': u'Álbert Dūmblédore',
            'email': u'wizard@wizardingschool.wiz',
        }, {
            'name': u'Albemarle K. Jôñes',
            'email': u'yeah@maps.yeah',
        },
           {
            'name': u'Ædgär E. Cummíngs',
            'email': u'poets@poetry.poem',
        },
        ],
        'description': unicode(longtext),
    }
    ]

    print uber_hasher([grab_title, grab_description, grab_contributors], somedata)
