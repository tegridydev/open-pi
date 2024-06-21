import json
import yaml
from .intent_screening import IntentScreening
from .tool_selection import ToolSelection
from .parameter_extraction import ParameterExtraction
from .function_execution import FunctionExecution
from .chat_extension import ChatExtension
from .scheduler import Scheduler
from .json_schema_enforcer import JSONSchemaEnforcer

class OpenPi:
    def __init__(self, config, functions):
        self.intent_screening = IntentScreening(config)
        self.tool_selection = ToolSelection(functions)
        self.parameter_extraction = ParameterExtraction()
        self.function_execution = FunctionExecution()
        self.chat_extension = ChatExtension()
        self.scheduler = Scheduler()
        self.schema_enforcer = JSONSchemaEnforcer()

    def handle_query(self, query):
        screened_query = self.intent_screening.screen_intent(query)
        selected_tool = self.tool_selection.select_tool(screened_query)
        if selected_tool:
            parameters = self.parameter_extraction.extract_parameters(screened_query, selected_tool)
            if self.schema_enforcer.enforce(parameters, selected_tool.schema):
                result = self.function_execution.execute_function(selected_tool, parameters)
                return self.chat_extension.extend_chat(result)
            return "Parameters do not comply with the schema."
        return "No suitable function found to handle the query."

    def schedule_query(self, query, interval):
        self.scheduler.schedule_function(self.handle_query, interval, query)

    def run_scheduler(self):
        self.scheduler.run_continuously()

    def handle_json(self, json_data):
        query = json.loads(json_data)
        return self.handle_query(query)

    def handle_yaml(self, yaml_data):
        query = yaml.safe_load(yaml_data)
        return self.handle_query(query)
