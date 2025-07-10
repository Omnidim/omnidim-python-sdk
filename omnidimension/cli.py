"""
omnidim cli — terminal interface to manage your omnidimension agents

- built using typer + rich  
- needs OMNIDIMENSION_API_KEY (env var)  
- works with the official omnidimension sdk

features:
- list agents with pagination
- get agent details by id
- create agents with name, welcome message, and context
- update agents with raw json
- delete agents instantly

usage:
    export OMNIDIMENSION_API_KEY=your_key_here

    # basic commands
    omnidim list-agents
    omnidim get-agent AGENT_ID
    omnidim create-agent -n "Echo" -w "hello" -c "this is a test agent"
    omnidim update-agent AGENT_ID -d '{"name": "new name"}'
    omnidim delete-agent AGENT_ID

dev notes:
- this file only touches: env, sdk client, api
- no state is stored locally
- for one-shot terminal workflows (｡•̀ᴗ-)✧

"""

import typer
import json
import os
from rich.console import Console
from rich.table import Table
from omnidimension.client import Client

app = typer.Typer(help="omnidimension cli — manage agents and more")
console = Console()

def get_client():
    api_key = os.getenv("OMNIDIMENSION_API_KEY")

    if not api_key:
        console.print(
            "[bold red]OMNIDIMENSION_API_KEY not found.[/bold red]\n"
            "you can generate one here: [cyan underline]https://www.omnidim.io/api[/cyan underline]"
        )
        api_key = typer.prompt("please paste your API key")
        if not api_key.strip():
            console.print("[bold red]no API key provided. exiting.[/bold red]")
            raise typer.Exit()

        # ~ persist for this session
        os.environ["OMNIDIMENSION_API_KEY"] = api_key
        console.print(
            f"[green]✔ api key set for this session[/green]\n"
            f"to persist it, run:\n[cyan]export OMNIDIMENSION_API_KEY={api_key}[/cyan]"
        )
    return Client(api_key)

@app.command("list-agents")
def list_agents(page: int = 1, page_size: int = 10):
    """
    list all agents with pagination
    """
    client = get_client()
    result = client.agent.list(page=page, page_size=page_size)

    agent_list = result.get("json", {}).get("bots", [])
    if not agent_list:
        console.print("[yellow]no agents found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Welcome Message", overflow="fold")

    for agent in agent_list:
        table.add_row(
            str(agent.get("id", "")),
            agent.get("name", ""),
            agent.get("welcome_message", "")
        )

    console.print(table)



@app.command("get-agent")
def get_agent(agent_id: str):
    """
    get details of an agent by id
    """
    client = get_client()
    agent = client.agent.get(agent_id)
    console.print_json(data=agent)


@app.command("create-agent")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="name of the agent"),
    welcome: str = typer.Option(..., "--welcome", "-w", help="welcome message"),
    context: str = typer.Option(..., "--context", "-c", help="context JSON or text"),
):
    """
    create a new agent with minimal config
    """
    try:
        context_breakdown = json.loads(context)
        if not isinstance(context_breakdown, list):
            raise ValueError
    except Exception:
        context_breakdown = [{"title": "Purpose", "body": context}]

    client = get_client()
    response = client.agent.create(
        name=name,
        welcome_message=welcome,
        context_breakdown=context_breakdown
    )
    console.print(f"[bold green]✓ created agent:[/bold green] {response}")


@app.command("update-agent")
def update_agent(agent_id: str, update_json: str = typer.Option(..., "--data", "-d", help="json string with update data")):
    """
    update an agent using a JSON string
    """
    try:
        data = json.loads(update_json)
    except Exception as e:
        console.print(f"[red]invalid json: {e}[/red]")
        raise typer.Exit()

    client = get_client()
    result = client.agent.update(agent_id, data)
    console.print(f"[bold cyan]✓ updated agent:[/bold cyan] {result}")


@app.command("delete-agent")
def delete_agent(agent_id: str):
    """
    delete an agent by id
    """
    client = get_client()
    result = client.agent.delete(agent_id)
    console.print(f"[bold red]✓ deleted agent:[/bold red] {result}")


if __name__ == "__main__":
    app()
