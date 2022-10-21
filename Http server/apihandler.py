from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import socket
import datetime
import subprocess
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
api = Api(app)

Demo_status = False


class init(Resource):

    def post(self):
        global Demo_status
        print("[INFO] INIT request received")
        parser = reqparse.RequestParser()
        parser.add_argument('Demo_status', required=True)    # add arguments
        body = parser.parse_args()

        if body['Demo_status'] == 'True':
            Demo_status = True
        else:
            Demo_status = False
        string = {"STATE": True, "Verify": "chunk"}
        print(f'[STATUS] Demo_status: {Demo_status}\n')
        return (string)


class action(Resource):
    def time_to_seconds(self, time: str, cancel: str):
        if not cancel == "True":
            # its not cancel cmd
            try:
                date_time = datetime.datetime.strptime(time, "%H:%M:%S")
                a_timedelta = date_time - datetime.datetime(1900, 1, 1)
                seconds = a_timedelta.total_seconds()
                return int(seconds)
            except ValueError:
                # in case its an err
                return 0
        else:
            # its cancel command
            return False

    def post(self):
        global Demo_status
        print("[INFO] POST ACTION request received")
        parser = reqparse.RequestParser()
        parser.add_argument('Action', required=True)    # add arguments
        parser.add_argument('Time', required=True)    # add arguments
        parser.add_argument('Demo_status', required=True)  # add args
        parser.add_argument('Cancel')  # add args
        body = parser.parse_args()

        Action = body['Action']  # get mode
        Time = body['Time']  # get string time
        Demo_status = body['Demo_status']
        cancel = body['Cancel']
        # convert to seconds

        time_sec = self.time_to_seconds(Time, cancel)
        print(Demo_status)
        if Demo_status == "True" and cancel == 'False':
            if time_sec > 0:
                string = {"STATUS": True, "Time": time_sec}
                print(
                    f'[OPUTPUT]  (Temp) PC will {Action} in {time_sec} seconds\n')
                return jsonify(string)
            else:
                string = {"STATUS": True, "Time": time_sec,
                          "Error": "Wrong time input"}
                print(f'[OPUTPUT]  (Temp) erro in conv\n')
                return jsonify(string)
        elif cancel == 'False':
            if time_sec > 0:
                string = {"STATUS": True, "Time": time_sec}

                print(
                    f'[OPUTPUT]  (Real) PC will {Action} in {time_sec} seconds\n')
                subprocess.run(["shutdown", "-a"],  shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run(["shutdown", "-s", "-t", f"{time_sec}"],  shell=True,
                               stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return jsonify(string)
            else:
                string = {"STATUS": True, "Time": time_sec,
                          "Error": "Wrong time input\n"}
                print(f'[OPUTPUT]  (Real) erro in conv')
                return jsonify(string)
        else:
            string = {"STATUS": time_sec}
            subprocess.run(["shutdown", "-a"],  shell=True, stdout=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[OPUTPUT] ALL ACTIVE COMMANDS CANCELED\n")
            print(string)
            return jsonify(string)


# for debug
# gets body
# @app.after_request
# def after(response):
#         print(response.status)
#         print(response.headers)
#         print(response.get_data())
#         return response

api.add_resource(action, '/action', methods=['POST'])
api.add_resource(init, '/init', methods=['POST'])
if __name__ == '__main__':
    localip = socket.gethostbyname(socket.gethostname())
    port = 5000
    print('\n', '#'*54, '\n', '#'*15, "REMOTE SHUTDOWN SERVER",
          "#"*15, '\n', '#'*54, sep=None, end=None)
    print(f'\n\n[INFO] Server running on {localip}:{port}\n\n')
    # Development server
    # app.env = "development"
    # app.run(debug=True,host=localip,port=port)

    # Production server
    http_server = WSGIServer((str(localip), port), app)
    http_server.serve_forever()
    print("EXITING.........")
