from dash import html, dash_table, Input, Output
from App import app
import pandas as pd
from datetime import date


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

layout = html.Div([
    
    # Table header
    html.Div([

        html.H2(
            'Financial Ratios',
            style = {
                'padding':10,
                'padding-top':10,
                'margin-top':50,
                'font-family':'Arial, Helvetica, sans-serif',
                # 'background':'#00008B',
                # 'color':'#FFFFFF',
                'textAlign':'left'
            }
        ),
        
        html.Div(id = 'ratios')
    ]),
])

######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################

# Pull 
#####################################################
@app.callback(
    Output('ratios','children'),
    Input('filtered_data', 'data')
)

def ratios(jsonified_cleaned_data):
    # Get filtered data
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    
    try:
        # Balance Sheet
        #####################################################################################

        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Balance Sheet')]

        table = table[[
            'financial_accounts',
            'calendar_year',
            'financial_values'
        ]]

        table['calendar_year'] = table['calendar_year'].astype(str)

        # Pivot table
        table = table.pivot(
            index = 'financial_accounts', 
            columns = 'calendar_year',
            values = 'financial_values'
        )

        # Rename columns to remove multi-index column names
        table = table.reset_index()
        table = table.rename(columns = {'financial_accounts': 'Account'})

        # Reset index
        table = table.set_index(['Account'])

        # Reindex rows
        table = table.reindex([
            'Cash And Cash Equivalents',
            'Short Term Investments',
            'Cash And Short Term Investments',
            'Net Receivables',
            'Inventory',
            'Other Current Assets',
            'Total Current Assets',
            '',
            'Property Plant Equipment Net',
            'Goodwill',
            'Intangible Assets',
            'Goodwill And Intangible Assets',
            'Long Term Investments',
            'Tax Assets',
            'Other Non Current Assets',
            'Total Non Current Assets',
            'Other Assets',
            'Total Assets',
            '',
            'Account Payables',
            'Short Term Debt',
            'Tax Payables',
            'Deferred Revenue',
            'Other Current Liabilities',
            'Total Current Liabilities',
            '',
            'Long Term Debt',
            'Deferred Revenue Non Current',
            'Deferred Tax Liabilities Non Current',
            'Other Non Current Liabilities',
            'Total Non Current Liabilities',
            'Other Liabilities',
            'Capital Lease Obligations',
            'Total Liabilities',
            '',
            'Preferred Stock',
            'Common Stock',
            'Retained Earnings',
            'Accumulated Other Comprehensive Income Loss',
            'Othertotal Stockholders Equity',
            'Total Stockholders Equity',
            'Total Liabilities And Stockholders Equity',
            'Minority Interest',
            'Total Equity',
            'Total Liabilities And Total Equity',
            'Total Investments',
            'Total Debt',
            'Net Debt'
        ])

        balance_table = table.fillna('').reset_index()


        # Income Statement
        #####################################################################################

        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Income Statement')]

        table = table[[
            'financial_accounts',
            'calendar_year',
            'financial_values'
        ]]

        table['calendar_year'] = table['calendar_year'].astype(str)

        # Pivot table
        table = table.pivot(
            index = 'financial_accounts', 
            columns = 'calendar_year',
            values = 'financial_values'
        )

        # Rename columns to remove multi-index column names
        table = table.reset_index()
        table = table.rename(columns = {'financial_accounts': 'Account'})

        # Reset index
        table = table.set_index(['Account'])

        # Reindex rows
        table = table.reindex([
            'Revenue',
            'Cost Of Revenue',
            'Gross Profit',
            'Gross Profit Ratio',
            '',
            'Research And Development Expenses',
            'General And Administrative Expenses',
            'Selling And Marketing Expenses',
            'Selling General And Administrative Expenses',
            'Other Expenses',
            'Operating Expenses',
            'Cost And Expenses',
            'Operating Income',
            'Operating Income Ratio',
            '',
            'Interest Income',
            'Interest Expense',
            'Depreciation And Amortization',
            'Ebitda',
            'Ebitdaratio',
            'Total Other Income Expenses Net',
            'Income Before Tax',
            'Income Before Tax Ratio',
            'Income Tax Expense',
            '',
            'Net Income',
            'Net Income Ratio',
            'Eps',
            'Epsdiluted',
            'Weighted Average Shs Out',
            'Weighted Average Shs Out Dil'
        ])

        income_table = table.fillna('').reset_index()


        # Cash-Flow Statement
        #####################################################################################

        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Cash-Flow Statement')]

        table = table[[
            'financial_accounts',
            'calendar_year',
            'financial_values'
        ]]

        table['calendar_year'] = table['calendar_year'].astype(str)

        # Pivot table
        table = table.pivot(
            index = 'financial_accounts', 
            columns = 'calendar_year',
            values = 'financial_values'
        )

        # Rename columns to remove multi-index column names
        table = table.reset_index()
        table = table.rename(columns = {'financial_accounts': 'Account'})

        # Reset index
        table = table.set_index(['Account'])

        # Reindex rows
        table = table.reindex([
            'Net Income',
            'Depreciation And Amortization',
            'Deferred Income Tax',
            'Stock Based Compensation',
            'Change In Working Capital',
            'Accounts Receivables',
            'Inventory',
            'Accounts Payables',
            'Other Working Capital',
            'Other Non Cash Items',
            'Net Cash Provided By Operating Activities',
            '',
            'Investments In Property Plant And Equipment',
            'Acquisitions Net',
            'Purchases Of Investments',
            'Sales Maturities Of Investments',
            'Other Investing Activites',
            'Net Cash Used For Investing Activites',
            '',
            'Debt Repayment',
            'Common Stock Issued',
            'Common Stock Repurchased',
            'Dividends Paid',
            'Other Financing Activites',
            'Net Cash Used Provided By Financing Activities',
            '',
            'Effect Of Forex Changes On Cash',
            'Net Change In Cash',
            'Cash At End Of Period',
            'Cash At Beginning Of Period',
            'Operating Cash Flow',
            'Capital Expenditure',
            'Free Cash Flow'
        ])

        cash_table = table.fillna('').reset_index()


        # Income
        #####################################################################################
        income = income_table.loc[income_table['Account'] == 'Net Income']

        income = income.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        income_list = income[25].tolist()[1:]


        # AVG Equity
        #####################################################################################
        avg_equity = balance_table.loc[balance_table['Account'] == 'Total Stockholders Equity']

        avg_equity = avg_equity.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_equity = avg_equity.rolling(2).mean().dropna()
        avg_equity_list = avg_equity[40].tolist()


        # Equity
        #####################################################################################
        equity = balance_table.loc[balance_table['Account'] == 'Total Stockholders Equity']

        equity = equity.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        equity_list = equity[40].tolist()[1:]


        # EBIT
        #####################################################################################
        ebit = income_table.loc[
            (income_table['Account'] == 'Revenue') | 
            (income_table['Account'] == 'Cost And Expenses')
             ]

        ebit = ebit.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        ebit['ebit'] = ebit[0] - ebit[11]
        ebit_list = ebit['ebit'].tolist()[1:]


        # AVG Total Assets
        #####################################################################################
        avg_t_assets = balance_table.loc[balance_table['Account'] == 'Total Assets']

        avg_t_assets = avg_t_assets.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_t_assets = avg_t_assets.rolling(2).mean().dropna()
        avg_t_assets_list = avg_t_assets[17].tolist()


        # Total Assets
        #####################################################################################
        t_assets = balance_table.loc[balance_table['Account'] == 'Total Assets']

        t_assets = t_assets.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        t_assets_list = t_assets[17].tolist()


        # Revenue
        #####################################################################################
        revenue = income_table.loc[
            (income_table['Account'] == 'Revenue')
             ]

        revenue = revenue.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        revenue_list = revenue[0].tolist()[1:]


        # Gross Profit
        #####################################################################################
        gross_profit = income_table.loc[
            (income_table['Account'] == 'Gross Profit')
             ]

        gross_profit = gross_profit.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        gross_profit_list = gross_profit[2].tolist()[1:]


        # Operating Income
        #####################################################################################
        operating_income = income_table.loc[
            (income_table['Account'] == 'Operating Income')
             ]

        operating_income = operating_income.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        operating_income_list = operating_income[12].tolist()[1:]


        # Selling General And Administrative Expenses
        #####################################################################################
        selling_gen_admin_exp = income_table.loc[
            (income_table['Account'] == 'Selling General And Administrative Expenses')
             ]

        selling_gen_admin_exp = selling_gen_admin_exp.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        selling_gen_admin_exp_list = selling_gen_admin_exp[8].tolist()[1:]


        # Interest Expense
        #####################################################################################
        interest_expense = income_table.loc[
            (income_table['Account'] == 'Interest Expense')
             ]

        interest_expense = interest_expense.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        interest_expense_list = interest_expense[16].tolist()[1:]


        # Tax Expense
        #####################################################################################
        tax_expense = income_table.loc[
            (income_table['Account'] == 'Income Tax Expense')
             ]

        tax_expense = tax_expense.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        tax_expense_list = tax_expense[23].tolist()[1:]


        # AVG Accounts Recievable 
        #####################################################################################
        avg_net_recievables = balance_table.loc[
            (balance_table['Account'] == 'Net Receivables')
             ]

        avg_net_recievables = avg_net_recievables.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_net_recievables = avg_net_recievables.rolling(2).mean().dropna()
        avg_net_recievables_list = avg_net_recievables[3].tolist()


        # AVG Accounts Recievable 
        #####################################################################################
        net_recievables = balance_table.loc[
            (balance_table['Account'] == 'Net Receivables')
             ]

        net_recievables = net_recievables.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        net_recievables_list = net_recievables[3].tolist()


        # Cost Of Revenue
        #####################################################################################
        cost_of_rev = income_table.loc[
            (income_table['Account'] == 'Cost Of Revenue')
             ]

        cost_of_rev = cost_of_rev.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        cost_of_rev_list = cost_of_rev[1].tolist()[1:]


        # AVG Inventory
        #####################################################################################
        avg_inventory = balance_table.loc[
            (balance_table['Account'] == 'Inventory')
             ]

        avg_inventory = avg_inventory.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_inventory = avg_inventory.rolling(2).mean().dropna()
        avg_inventory_list = avg_inventory[4].tolist()


        # Payable
        #####################################################################################
        payable = balance_table.loc[
            (balance_table['Account'] == 'Account Payables')
             ]

        payable = payable.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        payable_list = payable[19].tolist()[1:]


        # AVG PPE
        #####################################################################################
        avg_ppe = balance_table.loc[
            (balance_table['Account'] == 'Property Plant Equipment Net')
             ]

        avg_ppe = avg_ppe.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_ppe = avg_ppe.rolling(2).mean().dropna()
        avg_ppe_list = avg_ppe[8].tolist()


        # Total Current Assets
        #####################################################################################
        t_current_assets = balance_table.loc[
            (balance_table['Account'] == 'Total Current Assets')
             ]

        t_current_assets = t_current_assets.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        t_current_assets_list = t_current_assets[6].tolist()[1:]


        # Cash and Equivalents
        #####################################################################################
        cash_equivalents = balance_table.loc[
            (balance_table['Account'] == 'Cash And Cash Equivalents')
             ]

        cash_equivalents = cash_equivalents.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        cash_equivalents_list = cash_equivalents[0].tolist()[1:]


        # Total Current Liabilities
        #####################################################################################
        t_current_liabilities = balance_table.loc[
            (balance_table['Account'] == 'Total Current Liabilities')
             ]

        t_current_liabilities = t_current_liabilities.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        t_current_liabilities_list = t_current_liabilities[24].tolist()[1:]


        # AVG Total Current Liabilities
        #####################################################################################
        avg_t_current_liabilities = balance_table.loc[
            (balance_table['Account'] == 'Total Current Liabilities')
             ]

        avg_t_current_liabilities = avg_t_current_liabilities.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_t_current_liabilities = avg_t_current_liabilities.rolling(2).mean().dropna()
        avg_t_current_liabilities_list = avg_t_current_liabilities[24].tolist()


        # Net Cash from Operations
        #####################################################################################
        net_cash_operations = cash_table.loc[
            (cash_table['Account'] == 'Net Cash Provided By Operating Activities')
             ]

        net_cash_operations = net_cash_operations.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        net_cash_operations_list = net_cash_operations[10].tolist()[1:]


        # Toal Liabilities
        #####################################################################################
        total_liabilities = balance_table.loc[
            (balance_table['Account'] == 'Total Liabilities')
             ]

        total_liabilities = total_liabilities.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        total_liabilities_list = total_liabilities[33].tolist()[1:]


        # Intangible Assets
        #####################################################################################
        intangible_assets = balance_table.loc[
            (balance_table['Account'] == 'Goodwill And Intangible Assets')
             ]

        intangible_assets = intangible_assets.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        intangible_assets_list = intangible_assets[11].tolist()[1:]


        # AVG Intangible Assets
        #####################################################################################
        avg_intangible_assets = balance_table.loc[
            (balance_table['Account'] == 'Goodwill And Intangible Assets')
             ]

        avg_intangible_assets = avg_intangible_assets.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_intangible_assets = avg_intangible_assets.rolling(2).mean().dropna()
        avg_intangible_assets_list = avg_intangible_assets[11].tolist()


        # Long-Term Debt
        #####################################################################################
        long_term_debt = balance_table.loc[
            (balance_table['Account'] == 'Long Term Debt')
             ]

        long_term_debt = long_term_debt.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        long_term_debt_list = long_term_debt[26].tolist()[1:]


        # Avg Long-Term Debt
        #####################################################################################
        avg_long_debt = balance_table.loc[balance_table['Account'] == 'Long Term Debt']

        avg_long_debt = avg_long_debt.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        avg_long_debt = avg_long_debt.rolling(2).mean().dropna()
        avg_long_debt_list = avg_long_debt[26].tolist()


        # Inventory Begining
        #####################################################################################
        beginning_inventory = balance_table.loc[balance_table['Account'] == 'Inventory']

        beginning_inventory = beginning_inventory.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        beginning_inventory_list = beginning_inventory[4].tolist()[0:-1]


        # Inventory End
        #####################################################################################
        end_inventory = balance_table.loc[balance_table['Account'] == 'Inventory']

        end_inventory = end_inventory.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        end_inventory_list = end_inventory[4].tolist()[1:]


        # Depreciation and Amortization
        #####################################################################################
        depreciation_amortization = income_table.loc[income_table['Account'] == 'Depreciation And Amortization']

        depreciation_amortization = depreciation_amortization.drop(
            ['Account'], 
            axis = 1, 
            errors = 'ignore'
        ).T

        depreciation_amortization_list = depreciation_amortization[17].tolist()


        # Ratios table
        #####################################################################################

        ratio_list = []
        for (
            avg_equity, income, ebit, avg_t_assets, 
            revenue, cost_of_rev, selling_gen_admin_exp,
            operating_income, interest_expense, tax_expense,
            avg_net_recievables, avg_inventory, avg_ppe, 
            t_current_assets, t_current_liabilities,
            avg_t_current_liabilities, net_cash_operations,
            cash_equivalents, net_recievables, total_liabilities,
            equity, long_term_debt, t_assets, intangible_assets,
            avg_long_debt, depreciation_amortization, avg_intangible_assets,
            beginning_inventory, end_inventory

            ) in zip(
            avg_equity_list, income_list, ebit_list, avg_t_assets_list, 
            revenue_list, cost_of_rev_list, selling_gen_admin_exp_list,
            operating_income_list, interest_expense_list, tax_expense_list,
            avg_net_recievables_list, avg_inventory_list, avg_ppe_list,
            t_current_assets_list, t_current_liabilities_list,
            avg_t_current_liabilities_list, net_cash_operations_list,
            cash_equivalents_list, net_recievables_list, total_liabilities_list,
            equity_list, long_term_debt_list, t_assets_list, intangible_assets_list,
            avg_long_debt_list, depreciation_amortization_list, avg_intangible_assets_list,
            beginning_inventory_list, end_inventory_list
        ):

            purchase = end_inventory + cost_of_rev - beginning_inventory

            try:
                days_receivable = round(365 * (avg_net_recievables / revenue), 2)
            except:
                days_receivable = 0.0

            try:
                days_inventory = round(365 * (avg_inventory / cost_of_rev), 2)
            except:
                 days_inventory = 0.0

            try:
                days_payable = round(365 * (avg_net_recievables / purchase), 2)
            except:
                days_payable = 0.0

            try:
                roe =  round(income / avg_equity, 2),
            except:
                roe = 0.0,

            try:
                roa =  round(ebit / avg_t_assets, 2),
            except:
                roa = 0.0,       

            try:
                financial_leverage = round(avg_t_assets / avg_equity, 2),
            except:
                financial_leverage = 0.0, 

            try:
                correction_factor = round(income / ebit, 2),
            except:
                correction_factor = 0.0, 

            try:
                ros = round(ebit / revenue, 2),
            except:
                ros = 0.0, 

            try:
                ros = round(ebit / revenue, 2),
            except:
                ros = 0.0,

            try:
                asset_turnover = round(revenue / avg_t_assets, 2),
            except:
                asset_turnover = 0.0,  

            try:
                gross_margin = round((revenue - cost_of_rev) / revenue, 2),
            except:
                gross_margin = 0.0, 

            try:
                sgas = round(selling_gen_admin_exp / revenue, 2),
            except:
                sgas = 0.0, 

            try:
                operating_margin = round(operating_income / revenue, 2),
            except:
                operating_margin = 0.0, 

            try:
                interest_expense = round(interest_expense / revenue, 2),
            except:
                interest_expense = 0.0, 

            try:
                tax_rate = round(tax_expense / ebit, 2),
            except:
                tax_rate = 0.0, 

            try:
                acc_rec_turnover = round(revenue / avg_net_recievables, 2),
            except:
                acc_rec_turnover = 0.0, 

            try:
                inventory_turnover =  round(cost_of_rev / avg_inventory, 2),
            except:
                inventory_turnover = 0.0, 

            try:
                acc_pay_turnover =  round(purchase / avg_net_recievables, 2),
            except:
                acc_pay_turnover = 0.0, 

            try:
                fix_asset_turnover =  round(revenue / avg_ppe, 2),
            except:
                fix_asset_turnover = 0.0, 

            try:
                current_ratio =  round(t_current_assets / t_current_liabilities, 2),
            except:
                current_ratio = 0.0, 

            try:
                quick_ratio =  round((cash_equivalents + net_recievables) / t_current_liabilities, 2),
            except:
                quick_ratio = 0.0, 

            try:
                cfo_cur_lib =  round(net_cash_operations / avg_t_current_liabilities, 2),
            except:
                cfo_cur_lib = 0.0, 

            try:
                interest_coverage =  round(ebit / interest_expense, 2),
            except:
                interest_coverage = 0.0, 

            try:
                debt_to_equity =  round(total_liabilities / equity, 2),
            except:
                debt_to_equity = 0.0,

            try:
                long_debt_to_equity =  round(long_term_debt / equity, 2),
            except:
                long_debt_to_equity = 0.0,

            try:
                long_debt_tan_assets =  round(long_term_debt / (t_assets - intangible_assets), 2),
            except:
                long_debt_tan_assets = 0.0,

            try:
                weight_avg_interest_rate =   round(interest_expense / avg_long_debt, 2),
            except:
                weight_avg_interest_rate = 0.0,

            try:
                weight_avg_dep_rate =   round(depreciation_amortization / (avg_ppe + avg_intangible_assets), 2),
            except:
                weight_avg_dep_rate = 0.0,

            ratio_dict = {
                "":"",
                "Return on Equity:": "",
                "Return on Equity = Net Income / Avg. Stockholders' Equity": roe,
                "Return on Assets = De-levered Net Income / Avg. Total Assets": roa,
                "Financial Leverage = Avg. Total Assets / Avg. Stockholders’ Equity": financial_leverage,
                "Correction Factor = Net Income / De-levered Net Income": correction_factor,
                " ":"",
                "Return on Assets:": "",
                "Return on Sales =  De-levered Net Income / Sales": ros,
                "Asset turnover = Sales / Avg. Total Assets": asset_turnover,
                "  ":"",
                "Profitability:": "",
                "Gross Margin = (Sales - Cost of Goods Sold) / Sales": gross_margin,
                "SG&A as a % of Sales = SG&A Expense / Sales": sgas,
                "Operating Margin = Operating Income / Sales": operating_margin,
                "Interest Expense as % of Sales = Interest Expense / Sales": interest_expense,
                "Effective Tax Rate = Income Taxes / Pre-tax Income": tax_rate,    
                "   ":"",
                "Asset Turnover Ratios:": "",
                "Accounts Receivables Turnover = Sales / Avg. Accounts Receivable": acc_rec_turnover,         
                "Inventory Turnover = Cost of Goods Sold / Avg. Inventory": inventory_turnover,          
                "Accounts Payable Turnover = Purchases / Avg. Accounts Payable": acc_pay_turnover,          
                "Fixed Asset Turnover = Sales / Avg. Net Property, Plant and Equipment": fix_asset_turnover,  
                "    ":"",
                "Days Turnover Ratios:": "",
                "Days Receivables =  365 * (Avg. Accounts Receivable / Sales)": days_receivable,                    
                "Days Inventory = 365 * (Avg. Inventory / Cost of Goods Sold)": days_inventory,
                "Days Payable = 365 * (Avg. Accounts Payable / Purchases)": days_payable,
                "Net Trade Cycle = Days Receivable + Days Inventory - Days Payable": round(days_receivable + days_inventory - days_payable, 2),
                "     ":"",
                "Liquidity Analysis:": "",
                "Current Ratio = Current Assets / Current Liabilities": current_ratio,         
                "Quick Ratio = (Cash + Accts Rec) / Current Liabilities": quick_ratio,         
                "CFO-to-Current Liabilities = Cash from Operations / Avg. Current Laibilities": cfo_cur_lib,     
                "     ":"",
                "Interest Coverage = Operating Income before Depreciation / Interest Expense": interest_coverage,
                "       ":"",
                "Debt to Equity = Total Liabilities / Total Stockholders’ Equity": debt_to_equity,         
                "Long-Term-Debt to Equity = Total Long-Term Debt / Total Stockholders’ Equity": long_debt_to_equity,          
                "Long-Term Debt to Tangible Assets = Total Long-Term Debt / (Total Assets - Intangible Assets)": long_debt_tan_assets,
                "        ":"",
                "Other Information:": "",
                "Weighted Avg Interest Rate = Interest Expense / Avg. Long-Term Debt": weight_avg_interest_rate,         
                "Weighted Avg Depreciation Rate = Depreciation & Amortization / (Avg. Gross PP&E + Avg. Intangible Assets)": weight_avg_dep_rate,                   
            }

            ratio_list.append(ratio_dict)

        ratio_df = pd.DataFrame(ratio_list).T
        ratio_df.columns = balance_table.columns[2:]
        ratio_df = ratio_df.reset_index()
        table = ratio_df.rename(columns = {'index': 'Ratios'})
        
    except:
        table = pd.DataFrame([{
            'Ratios': '-',
            str(date.today().year - 4): '-',
            str(date.today().year - 3): '-',
            str(date.today().year - 2): '-',
            str(date.today().year - 1): '-'
        }])
        
    
    # Return table
    return html.Div([
        dash_table.DataTable(
            data = table.to_dict('records'),
            columns = [{'id': c, 'name': c} for c in table.columns],
            style_cell_conditional = [{'if': {'column_id': c},'textAlign': 'left'} for c in ['Ratios']],
            style_cell = {'font-family':'Arial, Helvetica, sans-serif'},
            style_as_list_view = True,
            style_header = {
                'font-family':'Arial, Helvetica, sans-serif',
                'font-size': 24,
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional = [ { 'if': {'filter_query': '{Ratios} contains ":"' },'fontWeight': 'bold'}]
        )
    ],
        style = {
            'padding-top': 10,
            'padding-left': 10,
            'padding-right': 15,
            'padding-bottom': 10,
        })

