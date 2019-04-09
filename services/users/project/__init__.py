from flask import Flask, jsonify

# instantiate!
app = Flask(__name__)

# set config
app.config.from_object('project.config.DevConfig')


@app.route('/users/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'success',
        'message': 'healthy'
    })
