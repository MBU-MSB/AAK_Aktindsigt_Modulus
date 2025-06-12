"""Test hele eller dele af robotprocessen"""
import os
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from msb_rpa.generelt import use_retry_logic
from msb_rpa.logins import modulus_login
from robot_framework import config
from robot_framework.Processer.Modulus.modulus_api_calls import get_fileids_by_case_api
from robot_framework.Processer.Modulus.modulus_api_calls import get_filelinks_by_fileid_api
from robot_framework.Processer.Fileconvert.docx_to_pdf import docx_to_pdf


# ###TEST TEST TEST####
connection_string = os.environ.get("OpenOrchestratorConnString")
crypto_key = os.environ.get("OpenOrchestratorKey")
orchestrator_connection = OrchestratorConnection(process_name=config.QUEUE_NAME, connection_string=connection_string, crypto_key=crypto_key, process_arguments="none")
# ###TEST TEST TEST####

gemt_credential = orchestrator_connection.get_credential("032_Boerns_Trivsel")
bearer_token = use_retry_logic(modulus_login, username=gemt_credential.username, password=gemt_credential.password, drivertype='chrome_wire')
# login

# test_dict = {"Bestiller":"lfrmi@aarhus.dk","CPR":"0909108999","Navn":"Per Familie","Startdato":"2024-01-01","Slutdato":"2025-06-30","SagsID":"114654","Serial":17}
# 92400
test_dict = {"Bestiller":"lfrmi@aarhus.dk","CPR":"AID4007012","Navn":"Astrid Test","Startdato":"2023-01-01","Slutdato":"2025-06-30","SagsID":"92388","Serial":17}

# 132018 Astrid Testborger sag
fileid_list = get_fileids_by_case_api(bearer_token, test_dict["SagsID"], test_dict["Startdato"], test_dict["Slutdato"])
for fileid in fileid_list:
    file_save_path = get_filelinks_by_fileid_api(bearer_token, fileid, test_dict["Serial"], test_dict["CPR"], test_dict["SagsID"])
    # if file_save_path.endswith(".docx"):
    #     docx_to_pdf(file_save_path)
    # else:
    #     print("No word doc")

print("Stop her")
