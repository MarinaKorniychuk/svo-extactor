import spacy
import textacy.extract


class SVOExtractor(object):
    def __init__(self):
        super().__init__()
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe(self.nlp.create_pipe("sentencizer"), first=True)

    def process(self, data):
        svo_triples = sum((self.process_item(item) for item in data), [])

        return svo_triples

    def process_item(self, item):
        text = self.nlp(
            "".join([sent.string for sent in self.nlp(item["text"]).sents][:2])
        )

        svo_triples = []
        for svo in textacy.extract.subject_verb_object_triples(text):
            svo_triples.append(
                {
                    "page": item["page_title"],
                    "subject": svo[0].lemma_,
                    "verb": svo[1].lemma_,
                    "object": svo[2].lemma_,
                    "url": item["page_url"],
                }
            )

        return svo_triples
