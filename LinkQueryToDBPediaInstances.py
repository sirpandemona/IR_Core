from DBPediaRequest import DBPediaRequest

p = DBPediaRequest('FC Barcelona')
print(p.get_related_subject_list())
p.get_all_information_on_subject()