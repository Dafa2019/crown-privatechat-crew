"""Crown PrivateChat Crew - Signal-grade privacy on Tencent Cloud IM"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, FileReadTool, CodeInterpreterTool


@CrewBase
class PrivateChatCrew():
    """Crown PrivateChat - Privacy Enhancement Team"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Agents ──

    @agent
    def product_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['product_lead'],
            llm="anthropic/claude-sonnet-4-6",
            tools=[SerperDevTool()],
            allow_delegation=True,
            memory=True,
            verbose=True,
            max_iter=25,
        )

    @agent
    def privacy_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['privacy_engineer'],
            llm="anthropic/claude-sonnet-4-6",
            tools=[FileReadTool(), CodeInterpreterTool()],
            memory=True,
            verbose=True,
        )

    @agent
    def flutter_dev(self) -> Agent:
        return Agent(
            config=self.agents_config['flutter_dev'],
            llm="anthropic/claude-sonnet-4-6",
            tools=[FileReadTool(), CodeInterpreterTool()],
            memory=True,
            verbose=True,
        )

    @agent
    def security_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['security_auditor'],
            llm="anthropic/claude-sonnet-4-6",
            tools=[FileReadTool(), CodeInterpreterTool()],
            verbose=True,
        )

    @agent
    def qa_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_tester'],
            llm="anthropic/claude-sonnet-4-6",
            tools=[FileReadTool(), CodeInterpreterTool()],
            verbose=True,
        )

    # ── Tasks ──

    @task
    def privacy_feature_spec(self) -> Task:
        return Task(config=self.tasks_config['privacy_feature_spec'])

    @task
    def privacy_architecture(self) -> Task:
        return Task(config=self.tasks_config['privacy_architecture'])

    @task
    def flutter_implementation(self) -> Task:
        return Task(config=self.tasks_config['flutter_implementation'])

    @task
    def security_audit(self) -> Task:
        return Task(config=self.tasks_config['security_audit'])

    @task
    def privacy_qa_testing(self) -> Task:
        return Task(config=self.tasks_config['privacy_qa_testing'])

    # ── Crew ──

    @crew
    def crew(self) -> Crew:
        # Product Lead is manager, not in workers list
        workers = [
            a for a in self.agents
            if a.role != self.product_lead().role
        ]
        return Crew(
            agents=workers,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.product_lead(),
            planning=True,
            memory=True,
            verbose=True,
        )
