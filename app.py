import flask
from flask import request, jsonify
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
import en_core_web_sm
from flask_cors import CORS, cross_origin
import youtube_transcript_api
from youtube_transcript_api import YouTubeTranscriptApi

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Youtube Video Summariser</h1>
<p>A prototype API for my mini project</p>'''



@app.route('/api', methods=['GET'])
def api_id():
    if 'url' in request.args:
        url = str(request.args['url'])
        nlp = en_core_web_sm.load()
        unique_id = url.split("=")[-1]
        sub = YouTubeTranscriptApi.get_transcript(unique_id)  
        subtitle = " ".join([x['text'] for x in sub])

        subtitle = " ".join(subtitle.split())   

        doc = nlp(subtitle)
        len(list(doc.sents))

        keyword = []
        stopwords = list(STOP_WORDS)
        pos_tag = ['PROPN','ADJ','NOUN','VERB']
        for token in doc:
            if(token.text in stopwords or token.text in punctuation):
                continue
            if(token.pos_ in pos_tag):
                keyword.append(token.lemma_)

        freq_word = Counter(set(keyword))
        freq_word.most_common(4)

        max_freq = Counter(keyword).most_common(1)[0][1]
        for word in freq_word.keys():
            freq_word[word] = (freq_word[word]/max_freq)
        freq_word.most_common(4)

        sent_strength = {}
        for sent in doc.sents:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent] += freq_word[word.text]
                    else:
                        sent_strength[sent] = freq_word[word.text]

        top_sentences=(sorted(sent_strength.values())[::-1])
        top_percent_sentence = int(0.1*len(top_sentences))
        top_sent = top_sentences[:top_percent_sentence]

        summary=[]
        for sent,strength in sent_strength.items():
                if strength in top_sent:
                    summary.append(sent)
                else:
                    continue

        summarised = ''.join(map(str,summary))
        result = {
            "Message" : summarised,
	    "Transcripts" : subtitle,
            #"METHOD" : GET
        }
        return jsonify(result)
    else:
        result = {
            "Message" : "Error"
            #"METHOD" : GET
        }
        return jsonify(result)

if __name__ == "__main__":
    app.run()