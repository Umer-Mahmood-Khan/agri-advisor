# src/your_project/crew.py
import yaml
from crewai import Agent, Task, Crew, Process
from mycrewaiproject.tools.weather_tool import OpenWeatherMapTool  # ✅ Updated Import
from crewai_tools import SerperDevTool       # For researcher agent

def load_agents(yaml_file='src/mycrewaiproject/config/agents.yaml'):
    with open(yaml_file, 'r') as file:
        agents_data = yaml.safe_load(file)

    # ✅ Instantiate your tools
    weather_tool = OpenWeatherMapTool()
    search_tool = SerperDevTool()

    agents = {}
    for key, data in agents_data.items():
        # Assign correct tools to each agent
        if key == 'weather_fetcher':
            tools = [weather_tool]
        elif key == 'weather_researcher':
            tools = [search_tool]  # Researcher uses SerperDevTool
        else:
            tools = []  # Report writer agent has no external tools

        agents[key] = Agent(
            role=data['role'],
            goal=data['goal'],
            backstory=data['backstory'],
            tools=tools,  # ✅ Correct tool assigned dynamically
            verbose=True,
            memory=True
        )
    return agents


def load_tasks(agents, yaml_file='src/mycrewaiproject/config/tasks.yaml'):
    with open(yaml_file, 'r') as file:
        tasks_data = yaml.safe_load(file)

    tasks = []
    for key, data in tasks_data.items():
        agent_key = (
            'weather_fetcher' if 'fetch_weather' in key else
            'weather_researcher' if 'research' in key else
            'weather_report_writer'
        )
        tasks.append(Task(
            description=data['description'],
            expected_output=data['expected_output'],
            agent=agents[agent_key],
            output_file=None
        ))
    return tasks


def create_crew():
    agents = load_agents()
    tasks = load_tasks(agents)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential
    )
    return crew
