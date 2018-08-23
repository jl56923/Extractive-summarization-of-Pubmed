import numpy as np
import pickle

from flask import Flask, abort, render_template, jsonify, request

from query_pubmed import get_pmid_list, convert_pmid_list_to_pmcid_list, get_dict_of_converted_papers_from_pmcid_list


def make_summarization(pubmed_query_summarizer_type):

    pubmed_query = pubmed_query_summarizer_type['pubmed_query']
    summarizer_type = pubmed_query_summarizer_type['summarizer_type']

    pmid_list = get_pmid_list(pubmed_query)

    pmcid_list = convert_pmid_list_to_pmcid_list(pmid_list)

    dict_of_converted_papers = get_dict_of_converted_papers_from_pmcid_list(pmcid_list)

    # paper_dict = dict_of_converted_papers[pmcid_list[0]]
    #
    # print(paper_dict['title'])

    # print(jsonify(dict_of_converted_papers).json)

    result = {
        'prediction': pubmed_query,
        'prob_survived': summarizer_type,
        'paper1': 'hello',
        'paper2': 'goodbye'
    }

    result = dict_of_converted_papers

    return result

if __name__ == '__main__':
    print(make_summarization(example))
