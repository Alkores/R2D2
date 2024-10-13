import pandas as pd

# Загрузим данные
okpd_path = 'C:/Users/vladm/Desktop/OKPD_2.xlsx'
sfaf_path = 'C:/Users/vladm/Desktop/sfaf.xlsx'

okpd_df = pd.read_excel(okpd_path)
sfaf_df = pd.read_excel(sfaf_path)

# Удаляем последние группы ОКПД2 и сохраняем на уровень выше
sfaf_df['ОКПД2_уровень_выше'] = sfaf_df['ОКПД2'].str.slice(0, 8)  # Сохраняем только первые 8 символов (xx.xx.xx)

# Объединяем DataFrames по столбцу 'ОКПД2_уровень_выше'
result = sfaf_df.merge(okpd_df, left_on='ОКПД2_уровень_выше', right_on='OKPD2', how='left')

# Получаем главное слово в наименовании
result['Главное_слово'] = result['OKPD2_NAME'].astype(str).str.extract(r'([^\s]+)')[0]  # Используем [0], чтобы получить серию

# Убираем главное слово из наименования и помещаем оставшиеся слова в 'Параметры'
result['Параметры'] = result.apply(lambda x: x['Наименование'].replace(x['Главное_слово'], '').strip() if isinstance(x['Наименование'], str) else '', axis=1)

# Сохраняем 'Наименование' только с главным словом
result['Наименование'] = result['Главное_слово']

# Удаляем временные столбцы, если они не нужны
result.drop(columns=['ОКПД2_уровень_выше', 'OKPD2', 'Главное_слово'], inplace=True)

# Смотрим результат
print(result[['Наименование', 'Параметры']])
