import numpy as np
import pickle

from flask import Flask, abort, render_template, jsonify, request

from query_pubmed import get_pmid_list, convert_pmid_list_to_pmcid_list, get_dict_of_converted_papers_from_pmcid_list
from summarize import get_summaries_from_list_of_abstracts


def make_abstracts(features):

    pubmed_query = features['pubmed_query']

    pmid_list = get_pmid_list(pubmed_query)
    pmcid_list = convert_pmid_list_to_pmcid_list(pmid_list)

    dict_of_converted_papers = get_dict_of_converted_papers_from_pmcid_list(pmcid_list)
    result = dict_of_converted_papers

    return result

def make_summaries(features):

    summarizer_type = features['summarizer_type']

    list_of_abstracts = features['list_of_abstracts']

    list_of_summaries = get_summaries_from_list_of_abstracts(list_of_abstracts, summarizer_type)

    result = list_of_summaries

    return result

if __name__ == '__main__':
    print(make_summarization(example))
