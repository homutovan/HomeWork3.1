def json_parser(filename):
    
    import json

    with open(filename) as datafile:
        json_data = json.load(datafile)

    for item in json_data['rss']['channel']['items']:
        try:
            description_list.append(item['description'])
        except NameError:
            description_list = []

    return description_list

def xml_parser(filename):

    import xml.etree.ElementTree as ET
    tree = ET.parse(filename)
    items = tree.findall('.//item')

    for item in items:
        for element in item:
            if element.tag == 'description':
                try:
                    description_list.append(element.text)
                except NameError:
                    description_list = []

    return description_list

def get_word_tuples(description_list, min_length = 6):

    for description in description_list:
        for word in description.split():
            if len(word) > min_length:
                try:
                    word_dict[word] += 1
                except KeyError: 
                    word_dict[word] = 1
                except NameError:
                    word_dict = {}

    word_tuples = list(word_dict.items())

    return(word_tuples)

def sort_word(selection, filename, json = False, xml = False):

    if json:
        description_list = json_parser(filename)
    
    if xml:
        description_list = xml_parser(filename)

    if (xml and json) or (not xml and not json):
        return 'Необходимо указать формат данных'
    
    word_tuples = get_word_tuples(description_list)
    sorted_word_tuples = sorted(word_tuples, key = lambda word_tuples: word_tuples[1])

    return sorted_word_tuples[-selection:]
  
#10 наиболее часто встречающихся слов (json)
print(sort_word(10, 'files/newsafr.json', json = True))
#10 наиболее часто встречающихся слов (xml)
print(sort_word(10, 'files/newsafr.xml', xml = True))
#Не указываем формат
print(sort_word(10, 'files/newsafr.xml'))
