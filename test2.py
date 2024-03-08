from flask import Flask, render_template_string, request, jsonify
import g4f

app = Flask(__name__)

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beautiful Chat</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/themes/prism-okaidia.min.css">
    <style>
        body {
            background-color: #212529; /* Тёмный фон */
            color: #fff; /* Белый текст */
            font-family: Arial, sans-serif;
            padding-bottom: 100px;
        }

        .container {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            background-color: #343a40; /* Цвет контейнера */
            margin-bottom: 50px;
        }

        #chat-box {
            max-height: 600px; /* Увеличение высоты чата */
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 10px;
            background-color: #454d55; /* Цвет фона чата */
        }

        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            overflow-wrap: break-word;
        }

        .user-message {
            /* Удаление границы и цвета фона */
        }

        .bot-message {
            /* Удаление границы и цвета фона */
        }

        #chat-form {
            margin-top: 20px;
            margin-bottom: 20px; /* Добавлено для увеличения расстояния между формой и чатом */
        }

        #user-input {
            width: calc(100% - 100px);
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 20px;
            font-size: 16px;
            color: #fff; /* Цвет текста в поле ввода */
            background-color: #495057; /* Цвет фона поля ввода */
        }

        button[type="submit"] {
            padding: 10px 20px;
            margin-left: 10px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
        }

        .typing-dots {
            display: none;
            color: #fff;
            font-size: 16px;
        }

        .code {
            font-size: 14px;
        }

        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #007bff;
            margin-right: 10px;
            display: inline-block;
            vertical-align: middle;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="avatar"></div>
        <h1 style="display: inline-block; vertical-align: middle;">Beautiful Chat</h1>
        <div id="chat-box"></div>
        <form id="chat-form">
            <input type="text" id="user-input" placeholder="Enter your message...">
            <button type="submit">Send</button>
        </form>
        <span class="typing-dots"></span>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.23.0/plugins/autoloader/prism-autoloader.min.js"></script>
    <script>
        $(document).ready(function () {
            $('#chat-form').submit(function (e) {
                e.preventDefault();
                var userInput = $('#user-input').val().trim();
                if (userInput === '') return;

                var userMessageDiv = $('<div class="message user-message"></div>');
                var userMessageText = $('<span></span>').html(userInput);
                userMessageDiv.append(userMessageText);
                $('#chat-box').append(userMessageDiv);

                $('#user-input').val('');

                $('.typing-dots').css('display', 'inline');

                var animationInterval = setInterval(function() {
                    var typingDots = $('.typing-dots');
                    typingDots.text(typingDots.text() === '...' ? '..' : '...');
                }, 500);

                $.ajax({
                    url: '/chat',
                    type: 'POST',
                    data: {user_input: userInput},
                    success: function (data) {
                        clearInterval(animationInterval);
                        $('.typing-dots').css('display', 'none');
                        var botResponse = data.conversation[data.conversation.length - 1].content;
                        var botMessageDiv = $('<div class="message bot-message"></div>');
                        var botMessageText = $('<span class="code"></span>').html(botResponse);
                        botMessageDiv.append(botMessageText);
                        $('#chat-box').append(botMessageDiv);
                        Prism.highlightAll(); // Подсветка кода
                        $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
                    }
                });
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    conversation = [{'role': 'user', 'content': user_input}]

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        stream=True,
    )

    bot_response = ''.join(response)
    bot_response_with_br = bot_response.replace('\n', '<br>')
    bot_response_cleaned = bot_response_with_br.replace('**', '')

    conversation.append({'role': 'bot', 'content': bot_response_cleaned})

    return jsonify({'conversation': conversation})

if __name__ == '__main__':
    app.run(debug=True)

