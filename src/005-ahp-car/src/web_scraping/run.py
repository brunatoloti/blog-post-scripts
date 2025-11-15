import pandas as pd
import requests

class ExtractVehiclesInfos:
    def __init__(self):
        self.df_extract = pd.DataFrame()
        self.df_transform = pd.DataFrame()
        self.options = [('fiat', 'pulse'), ('volkswagen', 't-cross'), ('citroen', 'c3')]

    def run(self):
        self.extract()
        if not self.df_extract.empty:
            self.transform()
            if not self.df_transform.empty:
                self.load()
            else:
                print('#2 - Empty dataframe!')
        else:
            print('#1 - Empty dataframe!')
    
    def extract(self):
        for option in self.options:
            url = f'https://www.webmotors.com.br/catalogo/api/specification/searchByYear/{option[0]}/{option[1]}/2026/999'
            req = requests.get(url).json()['result']
            for r in range(0, len(req)):
                price = req[r]['Precos']['PrecoSugerido']
                brand = option[0].upper()
                model = option[1].upper()
                version = req[r]['Versao']['nome']
                doors = req[r]['Especificacao']['Propriedades']['NumeroPortas']
                seats = req[r]['Especificacao']['Propriedades']['NumeroOcupantes']
                transmission = req[r]['Especificacao']['Propriedades']['TipoCambio']
                fuel = req[r]['Especificacao']['Propriedades']['TipoCombustivel1']
                try:
                    city_consumption_e = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][3]['Itens'] if i['Nome'] == 'Consumo cidade (km/litro) - Combustível 1'][0]
                except:
                    city_consumption_e = ''
                try:
                    road_consumption_e = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][3]['Itens'] if i['Nome'] == 'Consumo estrada (km/litro) - Combustível 1'][0]
                except:
                    road_consumption_e
                try:
                    city_consumption_g = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][3]['Itens'] if i['Nome'] == 'Consumo cidade (km/litro) - Combustível 2'][0]
                except:
                    city_consumption_g = ''
                try:
                    road_consumption_g = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][3]['Itens'] if i['Nome'] == 'Consumo estrada (km/litro) - Combustível 2'][0]
                except:
                    road_consumption_g = ''
                try:
                    fuel_tank_capacity = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][6]['Itens'] if i['Nome'] == 'Capacidade tanque de combustível (litros)'][0]
                except:
                    fuel_tank_capacity = ''
                try:
                    car_trunk_capacity = [i['Valor'] for i in req[r]['Especificacao']['Categorias'][6]['Itens'] if i['Nome'] == 'Capacidade do porta-malas (litros)'][0]
                except:
                    car_trunk_capacity = ''
                d = {'brand': [brand], 'model': [model], 'version': [version], 'price': [price], 'doors': [doors], 'seats': [seats], 
                    'transmission': [transmission], 'fuel': [fuel], 'city_consumption_e': [city_consumption_e], 'road_consumption_e': [road_consumption_e],
                    'city_consumption_g': [city_consumption_g], 'road_consumption_g': [road_consumption_g],
                    'fuel_tank_capacity': [fuel_tank_capacity], 'car_trunk_capacity': [car_trunk_capacity]}
                self.df_extract = pd.concat([self.df_extract, pd.DataFrame(d)])
    
    def transform(self):
        versions_filter = ['1.3 FLEX DRIVE CVT', '1.0 TURBO 200 FLEX YOU CVT', '1.0 200 TSI TOTAL FLEX SENSE AUTOMÁTICO']
        self.df_transform = self.df_extract.query(f"version in {versions_filter}")
        cols_transform = ['city_consumption_e', 'road_consumption_e', 'city_consumption_g', 'road_consumption_g',
                          'fuel_tank_capacity', 'car_trunk_capacity']
        for col in cols_transform:
            self.df_transform[col] = self.df_transform[col].apply(lambda x: float(x.replace(',', '.')))

    def load(self):
        self.df_transform.to_csv('../data/vehicles_infos.csv', index=False)


if __name__=='__main__':
    ExtractVehiclesInfos().run()