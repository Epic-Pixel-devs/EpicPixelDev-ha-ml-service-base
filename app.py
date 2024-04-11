# -*- coding: utf-8 -*-
from flask import Flask, jsonify

from services.env.build_env_service import BuildEnvService
from services.log.log_service import LogService
from services.scheduller_service import SchedulerService

log = LogService.log()

log.info(f'[root] (app): setting environment variables global on flask api')
BuildEnvService().load_environment('application.yml')

log.info(f'[root] (app): starting flask api')
app = Flask(__name__)

log.info(f'[root] (app): starting scheduler services')
ss = SchedulerService()
ss.start()


@app.route("/")
def health():
    try:
        return jsonify(message='The Server is OK!')
    except Exception as e:
        return jsonify(message=f'Error Server is down! {str(e)}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
