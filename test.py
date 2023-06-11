from sklearn.metrics import r2_score


st.header("Загрязнение атмосферы.\n Сравнение стран мира")
st.write("Итоговый проект по курсу Наука о данных, 2023")
st.write("Подготовила студентка 2 курса Совместного Баклавриата ВШЭ и РЭШ, Мороз Екатерина")
st.write("Конечно, нам должно беспокоить загрязнение воздуха на всей планете, поскольку границы государтв существуют только для людей и потоки воздушных масс распространя")
st.write("Рассмотрим, как в с загрязнением воздуха дела обстоят в России")

use_saved_data = False
# Если возникнут проблемы с запросами, вы можете заменить флаг на True,
# тогда будут использованы ранее запрошенные, данные.

def data_request(indicator_code):
    response = requests.get(f'https://ghoapi.azureedge.net/api/{indicator_code}')
    if response.status_code == 200:
        return pd.DataFrame(response.json()['value'])
    else:
        use_saved_data = True

if use_saved_data == False:
    fine_particulate_matter = data_request('SDGPM25')
    death_rate = data_request('AIR_42')
else:
    fine_particulate_matter = pd.read_csv('C:/Users/79096/Downloads/project/SDGPM25.csv')
    death_rate = pd.read_csv('C:/Users/79096/Downloads/project/AIR_42.csv')

co2_data = pd.read_csv('C:/Users/79096/Downloads/project/co2_data.csv')
co2_data = co2_data[['iso_code', 'country', 'year', 'co2', 'population']]


conn = sqlite3.connect("C:/Users/79096/Downloads/project/catalogs.sqlite")
cur = conn.cursor()


def drop_useless(data):
    data_new = data.dropna(axis=1, how='all')
    droped_columns = []
    for column in data_new.columns:
        if data_new[column].nunique() == 1:
            droped_columns.append(column)
    data_new = data_new.drop(droped_columns, axis=1)
    return data_new

fine_particulate_matter = drop_useless(fine_particulate_matter)
death_rate = drop_useless(death_rate)


fine_particulate_matter.head(2)


fine_particulate_matter = fine_particulate_matter[fine_particulate_matter['SpatialDimType'] == 'COUNTRY']

fine_particulate_matter = fine_particulate_matter.drop(
    ['Id', 'SpatialDimType', 'Value', 'Date', 'TimeDimensionValue', 'TimeDimensionBegin', 'TimeDimensionEnd'], axis=1)

fine_particulate_matter = fine_particulate_matter.rename(columns={
    'ParentLocationCode': 'Region',
    'SpatialDim': 'Country',
    'TimeDim': 'Year',
    'Dim1': 'Location',
    'NumericValue': 'Value',
    'Low': 'ValueLow',
    'High': 'ValueHigh'
})

fine_particulate_matter.head(3)
