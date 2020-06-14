from utils import arrange_animals_list
from data.animal_dictionary import animals_list
from pattern3.en import pluralize, singularize
import re


def check_animal_in_sentence(animals_set, data, per_animals_list, sentence, complex_sentence_list):
    animals_in_sentence_set = set()

    for word in sentence.split(" "):
        if word in animals_set:

            singular_animal = singularize(word)

            if singular_animal in animals_set:
                animals_in_sentence_set.add(singular_animal)
            else:
                animals_in_sentence_set.add(word)

    if len(animals_in_sentence_set) < 2:
        return
    if len(animals_in_sentence_set) == 2:
        per_animals_list.append((animals_in_sentence_set.pop(), animals_in_sentence_set.pop()))
        data.append(sentence)
        return

    complex_sentence_list.append((animals_in_sentence_set, sentence))


def filter_1_result_query(file_name, animals_set):
    data = [[]]
    per_animals_list = []
    complex_sentence_list = []
    prev_sent = ""
    with open(file_name, "r", encoding="utf8") as file:
        next(file)
        for line in file:
            line = line.lower()
            temp = line.split("\t")
            sentence = temp[16]
            if prev_sent == sentence:
                continue

            check_animal_in_sentence(animals_set, data, per_animals_list, sentence, complex_sentence_list)
            prev_sent = sentence
    data.pop(0)
    return data, per_animals_list, complex_sentence_list


def filter_2_result_query(data, per_animals_list):
    results = []
    bed_result = []
    for sentence, pair in zip(data, per_animals_list):

        if re.search(pair[1] + "[^...]*" + "to" + "[^...]*" + pair[0], sentence) or re.search(
                pair[0] + "[^...]*" + "to" + "[^...]*" + pair[1], sentence):
            results.append((pair, sentence))
        else:
            bed_result.append((pair, sentence))

    return results


def write_to_file(result, complex_sentence_list):
    with open("manually_filter", "w", encoding="utf8") as file:
        for index, line in enumerate(result):
            file.write(str(index) + "|" + str(line[0]) + "|" + str(line[1]))

        file.write("\n----------------complex sentence--------------------------\n\n")

        for index, line in enumerate(complex_sentence_list):
            animals_in_sentence, sentence = line[0], line[1]
            file.write(str(index) + "|(" + ",".join(animals_in_sentence) + ")|" + sentence)


def filter_transmit_query():
    animals_set = arrange_animals_list(animals_list)
    result_after_filter_1, per_animals_list_1, complex_sentence_list = filter_1_result_query(
        "data/transmit_query_results.tsv", animals_set)
    print(result_after_filter_1)
    print(per_animals_list_1)
    result = filter_2_result_query(result_after_filter_1, per_animals_list_1)

    write_to_file(result, complex_sentence_list)


def main():
    filter_transmit_query()


if __name__ == "__main__":
    main()