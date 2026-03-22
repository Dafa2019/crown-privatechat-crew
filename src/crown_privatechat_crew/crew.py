"""Crown PrivateChat Crew v2.0 - Signal-grade Privacy on Tencent Cloud IM"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class CrownPrivateChatCrew():
    """PrivateChat Crew - 4 Workers with auto manager"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # ── Worker Agents ──

    @agent
    def privacy_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['privacy_engineer'],
            llm="anthropic/claude-sonnet-4-6",
            verbose=True,
        )

    @agent
    def flutter_dev(self) -> Agent:
        return Agent(
            config=self.agents_config['flutter_dev'],
            llm="anthropic/claude-sonnet-4-6",
            verbose=True,
        )

    @agent
    def security_auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['security_auditor'],
            llm="openai/gpt-4o",
            verbose=True,
        )

    @agent
    def qa_tester(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_tester'],
            llm="openai/gpt-4o",
            verbose=True,
        )

    # ── Tasks ──

    @task
    def privacy_feature_spec(self) -> Task:
        return Task(config=self.tasks_config['privacy_feature_spec'])

    @task
    def implement_privacy_features(self) -> Task:
        return Task(config=self.tasks_config['implement_privacy_features'])

    @task
    def implement_advanced_privacy(self) -> Task:
        return Task(config=self.tasks_config['implement_advanced_privacy'])

    @task
    def security_hardening(self) -> Task:
        return Task(config=self.tasks_config['security_hardening'])

    @task
    def privacy_testing(self) -> Task:
        return Task(config=self.tasks_config['privacy_testing'])

    # ── Crew ──

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_llm="anthropic/claude-sonnet-4-6",
            planning=True,
            memory=True,
            verbose=True,
        )
