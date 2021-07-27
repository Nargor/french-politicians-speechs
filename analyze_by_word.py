import gzip
import json

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm = lambda x: x
    print_progess = print
else:
    print_progess = lambda x: x


speechs = gzip.open("data/speechs_normalized.rows_json.gz").readlines()
speechs_count = len(speechs)

results = {
    "merite": {},
    "meritocratie": {},
    "meritocratique": {},
}

for speech_k, speech in enumerate(tqdm(speechs)):

    speech = json.loads(speech)

    if speech_k % 1000 == 0:
        print_progess(f"{speech_k}/{speechs_count}")

    words = speech["text_normalized"].split(" ")
    for word_k, word in enumerate(words):
        if len(word) > 3:

            year = speech["datetime"].split("-")[0]

            for results_word in results.keys():
                if not results[results_word].get(year):
                    results[results_word][year] = [0, 0]

                results[results_word][year][1] += 1

            if word in results.keys():
                results[word][year][0] += 1


print("\n" * 2)
print("Word;Year;Percentage;Word_occurrence;Word_count")
for word, results in results.items():
    print()
    for year, d in sorted(results.items()):
        percentage = d[0] / d[1] * 100
        word_occurrence = d[0]
        word_count = d[1]

        print(f"{word};{year};{percentage:.4f};{word_occurrence};{word_count}")
