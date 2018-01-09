PRES_ENDINGS = {'1S':'m','2S':'š','1P':'mo','2P':'te','3P':['ju','e','u']}
HTJETI_FORMS = {'1S':'ću','2S':'ćeš','3S':'će','1P':'ćemo','2P':'ćete','3P': 'će'}
BITI_FORMS = {'1S':'sam','2S':'si','3S':'je','1P':'smo','2P':'ste','3P': 'su'}
BIH_FORMS = {'1S':'bih','2S':'bi','3S':'bi','1P':'bismo','2P':'biste','3P': 'bi'}
PAST_PART = {'SM':'o','PM':'li','SF':'la','PF':'le','SN':'lo','PN':'la'}

SOFTENED_CONS = {'b': 'blj', 'c': 'č', 'd': 'đ', 'g': 'ž', 'h': 'š', 'k': 'č', 'l': 'lj', 'm': 'mlj', 'n': 'nj', 'p': 'plj', 's': 'š', 'sl': 'šlj', 'sn': 'šnj', 'st': 'šć', 't': 'ć', 'v': 'vlj', 'z': 'ž', 'zd': 'žđ', 'zn': 'žnj'}

class Conjugation:
    ''' Take verb, pronoun, and optional tense
        Return: conjugated verb '''
    def __init__(self, verb, pronoun, tense=''):
        self.verb = verb
        self.p3 = pronoun
        self.p2 = pronoun[:-1]
        self.tense = tense

    def conjugate(self):
        ''' Filter verb into proper conjugation based on tense
        Return: conjugated verb '''
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

    def present(self, third=False):
        ''' Returns present, third var can be used to get
        third person plural for use in other tenses '''
        self.p2 = '3P' if third == True else self.p2
        verb_root = self.form_root()
        if self.p2 == '3S':
            c = verb_root
        elif self.p2 == '3P':
            if verb_root[-1] == 'a':
                c = verb_root+PRES_ENDINGS[self.p2][0]
            elif verb_root[-1] == 'i':
                c = verb_root[:-1]+PRES_ENDINGS[self.p2][1]
            elif verb_root[-1] == 'e':
                c = verb_root[:-1]+PRES_ENDINGS[self.p2][2]
        else:
            c = "{}{}".format(verb_root,PRES_ENDINGS[self.p2])
        return c

    def past(self):
        ''' Past participle + conjugation of biti '''
        verb_root = self.form_root()
        return "{}{} {}".format(verb_root, PAST_PART[self.p3[1:]], BITI_FORMS[self.p2])

    def future(self):
        ''' Conjugation of htjeti + infinitive '''
        verb_root = self.form_root()
        return "{} {}".format(self.verb, HTJETI_FORMS[self.p2])

    def conditional(self):
        ''' Past participle + conjugation of bih '''
        verb_root = self.form_root()
        return "{}{} {}".format(verb_root, PAST_PART[self.p3[1:]], BIH_FORMS[self.p2] )

    def imperative(self):
        ''' Form stem from 3rd person plural,
            ti form add -i if doesn't end in j, +te for vi, +mo for mi
            only works with 2S, 1P, 2P '''
        imp_stem = self.present(third=True)[:-1]
        if imp_stem[-1:] == 'j':
            imp = imp_stem
        elif imp_stem[-1:] != 'j':
            imp = imp_stem+'i'
        elif self.p2 == '2S':
            imp = imp_stem
        elif self.p2 == '2P':
            imp = imp_stem+'te'
        elif self.p2 == '1P':
            imp = imp_stem+'mo'
        return imp
