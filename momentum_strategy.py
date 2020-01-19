import pandas as pd 
import datetime 
import itertools
import os 

def total_pnl(start_price,end_price,number_of_shares_bought,number_of_shares_sold):
    SECURITIES_TRANSACTION_TAX = 0.00025 * (number_of_shares_sold* end_price)
    SEBI_Regulatory_Fees = 0.000002 * ((number_of_shares_sold* end_price)+ (number_of_shares_bought* start_price))
    Transaction_charges = 0.0000325 * ((number_of_shares_sold* end_price)+ (number_of_shares_bought* start_price))
    Brokerage_fees = 0.0005 * ((number_of_shares_sold* end_price)+ (number_of_shares_bought* start_price))
    total_transaction_fees = SECURITIES_TRANSACTION_TAX + SEBI_Regulatory_Fees + Transaction_charges + Brokerage_fees 
    return pnl(start_price,end_price)*number_of_shares_sold*start_price - total_transaction_fees

def pnl(start_price,end_price):
    return (end_price/start_price)-1

def trading_stock_list(master_csv_list_path):
    df = pd.read_csv(master_csv_list_path)
    tickers_list = df['Symbol']
    NSE_extension_string = ".NS"
    appended_tickers_list = [ string + NSE_extension_string for string in tickers_list] 
    return appended_tickers_list

def generate_stock_returns(data_folder,ticker,lookup_date_string,start_time,end_time):
    data = pd.read_csv(os.path.join(data_folder,ticker+'.csv'))
    df = data.loc[:,['Datetime','Close']]
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Date'] = df['Datetime'].dt.date
    df['Time'] = df['Datetime'].dt.time
    df.set_index('Datetime')
    df1 = df.loc[df['Date'] == pd.to_datetime(lookup_date_string),['Datetime','Close']]
    start_price = df1.loc[df1['Datetime'].dt.strftime("%H:%M:%S")==start_time,'Close'].item()
    end_price= df1.loc[df1['Datetime'].dt.strftime("%H:%M:%S")==end_time,'Close'].item()
    ticker_pnl = pnl(start_price,end_price)
    return [start_price, end_price,ticker_pnl]

def stock_ranking(return_dict,number_of_stocks_in_portfolio):
    portfolio_stocks = []
    sorted_return_dict = sorted(return_dict.items(), key = lambda x:x[1],reverse = True)
    portfolio_stocks_dict = sorted_return_dict[0:number_of_stocks_in_portfolio]
    for i in range (0,len(portfolio_stocks_dict)):
        portfolio_stocks.append(portfolio_stocks_dict[i][0])
    return portfolio_stocks

def common_equity(a, b): 
      
    a_set = set(a) 
    b_set = set(b) 
      
    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return{} 
    
def uncommon_equity(a, b): 
      
    a_set = set(a) 
    b_set = set(b) 
      
    # check length  
    if len(a_set-a_set.intersection(b_set)) > 0: 
        return(a_set-a_set.intersection(b_set))   
    else: 
        return{} 

def create_date_list(data_folder,ticker):
    df = pd.read_csv(os.path.join(data_folder,ticker+'.csv'))
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Date'] = df['Datetime'].dt.date
    date_list_series=df['Date']
    date_list_modified = date_list_series.unique()
    date_list = [pd.to_datetime(t) for t in date_list_modified]
    date_string_list = [t.strftime("%Y-%m-%d") for t in date_list]
    return date_string_list

def main():
    '''''
    sets up the directory , data folder and master_csv_file
    '''''
    original_open_price_dict = {}
    original_close_price_dict = {}
    original_return_dict = {}
    current_open_price_dict = {}
    current_close_price_dict = {}
    current_return_dict = {}
    working_directory = os.getcwd()
    folder_name = 'data'
    data_folder= os.path.join(working_directory,folder_name)
    master_csv_filename = 'nifty50list.csv'
    master_csv_list_path = os.path.join(data_folder,master_csv_filename)
    
    '''''
    creates the list of tickers of stocks within the master csv 
    '''''
    appended_nifty50_tickers_list = trading_stock_list(master_csv_list_path)
    
    '''''
    sets up the date and time strings 
    '''''
    lookup_dates = create_date_list(data_folder,"ADANIPORTS.NS")
    #lookup_dates_new = lookup_dates.remove('2019-10-27')
    #print(lookup_dates)
    
    original_start_time = '09:15:00'
    original_end_time = '11:15:00'
    time_points = 20
    base = pd.to_datetime( original_end_time, format='%H:%M:%S')
    time_list = [(base + datetime.timedelta(seconds=600*x)).strftime("%H:%M:%S") for x in range(time_points)]
    total_cum_pnl = 0
    pnl_history_dict = {}
    for lookup_date_string in lookup_dates :   
        print("\n")
        print('lookup_date_string is :', str(lookup_date_string))
        
        '''''
        generate the original ranking of stocks based on momentum
        '''''

        start_time = original_start_time
        end_time = original_end_time
        for ticker in appended_nifty50_tickers_list:
            start_price,end_price,pnl=generate_stock_returns(data_folder,ticker,lookup_date_string,start_time,end_time)
            original_open_price_dict[ticker]= start_price
            original_close_price_dict[ticker]= end_price
            original_return_dict[ticker]=pnl



        '''''
        generates the portfoilo of top n stocks based on historical momentum
        '''''   
        number_of_stocks_in_portfolio = 5
        original_portfolio_stocks = stock_ranking(original_return_dict,number_of_stocks_in_portfolio)
        long_portfolio = original_portfolio_stocks
        print('original portfolio suggestion is')
        print(original_portfolio_stocks)
        '''''
        generate the current ranking of stocks based on momentum
        '''''
        number_of_stocks_long = 5
        cum_pnl = 0
        PnL = {}


        for i in range (1,len(time_list)) :
            if(len(original_portfolio_stocks) == 0) :
                break
            else:
                print('number of stocks of original portfoilio still long : ' + str(len(original_portfolio_stocks)))
                start_time = time_list[i-1]
                end_time = time_list[i]

                for ticker in appended_nifty50_tickers_list:
                    start_price,end_price,pnl=generate_stock_returns(data_folder,ticker,lookup_date_string,start_time,end_time)
                    current_open_price_dict[ticker]= start_price
                    current_close_price_dict[ticker]= end_price
                    current_return_dict[ticker]=pnl

                current_portfolio_stocks = stock_ranking(current_return_dict,number_of_stocks_in_portfolio)
                print('current portfolio suggestion after iteration' + " " + str(i) + " " + 'is')
                print(current_portfolio_stocks)
                momentum_share_in_current_portfolio = common_equity(original_portfolio_stocks,current_portfolio_stocks)
                print('equity still with momentum')
                print(momentum_share_in_current_portfolio)
                momentum_share_not_in_current_portfolio = uncommon_equity(original_portfolio_stocks,current_portfolio_stocks)
                print('equity to be sold off')
                print(momentum_share_not_in_current_portfolio)
                #print('Total Profit and Loss after' + " " + str(i)+ " "+ 'iteration')
                print('Num of equity holding to be sold in iteration'+ " " + str(i)+ ": " + str(len(momentum_share_not_in_current_portfolio)))
                if(len(momentum_share_not_in_current_portfolio)==0):
                    cum_pnl = cum_pnl
                else:   
                    for ticker in momentum_share_not_in_current_portfolio :
                        PnL[ticker] = total_pnl(original_close_price_dict[ticker],current_close_price_dict[ticker],1,1)
                        print( ticker + ' buy price :' + " " + str(original_close_price_dict[ticker]) )
                        print( ticker + ' sell price :' + " " + str(current_close_price_dict[ticker]) )
                        cum_pnl = cum_pnl + PnL[ticker]
                    print(PnL)
                print('Total PnL after' + " " + str(i) + " "+ 'iteration')
                print(cum_pnl)
                original_portfolio_stocks = momentum_share_in_current_portfolio
                print('left stocks from original portfolio are :')
                print(original_portfolio_stocks)

        '''''
        generates the portfoilo of top n stocks based on historical momentum
        '''''   
        total_cum_pnl = cum_pnl
        pnl_history_dict[lookup_date_string] = cum_pnl
       
    
    print('Total Pnl of Strategy is : ' + str(total_cum_pnl))
    print('Pnl History by days is :')
    print(pnl_history_dict)
              
if __name__ == "__main__":
    main()