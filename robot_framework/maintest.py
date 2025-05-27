"""Test hele eller dele af robotprocessen"""
import os
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from msb_rpa.generelt import use_retry_logic
from msb_rpa.logins import modulus_login


# ###TEST TEST TEST####
connection_string = os.environ.get("OpenOrchestratorConnString")
crypto_key = os.environ.get("OpenOrchestratorKey")
orchestrator_connection = OrchestratorConnection(process_name="000_00_Eksempel", connection_string=connection_string, crypto_key=crypto_key, process_arguments="none")
# ###TEST TEST TEST####

gemt_credential = orchestrator_connection.get_credential("032_Boerns_Trivsel")
bearer_token = use_retry_logic(modulus_login, username=gemt_credential.username, password=gemt_credential.password, drivertype='chrome_wire')
# login

print("Stop her")
