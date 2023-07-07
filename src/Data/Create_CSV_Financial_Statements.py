import pandas as pd
import psycopg2 as ps

def financial_statement_view_csv():
    # Connect to database
    ############################################################
    try:
        conn = ps.connect('''

            host=localhost
            dbname=financialdb
            user=postgres
            password=iEchu133

        ''')

        cur = conn.cursor()

        print('Successfully connected to financialdb')

    except ps.Error as e:
        print('\n Database Error:')
        print(e)
    
    # financial_statement_view
    ############################################################
    try:
        # Query financial_statement_view
        query = '''

            SELECT *
            FROM financial_statement_view;

        '''

        cur.execute(query)
        financial_statement_view_df = cur.fetchall()

        financial_statement_view_columns = [
            'cik',
            'company',
            'ticker',
            'financial_accounts',
            'financial_statement',
            'date',
            'filling_date',
            'accepted_date',
            'calendar_year',
            'financial_values'
        ]


        # Convert view to pandas data frame
        financial_statement_view_df = pd.DataFrame(financial_statement_view_df, columns = financial_statement_view_columns)
        
        print('Financial_Statement.csv created')

    except Exception as e:
        print('CSV error:')
        print(e)
        
    # Export data
    financial_statement_view_df.to_csv(
        'Financial_Statement.csv', 
        index = False, 
        encoding = 'utf8'
    )

    
if __name__ == '__main__':
    financial_statement_view_csv()
    
    