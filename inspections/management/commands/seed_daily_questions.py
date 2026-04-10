from django.core.management.base import BaseCommand
from inspections.models import DailyQuestion


SITE_SUPERVISOR_QUESTIONS = [
    {
        "question_text": "A tenant reports a burst pipe flooding the basement at 7pm. What is your FIRST action?",
        "option_a": "Call your PC to report",
        "option_b": "Isolate the water supply and contain the flood",
        "option_c": "Log it in the system for morning",
        "option_d": "Wait for the plumber to arrive",
        "correct_option": "B",
        "explanation": "Emergency issues require immediate containment before reporting.",
    },
    {
        "question_text": "What is the maximum time allowed for acknowledging a tenant complaint?",
        "option_a": "1 hour",
        "option_b": "Same day",
        "option_c": "30 minutes",
        "option_d": "Next working day",
        "correct_option": "C",
        "explanation": "The target acknowledgement time is within 30 minutes.",
    },
    {
        "question_text": "A contractor arrives on site without an LPO. What do you do?",
        "option_a": "Let them start and sort paperwork later",
        "option_b": "Refuse to allow work to commence",
        "option_c": "Call procurement for a quick verbal approval",
        "option_d": "Ask them for their own contractor documentation",
        "correct_option": "B",
        "explanation": "No LPO means no work should start.",
    },
    {
        "question_text": "During a fire emergency, what is your first priority?",
        "option_a": "Saving equipment",
        "option_b": "Calling the fire department",
        "option_c": "Ensuring safe evacuation of all occupants",
        "option_d": "Securing the building perimeter",
        "correct_option": "C",
        "explanation": "Life safety comes first in a fire emergency.",
    },
    {
        "question_text": "A contractor offers you a small gift for giving them work. What should you do?",
        "option_a": "Accept it because it is small",
        "option_b": "Decline and report it to your AM",
        "option_c": "Accept it privately",
        "option_d": "Ask for a better gift",
        "correct_option": "B",
        "explanation": "Gifts from vendors are a conflict and must be reported.",
    },
]

ASSET_MANAGER_QUESTIONS = [
    {
        "question_text": "Your portfolio has 3 sites scoring below 70. According to the RAG system, these sites are:",
        "option_a": "Amber",
        "option_b": "Red",
        "option_c": "Green",
        "option_d": "Not a concern until next quarter",
        "correct_option": "B",
        "explanation": "Sites below 70 are classed as red and require intervention.",
    },
    {
        "question_text": "For a non-rate card job valued at KES 300,000, how many quotes are needed?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "3",
        "option_d": "None",
        "correct_option": "B",
        "explanation": "Jobs in that band require two quotes.",
    },
    {
        "question_text": "A Site Supervisor says an issue was handled but there is no documentation. What should you do?",
        "option_a": "Accept their word",
        "option_b": "Require documented evidence",
        "option_c": "Document it yourself afterwards",
        "option_d": "Ask the tenant to confirm verbally",
        "correct_option": "B",
        "explanation": "Undocumented work is treated as unverified work.",
    },
    {
        "question_text": "Finance and Procurement are:",
        "option_a": "Line managers to FM",
        "option_b": "Control functions, not line managers",
        "option_c": "Subordinate to FM",
        "option_d": "Optional support functions",
        "correct_option": "B",
        "explanation": "They are control functions in the operating model.",
    },
    {
        "question_text": "The FM principle 'discipline beats heroics' means:",
        "option_a": "Strict punishment for mistakes",
        "option_b": "Consistent process execution beats firefighting",
        "option_c": "Never take initiative",
        "option_d": "Only follow rules without thinking",
        "correct_option": "B",
        "explanation": "Strong systems and consistency outperform one-off heroics.",
    },
]


class Command(BaseCommand):
    help = "Seed starter daily knowledge questions"

    def handle(self, *args, **options):
        created = 0
        for row in SITE_SUPERVISOR_QUESTIONS:
            _, was_created = DailyQuestion.objects.get_or_create(
                role="site_supervisor",
                question_text=row["question_text"],
                defaults=row,
            )
            created += int(was_created)

        for row in ASSET_MANAGER_QUESTIONS:
            _, was_created = DailyQuestion.objects.get_or_create(
                role="asset_manager",
                question_text=row["question_text"],
                defaults=row,
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} question(s)."))
