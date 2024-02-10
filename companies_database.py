import global_variables

import pandas as pd

def load_excel_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        companies_df = pd.read_excel(xls, 'Companies (ALL)')
        careers_df = pd.read_excel(xls, 'Careers Pages')
        return companies_df, careers_df
    except Exception as e:
        print("An error occurred while loading the Excel file:", e)
        return None, None

def filter_companies(companies_df, tags=None, industry=None, location=None):
    try:
        filtered_df = companies_df.copy()
        if tags:
            # AND operator search
            filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: all(tag in x.split() for tag in tags))]
            # OR operator search
            #filtered_df = filtered_df[filtered_df['Tags'].apply(lambda x: any(tag in x.split() for tag in tags))]
        if industry:
            filtered_df = filtered_df[filtered_df['Industry'] == industry]
        if location:
            filtered_df = filtered_df[filtered_df['Location'] == location]
        return filtered_df
    except Exception as e:
        print("An error occurred while filtering companies:", e)
        return pd.DataFrame()

def match_careers_pages(careers_df, filtered_companies=None):
    try:
        if filtered_companies is not None:
            matched_df = pd.merge(filtered_companies, careers_df, on='Website URL', how='inner')
        else:
            matched_df = careers_df.copy()
        return matched_df['Careers URL'].tolist()
    except Exception as e:
        print("An error occurred while matching companies with careers pages:", e)
        return []

def search_careers_pages(file_path, tags=None, industry=None, location=None):
    try:
        companies_df, careers_df = load_excel_data(file_path)
        if companies_df is None or careers_df is None:
            return []

        filtered_companies = filter_companies(companies_df, tags, industry, location)

        # Check if there are any filtered companies left after filtering
        if filtered_companies.empty:
            return []

        urls = match_careers_pages(careers_df, filtered_companies)

        return urls
    except Exception as e:
        print("An unexpected error occurred:", e)
        return []
