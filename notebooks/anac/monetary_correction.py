import pandas as pd

class MonetaryCorrection:
    def __init__(self):

        ipca_data = pd.read_csv("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv", sep=";")
        ipca_data["valor"] = ipca_data.valor.str.replace(",", ".").astype(float)
        ipca_data["taxa"] = ipca_data["valor"]/100 + 1     
        # ipca_data["data"] = ipca_data["data"].str[3:]
        ipca_data['correction_index'] = ipca_data.taxa.cumprod()
        self.ipca_data = ipca_data

        self.ipca_data_dict = {}

        for item in ipca_data.values.tolist():
            dia, mes, ano, = item[0].split("/")
            self.ipca_data_dict.setdefault(int(ano), {})[int(mes)] = item[3] #adiciona o acumulado


    def ipca(self, value, date_start, date_end):
        """
        >>> corretor.ipca(100, [7, 2019], [2, 2023])
        (125.86683440392454, 25.86683)
        
        >>> corretor.ipca(231.24, [1, 2002], [2, 2023])
        (837.2630247284197, 262.07534)
        
        >>> corretor.ipca(231.24, [1, 2002], [2, 2023])
        (837.2630247284197, 262.07534)
               
        >>> corretor.ipca(231.24, [1, 2002], [2, 2023])
        (837.2630247284197, 262.07534)

        >>> corretor.ipca(231.24, [1, 2002], [2, 2223])
        Traceback (most recent call last):
        ...
        ValueError: Datas inválidas
        """

        date_start = pd.Timestamp(date_start[1], date_start[0], 1) - pd.DateOffset(months=1)#reduz um mês 
        month_start, year_start = date_start.month, date_start.year
        month_end, year_end = date_end
        try:
            correction_index_in_time = (
                self.ipca_data_dict[year_end][month_end]) / (self.ipca_data_dict[year_start][month_start]
            )
        except KeyError: 
            raise ValueError("Datas inválidas")
        
        return value * correction_index_in_time, round((correction_index_in_time - 1) * 100, 5)



        # date_start_valid = (pd.to_datetime(date_start, format="%m/%Y") - pd.DateOffset(months=1)).strftime('%m/%Y')
        # correction_index_start = self.ipca_data_dict[date_start_valid]
        # correction_index_end = self.ipca_data_dict[("0" + date_end)[-7:]]

        # correction_index_in_time = (correction_index_end / correction_index_start)

        # return value * correction_index_in_time, round((correction_index_in_time - 1) * 100, 5)
 


ipca = MonetaryCorrection().ipca
    

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'corretor': MonetaryCorrection()})




