import pandas as pd
from functools import reduce
from collections import OrderedDict

class MonetaryCorrectionV0:
    def __init__(self):

        self.ipca_data = pd.read_csv("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv", sep=";")
        self.ipca_data["valor"] = self.ipca_data.valor.str.replace(",", ".").astype(float)
    
            
    def ipca(self, value, date_start, date_end=False):
        """
        >>> corretor.ipca(100, "07/2019", "02/2023")
        (125.87, 25.86683)
        
        >>> corretor.ipca(231.24, "01/2002", "02/2023")
        (837.26, 262.07534)
        
        >>> corretor.ipca(231.24, "1/2002", "2/2023")
        (837.26, 262.07534)
               
        """
        
        ipca = self.ipca_data[self.ipca_data["data"] >= pd.Timestamp(date_start)].copy()
        if date_end:
            ipca = ipca[ipca["data"] <= pd.Timestamp(date_end)]    

        ipca["taxa"] = ipca["valor"]/100 + 1          
        acumulado = (reduce(lambda x, y: x*y, list(ipca["taxa"])) - 1)    
    
        return round(value * (1 + acumulado), 2), round(acumulado * 100, 5)
    

def multiplyList(myList):
    acumulado = []
    result = 1
    for x in myList:
        result = result * x
        acumulado.append(result -1 )
    return acumulado


class MonetaryCorrectionV1:
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

class MonetaryCorrectionV2:
    def __init__(self):

        ipca_data = pd.read_csv("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv", sep=";")
        ipca_data["valor"] = ipca_data.valor.str.replace(",", ".").astype(float)
        ipca_data["taxa"] = ipca_data["valor"]/100 + 1     
        ipca_data["data"] = ipca_data["data"].str[3:]
        ipca_data['correction_index'] = ipca_data.taxa.cumprod()
        self.ipca_data = ipca_data

        self.ipca_data_dict = { data: value for data,value in ipca_data[["data", "correction_index"]].values }


    def ipca(self, value, date_start, date_end):
        """
        >>> corretor.ipca(100, "07/2019", "02/2023")
        (125.86683440392454, 25.86683)
        
        >>> corretor.ipca(231.24, "01/2002", "02/2023")
        (837.2630247284197, 262.07534)
        
        >>> corretor.ipca(231.24, "1/2002", "2/2023")
        (837.2630247284197, 262.07534)
               
        >>> corretor.ipca(222.24, "1/1998", "2/2020")
        (828.0753098285626, 272.60408)
        
        """

        date_start_valid = (pd.to_datetime(date_start, format="%m/%Y") - pd.DateOffset(months=1)).strftime('%m/%Y')
        correction_index_start = self.ipca_data_dict[date_start_valid]
        correction_index_end = self.ipca_data_dict[("0" + date_end)[-7:]]

        correction_index_in_time = (correction_index_end / correction_index_start)

        return value * correction_index_in_time, round((correction_index_in_time - 1) * 100, 5)
 
