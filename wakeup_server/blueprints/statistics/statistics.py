from flask import Blueprint, request, jsonify
from models.target_device_logs import TargetDeviceLogs
from models.signal_logs import SignalLogs

statistics_blueprint = Blueprint('statistics', __name__)

@statistics_blueprint.route('/statistics/signals', methods=['GET'])
def get_signal_logs():
    signal_logs = SignalLogs.aggregate_signal_logs_by_day()
    return jsonify(signal_logs), 200

@statistics_blueprint.route('/statistics/targets', methods=['GET'])
def get_target_logs():
    td_logs = TargetDeviceLogs.query.all()
    return jsonify([td_log.json() for td_log in td_logs]), 200

@statistics_blueprint.route('/statistics/patients', methods=['GET'])
def get_patient_logs():
    patient_signal_logs = SignalLogs.aggregate_signal_logs_by_patient()
    return jsonify(patient_signal_logs), 200


#@statistics_blueprint.route('/statistics/all', methods=['GET'])


