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
    <style>
        body {
            background-color: #222;
            color: #eee;
            font-family: Arial, sans-serif;
        }

        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            padding: 20px;
        }

        #chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #333;
        }

        .message {
            margin-bottom: 20px;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            display: flex;
            align-items: center;
        }

        .user-avatar, .bot-avatar {
            width: 30px; /* Reduced size */
            height: 30px; /* Reduced size */
            border-radius: 50%;
            background-color: #4CAF50; /* Green for user, change accordingly */
            margin-right: 10px;
        }

        .bot-avatar {
            background-color: #8e44ad; /* Purple for bot, change accordingly */
        }

        .user-message {
            color: white;
            align-self: flex-start;
        }

        .bot-message {
            color: white;
            align-self: flex-end;
        }

        #chat-form {
            padding-top: 20px;
        }

        #user-input {
            width: calc(100% - 100px);
            padding: 10px;
            border: none;
            border-radius: 20px;
            margin-right: 10px;
            font-size: 16px;
        }

        button[type="submit"] {
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
        }

        .typing-dots {
            color: #fff;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="chat-box"></div>
        <form id="chat-form">
            <input type="text" id="user-input" placeholder="Enter your message...">
            <button type="submit">Send</button>
        </form>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
        $(document).ready(function () {
            $('#chat-form').submit(function (e) {
                e.preventDefault();
                var userInput = $('#user-input').val().trim();
                if (userInput === '') return;

                $('#chat-box').append('<div class="message user-message"><div class="user-avatar"></div>' + userInput + '</div>');
                $('#user-input').val('');

                // Show typing dots
                var typingDots = $('<span class="typing-dots">...</span>');
                $('#chat-box').append(typingDots);

                // Animate typing dots
                var animationInterval = setInterval(function() {
                    typingDots.text(typingDots.text() === '...' ? '..' : '...');
                }, 500);

                $.ajax({
                    url: '/chat',
                    type: 'POST',
                    data: {user_input: userInput},
                    success: function (data) {
                        clearInterval(animationInterval); // Stop animation
                        typingDots.remove(); // Remove typing dots
                        var botResponse = data.conversation[data.conversation.length - 1].content;
                        $('#chat-box').append('<div class="message bot-message"><div class="bot-avatar"></div>' + botResponse + '</div>');
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

    conversation.append({'role': 'bot', 'content': bot_response})

    return jsonify({'conversation': conversation})

if __name__ == '__main__':
    app.run(debug=True)
