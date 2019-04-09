from flask import Flask, jsonify

# instantiate!
app = Flask(__name__)

@app.route('/users/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'healthy'
    })
