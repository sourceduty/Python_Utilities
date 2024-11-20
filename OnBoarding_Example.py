from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()

def display_welcome_message():
    console.print(Panel("Welcome to Sourceduty!", style="bold green"))
    console.print(
        "[bold cyan]Sourceduty is excited to have you join us! Let's get started with your onboarding process.[/bold cyan]\n"
    )

def collect_user_info():
    console.print(Panel("[bold magenta]Step 1: Collecting Your Information[/bold magenta]"))
    name = Prompt.ask("[green]What is your full name?[/green]")
    email = Prompt.ask("[green]What is your email address?[/green]")
    department = Prompt.ask("[green]Which department will you be joining?[/green]", choices=["Art", "Tech", "Community", "Innovation"], default="Art")
    return name, email, department

def display_policies_and_acknowledge():
    console.print(Panel("[bold magenta]Step 2: Review Company Policies[/bold magenta]"))
    console.print("[yellow]Please review the key company policies below:[/yellow]\n")
    policies = [
        "1. Maintain ethical and sustainable practices.",
        "2. Respect your teammates and their contributions.",
        "3. Innovate with a forward-thinking mindset.",
        "4. Protect company assets and intellectual property.",
        "5. Strive for excellence in your role."
    ]
    for policy in policies:
        console.print(f"[cyan]{policy}[/cyan]")
    acknowledgment = Confirm.ask("[green]Do you acknowledge and agree to the policies listed above?[/green]")
    return acknowledgment

def setup_initial_tasks(department):
    console.print(Panel("[bold magenta]Step 3: Initial Tasks Setup[/bold magenta]"))
    tasks = {
        "Art": ["Review brand style guidelines.", "Complete your first art assignment."],
        "Tech": ["Set up development environment.", "Review coding standards and repo access."],
        "Community": ["Read community engagement guidelines.", "Introduce yourself in the community forum."],
        "Innovation": ["Familiarize yourself with ongoing projects.", "Brainstorm one new idea to discuss with the team."]
    }
    selected_tasks = tasks.get(department, [])
    console.print("[yellow]Here are your initial tasks based on your department:[/yellow]\n")
    for task in selected_tasks:
        console.print(f"[cyan]- {task}[/cyan]")
    confirmation = Confirm.ask("[green]Are you ready to start on these tasks?[/green]")
    return confirmation

def main():
    display_welcome_message()
    
    # Step 1: Collect user information
    name, email, department = collect_user_info()
    
    # Step 2: Display policies and get acknowledgment
    acknowledgment = display_policies_and_acknowledge()
    if not acknowledgment:
        console.print("[red]You need to agree to the policies to proceed with onboarding.[/red]")
        return
    
    # Step 3: Setup initial tasks
    ready = setup_initial_tasks(department)
    if not ready:
        console.print("[red]Please review the tasks and prepare before continuing onboarding.[/red]")
        return
    
    # Completion Message
    console.print(
        Panel(
            f"[bold green]Welcome to Sourceduty, {name}![/bold green]\n\n"
            f"[blue]We're thrilled to have you join our [bold]{department}[/bold] department. "
            "Check your email ([bold]{email}[/bold]) for further instructions.[/blue]",
            style="bold magenta"
        )
    )

if __name__ == "__main__":
    main()
