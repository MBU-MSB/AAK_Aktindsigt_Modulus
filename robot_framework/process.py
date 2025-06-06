"""This module contains the main process of the robot."""
import json
from msb_rpa.generelt import sql_insert_result
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from robot_framework import config
from robot_framework.Processer.Modulus.modulus_api_calls import get_fileids_by_case_api
from robot_framework.Processer.Modulus.modulus_api_calls import get_filelinks_by_fileid_api


def process(orchestrator_connection: OrchestratorConnection, queue_element, bearer_token: str) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    # Gemmer data kolonnen som en dictionary, hvis du har behov for at hente data derfra.
    queue_data_string = queue_element.data
    rpa_id = str(queue_element.reference)
    executionid = str(queue_element.id)
    # Konverterer kun data kolonnen til dictionary, hvis den indeholder data.
    if queue_data_string:
        queue_dict = json.loads(queue_data_string)
    else:
        queue_dict = ''
    # Hent RPA_ID og ExecutionID fra køelementet

    sql_connection = orchestrator_connection.get_credential("sql_connection_string").password

    sql_insert_result(rpa_id, executionid, '1', "{}", sql_connection, config.RESULT_TABLE)

    orchestrator_connection.log_trace("Start: get_fileids_by_case_api, to get all the filelinks connected to the caseID")
    fileid_list = get_fileids_by_case_api(bearer_token, queue_dict["SagsID"], queue_dict["Startdato"], queue_dict["Slutdato"])
    orchestrator_connection.log_trace("Slut: get_fileids_by_case_api")

    orchestrator_connection.log_trace("Start: get_filelinks_by_fileid_api, to download the files")
    for fileid in fileid_list:
        get_filelinks_by_fileid_api(bearer_token, fileid, queue_dict["Serial"], queue_dict["CPR"])
    orchestrator_connection.log_trace("Slut: get_filelinks_by_fileid_api")

    sql_insert_result(rpa_id, executionid, '2', "{}", sql_connection, config.RESULT_TABLE)
