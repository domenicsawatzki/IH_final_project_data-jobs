# LinkedIn Web Scraper and Job Recommender

## Description
This project aims to scrape job postings from LinkedIn and provide job recommendations based on the scraped data. It uses various Natural Language Processing (NLP) techniques to process job descriptions and titles, ultimately suggesting jobs that best match a set of skills.

## Project Structure
```
|-- config
|   |-- config.json
|-- data
|-- notebooks
|   |-- NLP_processing_job_description.ipynb
|   |-- NLP_processing_job_title_first_view.ipynb
|   |-- NLP_processing_job_title_transformer.ipynb
|   |-- data_transformer.ipynb
|   |-- linkedin_scraper.ipynb
|   |-- transform_scraped_data.ipynb
|-- pages
|   |-- 02_job_search.py
|   |-- 03_Skills.py
|   |-- 04_Trainer.py
|-- src
|   |-- myModules
|       |-- __init__.py
|       |-- my_NLP.py
|       |-- prep.py
|       |-- scraper_ds.py
|       |-- transformer.py
|-- .gitignore
|-- README.md
|-- app.py
|-- requirements.txt
```

## Setup and Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `pip install -r requirements.txt` to install the required packages.
4. Update the `config.json` file with your LinkedIn credentials and other settings.
5. Run `app.py` to launch the Streamlit application.

## Main Dependencies

- pandas
- numpy
- streamlit
- spacy
- bs4
- requests
- matplotlib
- seaborn

For a full list of dependencies, see `requirements.txt`.
