#!/usr/bin/env python
"""Crown PrivateChat Crew - Entry Point"""
from privatechat_crew.crew import PrivateChatCrew


def run():
    PrivateChatCrew().crew().kickoff()


if __name__ == "__main__":
    run()
