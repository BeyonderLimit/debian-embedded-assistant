#!/usr/bin/env python3
# src/main.py
import sys
import os
from rich.console import Console
from src.text_input import get_text_input
from src.voice_input import VoiceInput
from src.tts import TextToSpeech
from src.task_manager import add_task, show_tasks
from src.app_launcher import launch_app
from src.ui import print_header, print_weather, print_system_status, print_menu

console = Console()

def main():
    """Main application loop"""
    # Initialize voice input and TTS
    voice = VoiceInput(model_size="tiny")
    tts = TextToSpeech()

    # Print startup info
    print_header()
    print_weather()
    print_system_status()
    print_menu()

    console.print("\n[bold green]🚀 Assistant ready! Type 'help' for commands.[/bold green]\n")
    tts.speak("Assistant ready")

    while True:
        try:
            command = get_text_input()

            if not command:
                continue

            cmd_lower = command.lower().strip()

            # Handle commands
            if cmd_lower == "exit" or cmd_lower == "quit":
                console.print("[green]👋 Goodbye![/green]")
                tts.speak("Goodbye")
                break

            elif cmd_lower == "dictation" or cmd_lower == "voice":
                text = voice.get_voice_input()
                if text:
                    add_task(text)
                    tts.speak(f"Task added: {text}")

            elif cmd_lower == "show tasks":
                show_tasks()

            elif cmd_lower.startswith("add task "):
                task_text = command[9:].strip()
                if task_text:
                    add_task(task_text)
                    tts.speak("Task added")
                else:
                    console.print("[yellow]⚠️ Please provide task text[/yellow]")

            elif cmd_lower == "weather":
                print_weather()

            elif cmd_lower == "status":
                print_system_status()

            elif cmd_lower == "help":
                print_menu()

            elif cmd_lower.startswith("say "):
                # Test TTS
                text_to_speak = command[4:].strip()
                if text_to_speak:
                    tts.speak(text_to_speak)
                else:
                    console.print("[yellow]⚠️ Provide text to speak (e.g., 'say hello')[/yellow]")

            elif cmd_lower == "test piper":
                # Force test Piper
                console.print("[cyan]Testing Piper TTS specifically...[/cyan]")
                tts.speak("This is a test of the Piper text to speech engine", force_engine='piper')

            elif cmd_lower == "test espeak":
                # Force test espeak
                console.print("[cyan]Testing espeak TTS specifically...[/cyan]")
                tts.speak("This is a test of the espeak text to speech engine", force_engine='espeak')

            elif cmd_lower == "download voice":
                # Download Piper model
                tts.list_available_models()
                console.print("[cyan]Enter model name (or 'list' to see options again):[/cyan]")
                model = input("Model: ").strip()
                if model and model.lower() != 'list':
                    tts.download_model(model)
                elif model.lower() == 'list':
                    tts.list_available_models()

            elif cmd_lower in ["volume up", "volume down", "mute", "unmute",
                              "brightness up", "brightness down", "notes", 
                              "calendar", "search"]:
                launch_app(command)

            else:
                console.print(f"[yellow]⚠️ Unknown command: {command}[/yellow]")
                console.print("[dim]Type 'help' to see available commands[/dim]")

        except KeyboardInterrupt:
            console.print("\n[yellow]⚠️ Interrupted. Type 'exit' to quit.[/yellow]")
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

if __name__ == "__main__":
    main()
