#!/usr/bin/env python3
"""
Win My Argument - Political Debate Comparison Tool
Main entry point for the TUI application
"""

from debater.debate.service import make_debate, DebateStats
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box
from rich.layout import Layout
import sys

# Initialize Rich console
console = Console()

# Predefined debate topics
PREDEFINED_TOPICS = [
    "Climate change and environmental policy",
    "Universal healthcare systems",
    "Immigration and border control",
    "Gun control and Second Amendment rights",
    "Education reform and school funding",
    "Tax policy and wealth distribution",
    "Criminal justice reform",
    "Energy production and fossil fuels",
    "Free speech and social media regulation",
    "Economic stimulus and inflation control",
]


def display_welcome():
    """Display welcome screen"""
    welcome_text = Text("🗣️  WIN MY ARGUMENT", style="bold cyan", justify="center")
    console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))
    console.print(
        Text("Political Debate Comparison Tool", style="dim italic", justify="center"),
        end="\n\n",
    )


def display_input_menu():
    """Display menu for selecting how to input debate topic"""
    console.print(
        Panel(
            Text("How would you like to enter a debate topic?", style="bold white"),
            border_style="yellow",
        )
    )

    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    table.add_row("[1]", "Type your own topic")
    table.add_row("[2]", "Select from predefined topics")
    table.add_row("[3]", "Exit")

    console.print(table, end="\n\n")


def display_predefined_topics():
    """Display predefined topics for selection"""
    console.print(
        Panel(
            Text("Select a predefined debate topic:", style="bold white"),
            border_style="green",
        )
    )

    table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    for idx, topic in enumerate(PREDEFINED_TOPICS, 1):
        table.add_row(f"[{idx}]", topic)
    table.add_row(f"[{len(PREDEFINED_TOPICS) + 1}]", "Back to menu")

    console.print(table, end="\n\n")


def get_topic_input():
    """Get debate topic from user"""
    display_input_menu()

    choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")
    console.print()

    if choice == "1":
        topic = Prompt.ask("Enter your debate topic", default="Healthcare policy")
        return topic

    elif choice == "2":
        while True:
            display_predefined_topics()
            topic_choice = Prompt.ask(
                "Select a topic",
                choices=[str(i) for i in range(1, len(PREDEFINED_TOPICS) + 2)],
                default="1",
            )
            console.print()

            if topic_choice == str(len(PREDEFINED_TOPICS) + 1):
                continue

            return PREDEFINED_TOPICS[int(topic_choice) - 1]

    else:
        console.print("[red]Exiting...[/red]")
        sys.exit(0)


def display_stats_table(stats: DebateStats) -> Table:
    """Create a stats table for a side"""
    table = Table(box=box.ROUNDED, padding=(0, 1))
    table.add_row("[bold]Metric[/bold]", "[bold]Value[/bold]")
    table.add_row("Total Tokens", str(stats.total_tokens))
    table.add_row("Input Tokens", str(stats.input_tokens))
    table.add_row("Output Tokens", str(stats.output_tokens))
    table.add_row("Tokens/sec", f"{stats.tokens_per_second:.2f}")
    table.add_row("Response Time", f"{stats.response_time:.2f}s")
    return table


def display_split_pane(result: list, stats: dict):
    """Display debate results in a side-by-side split pane"""
    right_msg = result[0]
    left_msg = result[1]

    console.print()
    console.print(
        Panel(
            Text("⚖️  DEBATE COMPARISON", style="bold magenta"), border_style="magenta"
        )
    )
    console.print()

    # Create layout with three sections: header, content, stats
    layout = Layout()
    layout.split_column(
        Layout(name="header"),
        Layout(name="content"),
        Layout(name="stats"),
    )

    # Header with topic
    layout["header"].update(
        Panel(
            Text(
                "Side-by-Side Argument Comparison", style="bold cyan", justify="center"
            ),
            border_style="cyan",
            padding=(0, 1),
        )
    )

    # Split content into left and right
    layout["content"].split_row(
        Layout(name="right"),
        Layout(name="left"),
    )

    # Right-wing panel
    right_panel = Panel(
        Text(right_msg["message"], style="white", justify="left"),
        title="🔴 " + right_msg["agent"],
        border_style="red",
        title_align="left",
        padding=(1, 2),
    )
    layout["right"].update(right_panel)

    # Left-wing panel
    left_panel = Panel(
        Text(left_msg["message"], style="white", justify="left"),
        title="🔵 " + left_msg["agent"],
        border_style="cyan",
        title_align="left",
        padding=(1, 2),
    )
    layout["left"].update(left_panel)

    # Split stats into left and right
    layout["stats"].split_row(
        Layout(name="right_stats"),
        Layout(name="left_stats"),
    )

    right_stats_table = display_stats_table(stats["right"])
    left_stats_table = display_stats_table(stats["left"])

    right_stats_panel = Panel(
        right_stats_table,
        title="📊 Right-Wing Stats",
        border_style="red",
        title_align="left",
    )
    layout["right_stats"].update(right_stats_panel)

    left_stats_panel = Panel(
        left_stats_table,
        title="📊 Left-Wing Stats",
        border_style="cyan",
        title_align="left",
    )
    layout["left_stats"].update(left_stats_panel)

    # Print the layout
    console.print(layout)


async def run_debate(topic: str):
    """Run the debate with the given topic"""
    console.print("[cyan]Generating debate arguments...[/cyan]")

    try:
        result, stats = await make_debate(query=topic)
        display_split_pane(result, stats)
        return result
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        return None


async def main():
    """Main TUI application"""
    display_welcome()
    console.print()

    while True:
        try:
            # Get topic from user
            topic = get_topic_input()

            # Run debate
            result = await run_debate(topic)

            if result is None:
                continue

            # Ask if user wants to continue
            continue_choice = Prompt.ask(
                "\nRun another debate?", choices=["yes", "no"], default="yes"
            )

            if continue_choice.lower() != "yes":
                console.print("[cyan]Thank you for using Win My Argument![/cyan]")
                break

            console.print("\n" + "=" * 80 + "\n")

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")
            break


if __name__ == "__main__":
    load_dotenv()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
