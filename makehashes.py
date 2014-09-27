
# coding: utf-8

import unicodedata
import string
import hashlib

def uberhasher(metadata):
    title = metadata['title']
    contributors = metadata['contributors']
    description = metadata['description']
    return(titlehash(title), contributorhash(contributors), descriptionhash(description))

def normalizestring(astring): # takes a unicode string
    # docs.python.org/2/library/unicodedata.html
    # TODO: this does not work for æ or Æ! What else?
    bstring = unicodedata.normalize('NFKD', astring).encode('ascii','ignore')
    bstring = bstring.lower()
    exclude = set(string.punctuation)
    exclude.add(' ')
    bstring = ''.join(ch for ch in bstring if ch not in exclude)
    return bstring # returns an ascii string, all stuck together

def titlehash(title): # takes a unicode string
    normalizedtitle = normalizestring(title)
    return normalizedtitle  # returns an ascii string

def descriptionhash(description): #takes a unicode string
    normdescription = normalizestring(description)
    normdescription = hashlib.md5(normdescription).hexdigest()
    return normdescription # returns an actual hash; string of hexadecimal characters

def contributorhash(contributors): # takes a list of dictionaries, unicode
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

    for metadata in somedata:
        print(uberhasher(metadata))
    




