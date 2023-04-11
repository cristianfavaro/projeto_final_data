import pandas as pd
from functools import reduce

    
class MonetaryCorrection:
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
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'corretor': MonetaryCorrection()})