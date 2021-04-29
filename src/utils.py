from itertools import chain
import csv
import os
import re
import datetime

#Load entries
def entry_create_object(ugly_entry):

    lines = ugly_entry.split("\n")
    title = re.match('(^# (.*))', ugly_entry)
    # This doesn't work for some reason; Maybe that's why you should learn regex instead of searching how to do a certain pattern everytime
    date = re.search('(Date:) ((\w{3}) (\d{1,2}), (\d{4}))', ugly_entry)
    body = ugly_entry
    if not (bool(title) and bool(date) and bool(body)):
        return
    title = title.group(1)
    date = date.group(2)
    entry_object = {}
    entry_object['title'], entry_object['date'], entry_object['body'] = title, date, body
    return entry_object

def load_entries(directory):
    entries = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename) 

        with open(filepath, 'r') as f:
            text = f.read()
            entry_object = entry_create_object(text)
            if entry_object: entries.append(entry_object)
            else: print(f"Couldn't read {filepath}")
    return entries 

#End load entries

#misc

def mean(l):
    return sum(l)/len(l)

def generic_nth(l, sort_key_func, n):
    return sorted(l, key=sort_key_func, reverse=True)[n]
 
#End misc

#Frequency of words

def entry_wordcount(entry):
    return len(entry['body'].split(' '))

def entries_wordcount(entries):
    wordcounts = []

    for entry in entries:
        wordcount = entry_wordcount(entry) 
        wordcounts.append(wordcount)

    return wordcounts

def entries_nth_most_words(entries, n=0):
    return generic_nth(zip(entries_wordcount(entries), entries), lambda i: i[0], n)

def entries_mean_wordcount(entries):

    a = entries_wordcount(entries)

    return mean(a)

def entries_total_wordcount(entries):
    
    total = sum(entries_wordcount(entries))

    return total

def entries_split_bodies(entries, separator):
    splited = []
    for entry in entries:
        body = entry['body']
        body = body.split(separator)
        splited = splited + body
    return splited


def entries_words(entries):
    words = [] 
    for entry in entries:
        entry_words = re.compile('w+').findall(entry['body'].lower())
        words += entry_words
    return words


def entries_words_set(entries):
    words = entries_words(entries)

    return set(words)

def entries_mean_word_len(entries):
    words = entries_words_set(entries)
    words = list(map(lambda i: len(i), words))

    return mean(words)

def entries_sentences(entries):

    sentences = entries_split_bodies(entries, '.')
    return sentences

def entries_random_sentence(entries):

    sentences = entries_sentences(entries)
    from secrets import choice
    return choice(sentences)

def entries_words_frequencies(entries):

    frequencies = {} 
    all_ocurrences = entries_words(entries)

    for o in all_ocurrences:
        frequencies[o] = frequencies.get(o, 0) + 1 

    return frequencies

def entries_nth_most_frequent_word(entries, n=0):
    return generic_nth(entries_words_frequencies(entries).items(), lambda i: i[1], n)

def field_from_entries(field, entries):
    return [entry[field] for entry in entries]


def entries_search_term(entries, term, field='body', exact=False):

    corpus = field_from_entries(field, entries)
    search_result = {} 
    search_result['result'] = []


    for c in corpus:
        r = re.search(term.lower(), c.lower())
        if r: 
            if field == 'body':
                c_obj = entry_create_object(c)
                search_result['result'].append(c_obj)
            elif field == 'title':
                search_result['result'].append(c)

    search_result['matches'] = len(search_result['result'])
    return search_result

def entry_date_obj(plain_date):
    ''' converts plain text date in format MMM D, YYYY into datetime.date object'''

    def plain_month_number(plain_month):
        if plain_month == 'jan': return 1
        elif plain_month == 'feb': return 2
        elif plain_month == 'mar': return 3
        elif plain_month == 'apr': return 4
        elif plain_month == 'may': return 5
        elif plain_month == 'jun': return 6
        elif plain_month == 'jul': return 7
        elif plain_month == 'aug': return 8
        elif plain_month == 'sep': return 9
        elif plain_month == 'oct': return 10 
        elif plain_month == 'nov': return 11 
        elif plain_month == 'dec': return 12 

    
    plain_date = plain_date.lower()
    plain_date = plain_date.split(' ')
    plain_month = plain_date[0]
    plain_day = plain_date[1].replace(',', '')
    plain_year = plain_date[2]

    month = plain_month_number(plain_month)
    day = int(plain_day)
    year = int(plain_year)


    return datetime.date(year, month, day) 

d = datetime.date
def entries_period(entries, frm, to):
    def filter_by_date(entry, frm, to):
        if entry['date']:
            obj = entry_date_obj(entry['date'])
            return obj >= frm and obj <= to
        return False 
    filtered = filter(lambda i: filter_by_date(i, frm, to), entries) 
    return list(filtered)

def entries_time_since_start(entries):
    sorted_entries = sorted(entries, key=lambda entry: entry_date_obj(entry['date']))

    return entry_date_obj(sorted_entries[-1]['date']) - entry_date_obj(sorted_entries[0]['date'])

def entries_nth_recent(entries, n):
    return generic_nth(entries, lambda entry: entry_date_obj(entry['date']), n)

#TODO instead of doing all this, I could just save in memory the frequency of words from above and access it
def entries_frequency_query(entries, query, exact=False):
    matches = 0
    for entry in entries:
        body = entry['body']
        if not exact: 
            body = body.lower()
        body_matches = body.count(query)
        matches += body_matches
    return matches

#TODO create abstraction for common abstraction between hiatus and streaks;
def entries_streaks(entries):
    current_streak = []
    prev_entry = {} 
    streaks = []
    sorted_entries = sorted(entries, key=lambda entry: entry_date_obj(entry['date'])) 
    for entry in sorted_entries: 
        if prev_entry:
            current_streak.append(prev_entry)
            delta = (entry_date_obj(entry['date']) - entry_date_obj(prev_entry['date'])).days
            if delta > 1 or entry['title'] == sorted_entries[-1]['title']:
                streak_obj = {}
                streak_obj['entries'] = current_streak
                streak_obj['duration'] = (entry_date_obj(current_streak[-1]['date']) - entry_date_obj(current_streak[0]['date'])).days
                streaks.append(streak_obj)
                current_streak = []
                prev_entry = entry
            else:
                prev_entry = entry
            
        else:
            prev_entry = entry
    return streaks

def entries_nth_longest_streak(entries, n=0):
    return generic_nth(entries_streaks(entries), lambda streak: streak['duration'], n)

def entries_hiatuses(entries):
    current_streak = []
    prev_entry = {} 
    hiatuses = []
    streaks = []
    sorted_entries = sorted(entries, key=lambda entry: entry_date_obj(entry['date'])) 
    for entry in sorted_entries: 
        if prev_entry:
            current_streak.append(prev_entry)
            delta = (entry_date_obj(entry['date']) - entry_date_obj(prev_entry['date'])).days
            hiatus_obj = {}
            hiatus_obj['frm'] = prev_entry['date']
            hiatus_obj['to'] = entry['date']
            hiatus_obj['duration'] = delta
            hiatuses.append(hiatus_obj)
            if delta > 1 or entry['title'] == sorted_entries[-1]['title']:
                streak_obj = {}
                streak_obj['entries'] = current_streak
                streak_obj['duration'] = (entry_date_obj(current_streak[-1]['date']) - entry_date_obj(current_streak[0]['date'])).days
                streaks.append(streak_obj)
                current_streak = []
                prev_entry = entry
            else:
                prev_entry = entry
        else:
            prev_entry = entry

    return hiatuses

def entries_nth_longest_hiatus(entries, n=0):
    return generic_nth(entries_hiatuses(entries), lambda streak: streak['duration'], n)


def entries_replace_term_by(entries, term, by):
    new_entries = []
    for entry in entries:
        new_entry = entry.copy()
        new_entry = re.sub(term, by, new_entry['body'])
        new_entries.append(new_entry)

    return new_entries

def entry_sentences(entry):
    paragraphs = [pg for pg in entry['body'].split('\n') if len(pg) > 100]
    sentences = chain.from_iterable(map(lambda pg: pg.split('.'), paragraphs))
    sentences = filter(lambda stc: stc != '', sentences)
    return list(sentences)



from math import floor
def generate_report(entries):
    print("# Your journal report:")
    total_wordcount = entries_total_wordcount(entries)
    today = d.today()
    this_month_wordcount = entries_total_wordcount(entries_period(entries, d(today.year, today.month, 1), today))
    print(f"You've written {total_wordcount} words on total; {this_month_wordcount} words this month alone!") 
    wordcount, entry_longest = entries_nth_most_words(entries) 
    print(f"\"{entry_longest['title']}\" is your longest journal entry with {wordcount} words")
    mean_wordcount = entries_mean_wordcount(entries)
    print(f"You've written {floor(mean_wordcount)} words per entry on average") 
    mean_wordlength = entries_mean_word_len(entries)
    print(f"Your words have {floor(mean_wordlength)} characters on average")
    random_sentence = entries_random_sentence(entries)
    print(f"A random sentence from you: {random_sentence}")
    time_start = entries_time_since_start(entries)
    print(f"There are {time_start.days} days between your first entry and your last")
    hiatus = entries_nth_longest_hiatus(entries)
    print(f"The longest time you've spent without journaling was {hiatus['duration']} days, from {hiatus['frm']} to {hiatus['to']}")
    streak = entries_nth_longest_streak(entries)
    print(f"The longest you've journalled everyday was {streak['duration']} days, from {streak['entries'][0]['date']} to {streak['entries'][-1]['date']}. Keep going!")

