#!/usr/bin/env python3
"""Crown PrivateChat Crew - Entry Point"""
import sys
from crown_privatechat_crew.crew import CrownPrivateChatCrew


def run():
    inputs = {
        'project_description': (
            sys.argv[1] if len(sys.argv) > 1
            else 'Enhance existing PrivateChat Flutter app (80% complete, Tencent Cloud IM) '
                 'with 2026 Signal-grade privacy features: disappearing messages, screenshot '
                 'protection, sealed sender, incognito keyboard, encrypted backup, and '
                 'per-conversation privacy controls. Target: top-tier private messaging app '
                 'competing with Signal, Threema, and Session.'
        )
    }
    CrownPrivateChatCrew().crew().kickoff(inputs=inputs)


if __name__ == '__main__':
    run()
