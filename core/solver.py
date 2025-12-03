import yaml
from utils.ai_client import (
    deepseek_choice,
    deepseek_answer_text,
    deepseek_answer_blank
)

with open("config/config.yaml") as f:
    cfg = yaml.safe_load(f)

KEY = cfg["DEEPSEEK_KEY"]


def solve(question, options):
    return deepseek_choice(KEY, question, options)


def solve_text(question):
    return deepseek_answer_text(KEY, question)


def solve_blank(question):
    return deepseek_answer_blank(KEY, question)