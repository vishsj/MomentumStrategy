import yfinance as yf
import os 
import sys
import pandas as pd

def pulldata(ticker,period,interval,group_by,auto_adjust,prepost,threads,proxy):
    data = yf.download(tickers =ticker,period = period,interval = interval,group_by = group_by,
                       auto_adjust=auto_adjust,prepost= prepost,threads=threads, proxy = None)            
    return data
    
def main():
    working_directory = os.getcwd()
    folder_name = 'data'
    data_folder= os.path.join(working_directory,folder_name)
    nifty50_filename = 'nifty50list.csv'
    nifty50_list_path = os.path.join(data_folder,nifty50_filename)

    nifty50_ticker_list_df = pd.read_csv(nifty50_list_path)
    nifty50_tickers_list = nifty50_ticker_list_df['Symbol']
    NSE_extension_string = ".NS"
    appended_nifty50_tickers_list = [ string + NSE_extension_string for string in nifty50_tickers_list] 
    #print(appended_nifty50_tickers_list)
    for ticker in appended_nifty50_tickers_list:
        print(ticker)
        data = pulldata(ticker,"60d","5m",ticker,True,True,True,None)
        if(os.path.exists(os.path.join(data_folder,ticker+'.csv'))):
            print("The File exists, appending to the exisitng file")
            data.to_csv(os.path.join(data_folder,ticker+'.csv'), mode= 'a', header = False)
        else:
            print("The File does not exists, creating the file and writing in it")
            data.to_csv(os.path.join(data_folder,ticker+'.csv'), mode= 'w', header = True)

if __name__ == "__main__":
    main()