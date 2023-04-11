import pandas as pd
from collections import OrderedDict

def multiplyList(myList):
    acumulado = []
    result = 1
    for x in myList:
        result = result * x
        acumulado.append(result -1 )
    return acumulado


class MonetaryCorrection:
    def __init__(self):
        ipca_data = pd.read_csv("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv", sep=";")
        ipca_data["valor"] = ipca_data.valor.str.replace(",", ".").astype(float)
        ipca_data["taxa"] = ipca_data["valor"]/100 + 1   
        ipca_data["acumulado"] = multiplyList(list(ipca_data["taxa"]))
        
        self.ipca_data = OrderedDict()
        
        for item in ipca_data.values.tolist():
            dia, mes, ano, = item[0].split("/")
            self.ipca_data.setdefault(int(ano), {})[int(mes)] = item[3] #adiciona o acumulado
            
        
    def ipca(self, value, date_start, date_end):
        """
        >>> corretor.ipca(100, "07/2019", "02/2023")
        (125.87, 25.86683)
        
        >>> corretor.ipca(231.24, "01/2002", "02/2023")
        (837.26, 262.07534)
        
        >>> corretor.ipca(231.24, "1/2002", "2/2023")
        (837.26, 262.07534)
        
        >>> corretor.ipca(231.24, "1/2002", "2/2223")
        Traceback (most recent call last):
        ...
        ValueError: Datas inválidas
        
        """
        date_start = pd.Timestamp(date_start) - pd.DateOffset(months=1)#reduz um mês     
        month_start, year_start = date_start.month, date_start.year
        month_end, year_end = date_end.split("/")
        try:
            cumulated = ((1+ self.ipca_data[int(year_end)][int(month_end)]) / (1 + self.ipca_data[year_start][month_start])) - 1
        except KeyError: 
            raise ValueError("Datas inválidas")
        
        return round(value * (1 + cumulated), 2), round(cumulated * 100, 5)

    
ipca = MonetaryCorrection().ipca
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'corretor': MonetaryCorrection()})