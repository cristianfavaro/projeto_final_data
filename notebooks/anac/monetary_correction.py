import pandas as pd
    
class MonetaryCorrection:
    def __init__(self):

        ipca_data = pd.read_csv("https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv", sep=";")
        ipca_data["valor"] = ipca_data.valor.str.replace(",", ".").astype(float)
        ipca_data["taxa"] = ipca_data["valor"]/100 + 1     
        ipca_data["data"] = pd.to_datetime(ipca_data["data"].str[3:], format="%m/%Y") 
        ipca_data['correction_index'] = ipca_data.taxa.cumprod()

        self.ipca_data = ipca_data[["data", "correction_index"]]
            
    def ipca(self, value, date_start, date_end):
        """
        >>> corretor.ipca(100, "07/2019", "02/2023")
        (125.87, 25.86683)
        
        >>> corretor.ipca(231.24, "01/2002", "02/2023")
        (837.26, 262.07534)
        
        >>> corretor.ipca(231.24, "1/2002", "2/2023")
        (837.26, 262.07534)
               
        """
        
        correction_index_start = float(
            self.ipca_data[self.ipca_data["data"] == pd.to_datetime(date_start, format="%m/%Y") - pd.DateOffset(months=1)]["correction_index"]
        )
   
        correction_index_end = float(
            self.ipca_data[self.ipca_data["data"] == pd.to_datetime(date_end, format="%m/%Y")]["correction_index"] 
        )

        correction_index_in_time = (correction_index_end / correction_index_start)

        return round(value * correction_index_in_time, 2), round((correction_index_in_time - 1) * 100, 5)
 
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'corretor': MonetaryCorrection()})