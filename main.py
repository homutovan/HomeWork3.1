def json_spider(parent, description_list = []):

    if type(parent) == list:
        for item in parent:
          json_spider(item)
    else:
        for item in parent:
            if len(parent[item]) > 150:
                description_list.append(parent[item])
            if type(parent[item]) != str:
                try:
                    json_spider(parent[item])
                except TypeError:
                    continue

    return description_list

def json_parser(filename):
    
    import json

    try:
        with open(filename) as datafile:
            json_data = json.load(datafile)
    except:
        print('Файл поврежден, либо отсутствует')
        return []

    description_list = json_spider(json_data)

    return description_list

def xml_spider(parent_element, description_list = []):

    for element in parent_element:
        if len(element.text) > 150:
            description_list.append(element.text)
        xml_spider(element, description_list)
    return description_list

def xml_parser(filename):

    import xml.etree.ElementTree as ET

    try:
        tree = ET.parse(filename)
    except:
        print('Файл поврежден, либо отсутствует')
        return []

    root = tree.getroot()

    description_list = xml_spider(root)

    return description_list

def get_word_tuples(description_list, min_length = 6):
    
    if len(description_list) == 0:
        return ()
    for description in description_list:
        
        for word in description.split():
            if len(word) > min_length:
                try:
                    word_dict[word] += 1
                except KeyError: 
                    word_dict[word] = 1
                except NameError:
                    word_dict = {}
            else:
                continue

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
#print(sort_word(10, 'files/newsafr.xml'))

