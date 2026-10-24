import os
import ast
import operator
import traceback
from pathlib import Path
from datetime import datetime
from pydantic_ai import Agent
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GAPGPT_API_KEY")
BASE_URL = os.getenv("GAPGPT_BASE_URL", "https://api.gapgpt.app/v1")
MODEL_NAME = os.getenv("GAPGPT_MODEL", "gapgpt-qwen-3.5")

if not API_KEY:
    raise RuntimeError(
        "GAPGPT_API_KEY was not found. Check that your .env file is next to this script."
    )

provider = OpenAIProvider(
    base_url=BASE_URL,
    api_key=API_KEY,
)

model = OpenAIChatModel(
    model_name=MODEL_NAME,
    provider=provider,
)

NOTES_FILE = BASE_DIR / "notes.txt"


def get_current_time() -> str:
    """Get the current local date and time."""
    return datetime.now().astimezone().strftime("%A, %B %d, %Y at %I:%M %p %Z")


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_math(node):
    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator.")
        return op(evaluate_math(node.left), evaluate_math(node.right))

    if isinstance(node, ast.UnaryOp):
        op = OPERATORS.get(type(node.op))
        if op is None:
            raise ValueError("Unsupported operator.")
        return op(evaluate_math(node.operand))

    raise ValueError("Invalid math expression.")


def calculate(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(evaluate_math(tree.body))
    except Exception as error:
        return f"Error: {error}"


def save_note(note: str) -> str:
    """Save a note for later."""
    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(f"- {note}\n")
    return "Note saved."


def read_notes() -> str:
    """Read previously saved notes."""
    if not NOTES_FILE.exists():
        return "No notes saved yet."
    return NOTES_FILE.read_text(encoding="utf-8")


agent = Agent(
    model,
    tools=[
        get_current_time,
        calculate,
        save_note,
        read_notes,
    ],
    instructions=(
        "You are a helpful personal assistant. "
        "Answer in Persian unless the user asks for another language. "
        "Use get_current_time for questions about the current time. "
        "Use calculate for arithmetic questions. "
        "Use save_note when the user asks to remember something. "
        "Use read_notes when asked about saved notes. "
        "Keep answers short and friendly."
    ),
)


def main():
    print(f"GapGPT agent ready! Model: {MODEL_NAME}")
    print("Type 'quit' to exit.\n")

    history = []

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ("quit", "exit"):
                print("Goodbye!")
                break

            if not user_input:
                continue

            result = agent.run_sync(
                user_input,
                message_history=history,
            )

            history = result.all_messages()
            print(f"\nAgent: {result.output}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
