import os
import re
import sys
stop=set(['biti','jesam','budem','sam','jesi','budeš','si','jesmo','budemo','smo','jeste','budete','ste','jesu','budu','su','bih','bijah','bjeh','bijaše','bi','bje','bješe','bijasmo','bismo','bjesmo','bijaste','biste','bjeste','bijahu','biste','bjeste','bijahu','bi','biše','bjehu','bješe','bio','bili','budimo','budite','bila','bilo','bile','ću','ćeš','će','ćemo','ćete','želim','želiš','želi','želimo','želite','žele','moram','moraš','mora','moramo','morate','moraju','trebam','trebaš','treba','trebamo','trebate','trebaju','mogu','možeš','može','možemo','možete'])

curr_dir = os.path.dirname(__file__)
transformacije=[e.strip().split('\t') for e in open(os.path.join(curr_dir, 'transformations.txt'))]
pravila=[re.compile(r'^('+osnova+')('+nastavak+r')$') for osnova, nastavak in [e.strip().split(' ') for e in open(os.path.join(curr_dir, 'rules.txt'))]]


def istakniSlogotvornoR(niz):
    return re.sub(r'(^|[^aeiou])r($|[^aeiou])',r'\1R\2',niz)

def imaSamoglasnik(niz):
    if re.search(r'[aeiouR]',istakniSlogotvornoR(niz)) is None:
        return False
    else:
        return True

def transformiraj(pojavnica):
    for trazi,zamijeni in transformacije:
        if pojavnica.endswith(trazi):
            return pojavnica[:-len(trazi)]+zamijeni
    return pojavnica

def korjenuj(pojavnica):
    for pravilo in pravila:
        dioba=pravilo.match(pojavnica)
        if dioba is not None:
            if imaSamoglasnik(dioba.group(1)) and len(dioba.group(1))>1:
                return dioba.group(1)
    return pojavnica

def create_wordlist(articletext):
    wordlist = []
    for paragraph in articletext:
        for word in paragraph.split():
            checkword = word.lower().replace('<p>','')
            if checkword not in stop and checkword.isalpha() and len(checkword) > 2:
              wordlist.append((korjenuj(transformiraj(checkword))))
    return wordlist
