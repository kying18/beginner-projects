adj = input("Adjective: ")
verb1 = input("Verb: ")
verb2 = input("Verb: ")
famous_person = input("Famous person: ")

madlib = "Computer programming is so {adj}! It makes me so excited all \
the time because I love to {verb1}. Stay hydrated and {verb2} like you are \
{famous_person}".format(adj=adj, verb1=verb1, verb2=verb2, famous_person=famous_person)

print(madlib)