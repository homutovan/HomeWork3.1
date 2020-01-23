def json_spider(parent, description_list = []):

    for item in parent:
        if type(parent) == list:
            json_spider(item)
        elif type(parent[item]) != str:
            json_spider(parent[item])
        elif len(parent[item]) > 150:
            description_list.append(parent[item])

    return description_list   

def json_parser(filename):
    
    import json

    try:
        with open(filename) as datafile:
            json_data = json.load(datafile)
    except Exception as e:
        print('Ошибка открытия файла', e)
        return []

    description_list = json_spider(json_data)

    return description_list

def xml_spider(parent_element, description_list = []):

    for element in parent_element:
        if len(element.text) > 150:
            description_list.append(element.text)
        xml_spider(element)
    return description_list

def xml_parser(filename):
    
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(filename)
    except Exception as e:
        print('Ошибка открытия файла', e)
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
                    word_dict[word] = 1
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