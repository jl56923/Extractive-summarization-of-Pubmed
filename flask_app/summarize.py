import sumy

#Plain text parsers since we are parsing through text
from sumy.parsers.plaintext import PlaintextParser

#for tokenization and stemming
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer

from sumy.utils import get_stop_words

from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer

def get_summaries_from_list_of_abstracts(list_of_abstracts, summarizer_type):

    if summarizer_type == 'lsa':
        summarizer = LsaSummarizer(Stemmer("english"))
    elif summarizer_type == 'luhn':
        summarizer = LuhnSummarizer(Stemmer("english"))
    elif summarizer_type == 'lexrank':
        summarizer = LexRankSummarizer(Stemmer("english"))
    elif summarizer_type == 'textrank':
        summarizer = TextRankSummarizer(Stemmer("english"))

    summarizer.stop_words = get_stop_words("english")

    list_of_summaries = []

    for abstract in list_of_abstracts:
        parser = PlaintextParser(abstract, Tokenizer("english"))
        summary = summarizer(parser.document, 3)
        summary_string = " ".join(map(str, summary))
        list_of_summaries.append(summary_string)

    print(list_of_summaries)

    return list_of_summaries
