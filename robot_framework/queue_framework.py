"""This module is the primary module of the robot framework. It collects the functionality of the rest of the framework."""

# This module is not meant to exist next to linear_framework.py in production:
# pylint: disable=duplicate-code
import sys
from OpenOrchestrator.orchestrator_connection.connection import OrchestratorConnection
from OpenOrchestrator.database.queues import QueueStatus
from OpenOrchestrator.database.db_util import get_all_triggers
from robot_framework import initialize, reset, process, config
from robot_framework.exceptions import handle_error, BusinessError, log_exception


def main():
    """The entry point for the framework. Should be called as the first thing when running the robot."""

    orchestrator_connection = OrchestratorConnection.create_connection_from_args()

    sys.excepthook = log_exception(orchestrator_connection)

    orchestrator_connection.log_trace("Robot Framework started.")
    initialize.initialize(orchestrator_connection)

    queue_element = None
    error_count = 0
    task_count = 0
    # Retry loop
    for _ in range(config.MAX_RETRY_COUNT):
        try:
            reset.reset(orchestrator_connection)

            # Queue loop
            while task_count < config.MAX_TASK_COUNT:
                task_count += 1
                alle_triggers = get_all_triggers()
                trigger_paused = False
                # Trigger loop
                for trigger in enumerate(alle_triggers):
                    if trigger[1].process_name == config.QUEUE_NAME:
                        if "PAUSED" in str(trigger[1].process_status.name) or "PAUSING" in str(trigger[1].process_status.name):
                            orchestrator_connection.log_info("Trigger paused - closing down.")
                            trigger_paused = True
                            break  # Break Trigger loop
                if trigger_paused:
                    break  # Break queue loop
                queue_element = orchestrator_connection.get_next_queue_element(config.QUEUE_NAME, set_status=True)

                if not queue_element:
                    orchestrator_connection.log_info("Queue empty.")
                    break  # Break queue loop

                try:
                    process.process(orchestrator_connection, queue_element)
                    orchestrator_connection.set_queue_element_status(queue_element.id, QueueStatus.DONE)

                except BusinessError as error:
                    handle_error("Business Error", error, queue_element, orchestrator_connection)

            break  # Break retry loop

        # We actually want to catch all exceptions possible here.
        # pylint: disable-next = broad-exception-caught
        except Exception as error:
            error_count += 1
            handle_error(f"Process Error #{error_count}", error, queue_element, orchestrator_connection)

    reset.kill_all(orchestrator_connection)

    if config.FAIL_ROBOT_ON_TOO_MANY_ERRORS and error_count == config.MAX_RETRY_COUNT:
        raise RuntimeError("Process failed too many times.")
