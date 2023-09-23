from langchain.agents.tools import Tool
from langchain.agents.conversational.base import ConversationalAgent
from langchain.agents import AgentExecutor
from tools import tools
from datetime import datetime

sop = [

    "1. Ask the user for their phone number to get their identity.",
    
    "2. Get the user's identity using the shared phone number with the tool, Get Customer Identity.",

    "3. Verify with the user that they are the person who's identity was returned with the tool.",

    "4. Get the customer's loan information using tool Get Customer Loans.",

    "5. Get saved payment method details using tool, Get Saved Payment Method.",

    "6. Ask the user if they want to use the saved payment method.",

    "7. Confirm with user they want to process the payment."

    "8. Process the payment using tool, Process Payment.",

    "9. Confirm with user the payment was processed successfully."

]

class Agent():
    def __init__(self, llm, memory) -> None:
        self.prefix = "What follows is a conversation with Grace, the virtual assistant of Mortgage, and Ujjal. The date is: " + \
            datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "." + \
            "\n To help the user make a mortgaeg payment he MUST follow these steps in order: \n" + str(sop) + \
            "\n\n\n Grace can also help do things like help the user calculate how many payments/time they have left on their loan and calculate how much interest they will pay over the life of the loan." + \
            "Grace can also help the user calculate how much they will save if they make an extra payment or start paying more on their loan."
        self.ai_prefix = "Grace"
        self.human_prefix = "Ujjal"
        self.llm = llm
        self.memory = memory
        self.agent = self.create_agent()

    def create_agent(self):
        agent = ConversationalAgent.from_llm_and_tools(
            llm=self.llm,
            tools=tools,
            prefix=self.prefix,
            ai_prefix=self.ai_prefix,
            human_prefix=self.human_prefix
        )
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=self.memory)
        return agent_executor

    def run(self, input):
        return self.agent.run(input=input)