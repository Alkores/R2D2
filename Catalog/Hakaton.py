import pandas as pd

file_path = 'C:/Users/vladm/Desktop/sfaf.xlsx'
df = pd.read_excel(file_path)

required_columns = ['Наименование', 'Маркировка', 'Регламенты (ГОСТ/ТУ)', 'Параметры', 'Базисная Единица измерения', 'код СКМТР', 'ОКПД2']
if not all(col in df.columns for col in required_columns):
    raise ValueError("Некоторые необходимые столбцы отсутствуют в DataFrame.")

result_file_path = 'combined_output1.xlsx'
with pd.ExcelWriter(result_file_path) as writer:
    for okpd in df['ОКПД2'].unique():
        filtered_df = df[df['ОКПД2'] == okpd]

        combined_rows = []

        for item_name in filtered_df['Наименование'].unique():
            matching_rows = filtered_df[filtered_df['Наименование'] == item_name]
            combined_rows.append([item_name, '', '', '', '', ''])
            for _, row in matching_rows.iterrows():
                combined_rows.append([
                    '',
                    row['Маркировка'], 
                    row['Регламенты (ГОСТ/ТУ)'], 
                    row['Параметры'], 
                    row['Базисная Единица измерения'], 
                    row['код СКМТР']
                ])
        result_df = pd.DataFrame(combined_rows, columns=['Наименование', 'Маркировка', 'Регламенты (ГОСТ/ТУ)', 'Параметры', 'Базисная Единица измерения', 'код СКМТР'])

        result_df.to_excel(writer, sheet_name=str(okpd), index=False)
print("Объединение завершено, результат сохранен в", result_file_path)
