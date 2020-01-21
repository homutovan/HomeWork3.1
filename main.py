import json

with open('files/newsafr.json') as datafile:
  json_data = json.load(datafile)

word_dict = {}

for item in json_data['rss']['channel']['items']:
    for word in item['description'].split():
        if len(word) > 6:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word]  += 1

word_tuples = list(word_dict.items())
sorted_word_tuples = sorted(word_tuples, key = lambda word_tuples: word_tuples[1])

#10 наиболее часто встречающихся слов
print(sorted_word_tuples[-10:])