import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

risk_free_rate=0.05
month_in_year=12
class CAPM:
    def __init__(self,stocks,start_date,end_date):
        self.data=None
        self.stocks=stocks
        self.start_date=start_date
        self.end_date=end_date

    def download_data(self):
        data={}
        for stock in self.stocks:
            ticker=yf.download(stock,start=self.start_date,end=self.end_date,auto_adjust=False)
            data[stock]=ticker['Close']
            data[stock] = ticker['Close'].squeeze()


        return pd.DataFrame(data)

    def initialize(self):
        stock_data=self.download_data()
        stock_data=stock_data.resample('ME').last()
        self.data=pd.DataFrame({'s_adjclose': stock_data[self.stocks[0]],
                                'm_adjclose': stock_data[self.stocks[1]]})
        self.data[['s_return','m_return']]=np.log(self.data[['s_adjclose','m_adjclose']]/
                                                  self.data[['s_adjclose','m_adjclose']].shift(1))
        self.data=self.data[1::]

    def calculate_beta(self):
        covriance_matrix=np.cov(self.data ['s_return'],self.data['m_return'])
        beta=covriance_matrix[0,1]/covriance_matrix[1,1]
        print("Beta value is ", beta)

    def regression(self):
        beta,alpha=np.polyfit(self.data['m_return'],self.data['s_return'],deg=1)
        print("Beta value from regression is ", beta)
        print("Alpha value is ", alpha)
        expected_return=risk_free_rate+beta*(self.data['m_return'].mean()*month_in_year-
                                             risk_free_rate)
        print("Expected return is ", expected_return)
        self.plot_regression(alpha,beta)

    def plot_regression(self, alpha, beta):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(self.data["m_return"], self.data["s_return"],
                    label="Data Points")
        axis.plot(self.data["m_return"],
                beta * self.data["m_return"] + alpha,
                color="red", label="CAPM Line")
        plt.title('Capital Asset Pricing model, finding alpha and beta')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()


if __name__=="__main__":
    capm=CAPM(stocks=['IBM','^GSPC'],start_date='2010-01-01',end_date='2026-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()