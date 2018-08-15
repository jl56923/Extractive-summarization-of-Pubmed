# Project 4

## Project proposal
The goal of this project is to build a program that can take a query about a topic (e.g. a medical condition or procedure), then search Pubmed/PMC for review papers, and return automatically generated summaries of the most-cited review papers about that topic.

## Domain
The overall domain of this project is medical/scientific literature, and I am familiar enough with reading medical and scientific papers that I would feel comfortable reading the papers that the program would find, and to judge whether or not the code was able to generate a relevant summary of that paper. I would like to be able to review a lot of different review papers, and also possibly to provide links and summaries of landmark trials or scientific breakthroughs that these papers mention.

## Data
The main data source for this project would be Pubmed and Pubmed Central. The NCBI (National Center for Biotechnology Information) which hosts Pubmed and PMC provides 'e-utilities' which are APIs to query the NCBI databases for information, and in Pubmed/PMC you can query for paper abstracts, citations, etc. There is also the open access subset of papers, which I can either use their e-utility to query for the full content of the paper as an XML, or I can actually download the [Open Access subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/) directly using an ftp connection, and then query the articles that I've downloaded already.

## Known unknowns
I'm not sure what would be the best algorithms to use for summarization, or how well auto-summarization will work for on review papers; a lot of review papers have similarly titled sections, e.g. 'history', 'therapies', etc, and I'm not sure what's the best way to take advantage of that similar structure. Also, I'm not sure what will be the best way to get access to review papers; it's probably going to be querying PMC for the full XML, since I am pretty sure that I am going to want to summarize the full paper and not just the abstract. PMC does not have as many papers or review papers as the full pubmed archive, and also pubmed does have more papers that are 'free' if you can click the link to where the full paper is published, but this would involve scraping those outside webpages.

## Minimal viable product
The minimal viable product in this case would be a website that would take in a query, and then spit back an auto-summary of the N (1, 5, 10 etc) most recent open access review papers on the topic.
