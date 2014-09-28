
# coding: utf-8

import unicodedata
import string
import hashlib

def uberhasher(listoffunctions, listofmetadata):
    metahashlist = [] # a list of lists; each internal list goes w/ a chunk of metadata
    for metadata in listofmetadata:
        listofhashes = []    
        for function in listoffunctions:
            listofhashes.append(function(metadata))
        metahashlist.append(listofhashes)
    return(metahashlist)
    
    
    return(titlehash(title), contributorhash(contributors), descriptionhash(description))

def normalizestring(astring): # takes a unicode string
    # docs.python.org/2/library/unicodedata.html
    # TODO: this does not work for æ or Æ! What else?
    bstring = unicodedata.normalize('NFKD', astring).encode('ascii','ignore')
    bstring = bstring.lower()
    exclude = set(string.punctuation)
    exclude.add(' ')
    bstring = ''.join(ch for ch in bstring if ch not in exclude)
    bstring = hashlib.md5(bstring).hexdigest()
    return bstring # returns an ascii string, all stuck together

def titlehash(metadata): # takes a dictionary
    title = metadata['title']
    normalizedtitle = normalizestring(title)
    return normalizedtitle  # returns an ascii string

def descriptionhash(metadata): #takes a dictionary
    description = metadata['description']
    normdescription = normalizestring(description)
    return normdescription # returns an actual hash; string of hexadecimal characters

def contributorhash(metadata): # takes a dictionary
    contributors = metadata['contributors'] # this is a list
    namehash = ''
    for contributor in contributors:
        # strip middle names/initials - not going to work for honorifics, degrees
        # can we please just have surname and givenname split out?
        name = contributor['name'].split()
        fullname = name[0] + name[len(name)-1]
        normedname = normalizestring(fullname)
        namehash += normedname
    return namehash
    
if __name__ == '__main__':
    longtext = '''Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical 
        Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at 
        Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a 
        Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the 
        undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" 
        (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, 
        very popular during the Renaissance. The first line of Lorem Ipsum, "Lorem ipsum dolor sit amet..", comes from a 
        line in section 1.10.32.'''

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
        }],
        'description': unicode(longtext),
    }
    ]

    print uberhasher([titlehash, descriptionhash, contributorhash], somedata)
    




