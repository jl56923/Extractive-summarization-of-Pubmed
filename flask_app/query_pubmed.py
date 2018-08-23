import numpy as np
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
import pickle

def get_pmid_list(pubmed_query):
    pubmed_query = pubmed_query.replace(" ", "+")

    with open("API_ignore.txt", "r") as f:
        lines = f.read()

    entrez_api_key = lines.split(":")[1].strip()

    esearch_base_query = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"

    review_pmids_query_dict = {
        "db": "pubmed",
        "sort": "relevance",
        "retmax": '10',
        "term": '{}+AND+(Review[ptyp]+OR+systematic[sb])+AND+free+full+text[sb]+AND+"last%205%20years"[PDat]',
        "api_key": entrez_api_key
    }

    joined_terms = [k+"="+v for k, v in review_pmids_query_dict.items()]

    get_review_pmids_query = esearch_base_query + "&".join(joined_terms)

    r = requests.get(get_review_pmids_query.format(pubmed_query, entrez_api_key))

    tree = ET.ElementTree(ET.fromstring(r.content))
    root = tree.getroot()

    pmids = root.findall('.//Id')
    pmid_list = [pmid.text for pmid in pmids]

    return pmid_list

#########################

def convert_pmid_list_to_pmcid_list(pmid_list):
    pmcid_list = []

    convert_PMID_query = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?tool=review_assistant&email=jl56923@gmail.com&ids={}&format=json"

    for pmid in pmid_list:
        r = requests.get(convert_PMID_query.format(pmid))
        result = r.json()
        records_dict = result['records'][0]

        # If there is an error message in the records dictionary that gets returned with the result, then this
        # paper does not have a PMCID and we are not going to be able to get the full text of this paper.
        if 'errmsg' in records_dict:
            pass
        else:
            if 'pmcid' in records_dict:
                pmcid_list.append(records_dict['pmcid'])

    return pmcid_list

#########################

# The next two functions, get_paragraphs_as_clean_string and get_article_text_exclude_after_conclusion are two
# helper functions which help clean up the contents of the XML of the paper that gets fetched from PMC.
# These two helper functions are both used by get_list_of_dictionaries_from_pmcid_list.

def get_paragraphs_as_clean_string(xml_node):
    # first, we'll clear all the children elements of the table-wrap tags,
    # which will get rid of all the content that was in the tables.
    # But, first check to see if the table even has tables, because if there is no table-wrap tag
    # then you don't need to do anything.
    if not xml_node:
        return ""

    if xml_node.find(".//table-wrap"):
        for table in xml_node.findall(".//table-wrap"):
            table.clear()

    node_paragraphs = xml_node.findall(".//p")

    clean_string = ""

    for paragraph in node_paragraphs:
        clean_string += " ".join(paragraph.itertext())
        clean_string += " "

    clean_string = clean_string.strip()

    # We'll get rid of anything inside of square brackets, since those tend to be the citations.
    clean_string = re.sub(r'\[.*?]', "", clean_string)
    clean_string = re.sub(r'(\s)+', " ", clean_string)

    return clean_string

def get_article_text_exclude_after_conclusion(body_node):
    sections = body_node.findall(".//sec")

    conclusion_index = len(sections)

    for index, section in enumerate(sections):
        section_title = section.find(".//title")
        if section_title:
            if section_title.text:
                if "conclusion" in section_title.text.lower():
                    conclusion_index = index
                    break
                if "discussion" in section_title.text.lower():
                    conclusion_index = index
                    break

    article_text = ""

    for section in sections[:conclusion_index]:
        article_text += get_paragraphs_as_clean_string(section)

    return article_text

# This function takes a list of PMCIDs, and uses the eutils efetch function to get the raw XML for each
# paper from PMC. It extracts the title, PMCID, keywords, abstract, article, and citations and stores them
# in a dictionary for each paper in the list. It then returns a list of dictionaries for the papers.

# Not all papers that have PMCIDs will allow fetching the raw XML for the entire paper, and so we check
# for that and skip those papers.

def get_dict_of_converted_papers_from_pmcid_list(pmcid_list):

    get_pmc_xml_query = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={}&tool=review_assistant&email=jl56923@gmail.com"

    dict_of_converted_papers = {}

    for i in range(len(pmcid_list)):

        r = requests.get(get_pmc_xml_query.format(pmcid_list[i]))

        tree = ET.ElementTree(ET.fromstring(r.content))
        root = tree.getroot()

        # Check to see if you can even get the XML from PMC; if not, then pass. If you can, then you can go ahead
        # and continue making the dictionary and pickling it.
        body = root.find(".//body")
        if body:
            article_text = get_article_text_exclude_after_conclusion(body)
        else:
            print(f"Unable to get text for {pmcid_list[i]}.")
            continue

        pmcid = pmcid_list[i]

        # We'll find the first article-title in the text, which should be the title of the paper.
        title = root.find(".//article-title").text

        keyword_elements = root.findall(".//kwd")

        if keyword_elements:
            keywords = [keyword.text.lower() for keyword in keyword_elements if keyword.text]
        else:
            keywords = []

        abstract = root.find(".//abstract")
        abstract_text = get_paragraphs_as_clean_string(abstract)

        citations = root.findall(".//pub-id")
        citation_tuples = [(citation.text, list(citation.attrib.values())[0]) for citation in citations]

        paper_dict = {
            "title": title,
            "keywords": keywords,
            "abstract_text": abstract_text,
            "article_text": article_text,
            "citation_tuples": citation_tuples
        }

        dict_of_converted_papers[pmcid] = paper_dict

    return dict_of_converted_papers
