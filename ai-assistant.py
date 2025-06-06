!/usr/bin/env python3.12

import os
import sys
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


console = Console()


if "GEMINI_API_KEY" not in os.environ:
    sys.exit("❌ GEMINI_API_KEY not set in environment variables!")


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
chat = client.chats.create(model="gemini-2.0-flash")

def stream_response(user_input: str) -> str:
    """Streams response silently and returns full text for markdown rendering."""
    response_stream = chat.send_message_stream(user_input)
    full_text = ""
    for chunk in response_stream:
        full_text += chunk.text
    return full_text

def main():
    try:
        if len(sys.argv) > 1:
            user_input = " ".join(sys.argv[1:])
            console.print(f"[bold yellow]🤔 : {user_input}[/bold yellow]")
            with console.status("🤖 Thinking...", spinner="dots"):
                full_text = stream_response(user_input)
            console.print(Panel(Markdown(full_text), style="cyan"))

        while True:
            try:
                user_input = input("🤔 : ").strip()
                if not user_input:
                    continue
                if user_input.lower() in {"exit", "quit", "bye"}:
                    print("👋 Goodbye!")
                    break

                with console.status("🤖 Thinking...", spinner="dots"):
                    full_text = stream_response(user_input)
                console.print(Panel(Markdown(full_text), style="cyan"))

            except (KeyboardInterrupt, EOFError):
                print("\n👋 Goodbye!")
                break
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
