"""This module handles resetting the state of the computer so the robot can work with a clean slate."""
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from msb_rpa.logins import modulus_login
from msb_rpa.generelt import use_retry_logic
from msb_rpa.web import close_website_panes


def reset(orchestrator_connection: OrchestratorConnection) -> None:
    """Clean up, close/kill all programs and start them again. """
    orchestrator_connection.log_trace("Resetting.")
    kill_all(orchestrator_connection)
    open_all(orchestrator_connection)


def kill_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Forcefully close all applications used by the robot."""
    orchestrator_connection.log_trace("Killing all applications.")
    close_website_panes()
    orchestrator_connection.log_trace("Killed all applications succesfully")


def open_all(orchestrator_connection: OrchestratorConnection) -> None:
    """Open all programs used by the robot."""
    orchestrator_connection.log_trace("Opening all applications.")
    gemt_credential = orchestrator_connection.get_credential("032_Boerns_Trivsel")
    bearer_token = use_retry_logic(modulus_login, username=gemt_credential.username, password=gemt_credential.password, drivertype='chrome_wire')
    orchestrator_connection.log_trace("Opened application succesfully")
    return bearer_token
