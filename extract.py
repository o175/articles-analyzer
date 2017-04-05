f = open('document.txt')
raw = f.read()

import nltk, re, pprint
from nltk import word_tokenize
from natasha import Combinator
from natasha.grammars import Person
from natasha.grammars.person import PersonObject
from yargy.interpretation import InterpretationEngine
tokens = word_tokenize(raw)
combinator = Combinator([
    Person,   
])


matches = combinator.resolve_matches(
    combinator.extract(raw),
)

engine = InterpretationEngine(PersonObject)

persons = list(
    engine.extract(matches)
)
array = {};
for person in persons:
    print((person.normalized_firstname, person.normalized_lastname, (persons[0].firstname.position, persons[0].lastname.position)))
