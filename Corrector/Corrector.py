import pandas as pd
import requests
import csv
from flask import Flask, jsonify
import ssl

# Отключаем SSL проверку
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Чтение CSV файлов
MTR_PATH = 'MTR.csv'
OKPD2_PATH = 'OKPD_2.csv'

# Получение токена для работы с Gigachat
def get_gigachat_token():
    url_auth = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    payload = {'scope': 'GIGACHAT_API_PERS'}
    headers_auth = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': 'f61048d8-3ef0-411e-8805-b43f80373713',
        'Authorization': 'Basic <TOKEN>'  # Вставьте сюда свой ключ
    }
    response_auth = requests.post(url_auth, headers=headers_auth, data=payload, verify=False)
    if response_auth.status_code == 200:
        token_data = response_auth.json()
        return token_data['access_token']
    else:
        print(f"Ошибка получения токена: {response_auth.text}")
        return None

# Формирование промта для запроса к модели Gigachat
def create_prompt(product_name, gost, params):
    prompt = (f"Проанализируй информацию о продукте с наименованием '{product_name}', "
              f"ГОСТом '{gost}' и характеристиками '{params}', и укажи соответствующий код ОКПД2 "
              f"из списка эталонных кодов. Если код ОКПД2 указан неверно, предложи правильный код.")
    return prompt

# Запрос на сопоставление с Gigachat API
def match_with_gigachat(product_name, gost, params, token):
    url_model = "https://gigachat.devices.sberbank.ru/api/v1/models"
    headers_model = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    # Формирование промта для модели
    prompt = create_prompt(product_name, gost, params)

    payload = {
        "prompt": prompt  # Передаем сформированный промт в качестве запроса
    }
    
    response_model = requests.post(url_model, headers=headers_model, json=payload, verify=False)
    
    if response_model.status_code == 200:
        return response_model.json()
    else:
        print(f"Ошибка при запросе к Gigachat: {response_model.text}")
        return None

# Маршрут для обновления всех продуктов
@app.route('/update_all_products', methods=['GET'])
def update_all_products():
    try:
        # Чтение таблиц
        mtr_data = pd.read_csv(MTR_PATH, sep=',')
        okpd2_data = pd.read_csv(OKPD2_PATH, sep=',')
        
        # Получение токена для работы с Gigachat
        token = get_gigachat_token()
        if not token:
            return jsonify({"status": "error", "message": "Не удалось получить токен Gigachat"}), 500

        updated_products = []

        for _, row in mtr_data.iterrows():
            product_name = row['Наименование']
            gost = row['Регламенты (ГОСТ/ТУ)']
            params = row['Параметры']
            
            # Запрос к Gigachat для сопоставления
            match = match_with_gigachat(product_name, gost, params, token)
            if match:
                # Проверка соответствия ОКПД2
                correct_okpd2 = match.get('correct_okpd2')
                if correct_okpd2 and correct_okpd2 != row['ОКПД2']:
                    row['ОКПД2'] = correct_okpd2  # Обновляем код ОКПД2
                    updated_products.append(row)
        
        # Запись обновленных данных обратно в файл (можно также обновить в базе данных)
        mtr_data.to_csv(MTR_PATH, sep=',', index=False)
        
        return jsonify({"status": "success", "updated_products": len(updated_products)}), 200

    except Exception as e:
        print(f"Ошибка при обработке данных: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

