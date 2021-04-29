# Main
import utils
import model

def entry_analyze_emotions(entry, threshold=0):
    sentences = utils.entry_sentences(entry)
    e = model.query(sentences) 
    return e

    
    
def entry_generate_report(entry):
    emotions_stcs = entry_analyze_emotions(entry)
    emotions_entry = {}
    for stc in emotions_stcs:
        for emotion in stc:
            try:
                emotions_entry[emotion['label']] = (emotion['score'] + emotions_entry[emotion['label']]) / 2
            except KeyError:
                emotions_entry[emotion['label']] = emotion['score']
    body = entry['body']
    return emotions_entry

