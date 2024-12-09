from flask import Flask, request
import telegram

app = Flask(__name__)

BOT_TOKEN = '7641135357:AAFUuKRUv-exZq8YCLEq29EkrM3YSRuUKLg'
bot = telegram.Bot(token=BOT_TOKEN)

@app.route('/')
def index():
    return "Telegram Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        message_text = data['message'].get('text', '')

        try:
            if message_text:
                # Ожидаем баллы в формате: "30,40,50,60"
                scores = list(map(int, message_text.split(',')))

                if len(scores) != 4:
                    response_text = "Введите баллы для всех 4 заданий через запятую (например: 30,40,50,60)."
                else:
                    attestation1 = sum(scores[:2])
                    attestation2 = sum(scores[2:])
                    final_exam = 100  # Максимальный балл финального экзамена
                    
                    total_score = 0.3 * attestation1 + 0.3 * attestation2 + 0.4 * final_exam

                    response_text = f"""
Ваши баллы:
- 1-я аттестация: {attestation1}/60
- 2-я аттестация: {attestation2}/60
- Итоговый ожидаемый балл: {total_score}/100
"""
            else:
                response_text = "Пожалуйста, отправьте свои баллы через запятую (например: 30,40,50,60)."
        except ValueError:
            response_text = "Ошибка ввода. Убедитесь, что вы ввели только числа через запятую."

        bot.send_message(chat_id=chat_id, text=response_text)
    
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
