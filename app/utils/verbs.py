import sys


HTJETI_FORMS = {'1S':'ću','2S':'ćeš','3S':'će','1P':'ćemo','2P':'ćete','3P': 'će'}
BITI_FORMS = {'1S':'sam','2S':'si','3S':'je','1P':'smo','2P':'ste','3P': 'su'}
BIH_FORMS = {'1S':'bih','2S':'bi','3S':'bi','1P':'bismo','2P':'biste','3P': 'bi'}
PAST_PART = {'SM':'o','PM':'li','SF':'la','PF':'le','NS':'lo','NP':'la'}

class Conjugation:
    ''' take verb, pronoun, and optional tense
        returns conjugated verb '''
    def __init__(self, verb, pronoun, tense=''):
        self.verb = verb
        self.pronoun = pronoun
        self.tense = tense

    def conjugate(self):
        ''' filter verb into proper conjugation based on tense
        returns conjugated verb '''
        if self.tense=='present':
            verb = self.present()
        if self.tense=='past':
            verb = self.past()
        if self.tense=='future':
            verb = self.future()
        if self.tense=='conditional':
            verb = self.conditional()
        if self.tense=='imperative':
            verb = self.imperative()
        return verb

    def form_root(self):
        verb_root=self.verb[:-2]
        return verb_root

    def present(self):
        ''' Takes pronoun in format NumberPerson, ex. ja = 1S, vi = 2P, etc. '''
        pres_endings = {'1S':'m','2S':'š','1P':'mo','2P':'te','3P':['ju','e','u']}
        verb_root = self.form_root()
        if self.pronoun == '3S':
            c = verb_root
        elif self.pronoun == '3P':
            if verb_root[-1] == 'a':
                c = verb_root+pres_endings[self.pronoun][0]
            elif verb_root[-1] == 'i':
                c = verb_root[:-1]+pres_endings[self.pronoun][1]
            elif verb_root[-1] == 'e':
                c = verb_root[:-1]+pres_endings[self.pronoun][2]
        else:
            c = "{}{}".format(verb_root,pres_endings[self.pronoun])
        return c

    def past(self):
        ''' Past participle + conjugate biti
            Takes pronoun in format NumberPersonGender, ex. Kurt Russell  = 3SM, etc. '''
        verb_root = self.form_root()
        # add masculine if no pronoun gender
        pronoun = self.pronoun+'M' if len(self.pronoun) == 2 else self.pronoun
        return "{}{} {}".format(verb_root, PAST_PART[pronoun[1:]], BITI_FORMS[pronoun[:-1]])

    def future(self):
        ''' Conjugate htjeti + inifinitive
            Takes pronoun in format NumberPerson, ex. ja = 1S, vi = 2P, etc. '''
        verb_root = self.form_root()
        pronoun = self.pronoun[:-1] if len(self.pronoun) == 3 else self.pronoun
        return "{} {}".format(self.verb, HTJETI_FORMS[pronoun])

    def conditional(self):
        ''' Past participle + conjugate bih
            Takes pronoun in format NumberPerson, ex. ja = 1S, vi = 2P, etc. '''
        verb_root = self.form_root()
        pronoun = self.pronoun+'M' if len(self.pronoun) == 2 else self.pronoun
        return "{}{} {}".format(verb_root, PAST_PART[pronoun[1:]], BIH_FORMS[pronoun[:-1]] )

    def imperative(self):
        ''' Form stem from 3rd person plural,
            ti form add -i if doesn't end in j, +te for vi, +mo for mi
            Takes pronoun in format NumberPerson, ex. ja = 1S, vi = 2P, etc.
            only works with 2S, 1P, 2P '''
        imp_stem = self.present()[-1:]
        if imp_stem[-1:] != 'j':
            imp_stem = imp_stem+'i'
        if self.pronoun == '2S':
            imp = imp_stem
        if self.pronoun == '2P':
            imp = imp_stem+'te'
        if self.pronoun == '1P':
            imp = imp_stem+'mo'
        return imp
