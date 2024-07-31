import logging
from .tools.image_tools import create_image_from_prompt
from .tools.video_tools import create_video_from_image
from .tools.smart_contract_tools import generate_smart_contract
from .config.default_config import global_config
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThetaAgent:
    def __init__(self, capabilities: List, show_planning: bool = False, persona: str = '', config_thread_id: str = ''):
        self.edgecloud_endpoint = global_config["llm_endpoint"]
        self.model_name = global_config["llm_model_name"]
        self.api_key = global_config.get("llm_api_key", None)
        self.show_planning = show_planning
        self.capabilities = capabilities
        self.persona = persona
        self.config_thread_id = config_thread_id

        self.memory = MemorySaver()
        self.llm = ChatOpenAI(
            base_url=self.edgecloud_endpoint,
            model=self.model_name,
            api_key=self.api_key,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            verbose=True
        )

        self.llm = self.llm.bind(response_format={"type": "json_object"})
        system_prompt = """
            \nYou must always return JSON in the following format:
            {
                "planning_text": <when asked to do a task, you first must break it down like 'the user wants me to do X so here are steps I'll take to do that: ..[steps]> => this is only when you're asked to do something, not if they just say 'hello' and its only for the FINAL MESSAGE ones.,
                "user_facing_text": <the final message you want to send to the human>
                
            }

            The internal planning message isn't always necessary to be populated if the user's input isn't really a task. For example if they say 'hello' you'd just respond with
            {
                "planning_text": "",
                "user_facing_text": "Hi! Nice to meet you.", # this is just an example, just respond however you would to something like this
            }

            But if it is a task like "I nmeed a campaign about monkeys and it needs to include a image and a video that makes sense for me" your response might be:
            {
                "planning_text": "the user wants me to do X so here are steps I'll take to do that: ..[steps]",
                "user_facing_text": "Great! Here's my plan of approach. Shall we go ahead?"
            }

            Of course if it's a tool call request there's no content you need to provide. REMEMBER TO RESPOND WITH VALID JSON AND ONLY VALID JSON

        """
        if self.persona:
            system_prompt += f"\nYou are a helpful assistant with the persona detailed below: \n{self.persona}"
          
        self.system_prompt = system_prompt

        self.graph = create_react_agent(
            model=self.llm.bind_tools(self.capabilities),
            tools=self.capabilities,
            checkpointer=self.memory,
            state_modifier=self.system_prompt
        )
        if not self.config_thread_id:
            self.config_thread_id = self.generate_random_string()
        
        logger.info(f"Config thread ID: {self.config_thread_id}")
        self.thread_config = {"configurable": {"thread_id": self.config_thread_id}}

    def __call__(self, user_input: str) -> Dict:
        input_message = HumanMessage(content=user_input)
        response_data = {}
        for event in self.graph.stream({"messages": [input_message]}, config=self.thread_config, stream_mode="values"):
            last_message = event["messages"][-1]
            if isinstance(last_message, AIMessage):
                last_message_content = last_message.content
                if last_message_content:
                    try:
                        parsed_response = json.loads(last_message_content)
                        response_data['planning_text'] = parsed_response.get('planning_text', '')
                        response_data['user_facing_text'] = parsed_response.get('user_facing_text', '')
                    except json.JSONDecodeError as e:
                        response_data['error'] = e.msg
                        logger.error(f"JSONDecodeError: {e.msg}")
        return response_data

    @staticmethod
    def generate_random_string(size=10):
        import random, string
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))