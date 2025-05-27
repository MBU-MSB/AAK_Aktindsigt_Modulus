"""This module contains the main process of the robot."""
import json
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from robot_framework.Processer.make_folderpath import make_folderpath
from robot_framework.Processer.add_testfiles import add_testfiles


def process(orchestrator_connection: OrchestratorConnection, queue_element) -> None:
    """Do the primary process of the robot."""
    orchestrator_connection.log_trace("Running process.")
    # Gemmer data kolonnen som en dictionary, hvis du har behov for at hente data derfra.
    queue_data_string = queue_element.data
    # Konverterer kun data kolonnen til dictionary, hvis den indeholder data.
    if queue_data_string:
        queue_dict = json.loads(queue_data_string)
    else:
        queue_dict = ''
    # Hent RPA_ID og ExecutionID fra køelementet

    folderpath = make_folderpath(queue_dict["serial"], queue_dict["cpr"])
    add_testfiles(folderpath)


