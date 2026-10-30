"""Simple in-memory support ticket tracker."""
import json
import logging

TICKETS = {}
AUDIT_LOG = []


def create_ticket(title, description, reporter,
                  priority="medium", category="general"):
    """Create a ticket and store it. Returns None if title is empty."""
    if not title:
        return None
    ticket_id = str(len(TICKETS) + 1)
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "open",
        "reporter": reporter,
        "assignee": None,
    }
    TICKETS[ticket_id] = ticket
    AUDIT_LOG.append(f"Created ticket {ticket_id} for {reporter}")
    return ticket


def assign_ticket(ticket_id, agent):
    """Assign a ticket to an agent. Returns True on success."""
    try:
        TICKETS[ticket_id]["assignee"] = agent
        return True
    except KeyError:
        logging.warning("Ticket %s not found", ticket_id)
        return False


def update_status(ticket_id, status):
    """Update the status of a ticket and return the ticket."""
    TICKETS[ticket_id]["status"] = status
    return TICKETS[ticket_id]


def search_tickets(status=None, priority=None):
    """Return tickets matching the given status and priority."""
    results = []
    for ticket in TICKETS.values():
        if status is not None and ticket["status"] != status:
            continue
        if priority and ticket["priority"] != priority:
            continue
        results.append(ticket)
    return results


def save_tickets(path="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(json.dumps(TICKETS))


def load_tickets(path="tickets.json"):
    """Load tickets from a JSON file, replacing the current tickets."""
    with open(path, "r", encoding="utf-8") as file:
        loaded = json.loads(file.read())
    TICKETS.clear()
    TICKETS.update(loaded)


def print_ticket_report():
    """Print a simple report of all tickets."""
    print("Support Tickets")
    if not TICKETS:
        print("No tickets yet")
    for ticket_id, ticket in TICKETS.items():
        print(ticket_id, ticket["title"], ticket["status"])


def close_ticket(ticket_id):
    """Mark a ticket as closed."""
    TICKETS[ticket_id]["status"] = "closed"


def is_open(ticket_id):
    """Return True if the ticket is open or in progress."""
    return TICKETS[ticket_id]["status"] in ("open", "in_progress")


def main():
    """Run a small demo of the ticket tracker."""
    logging.basicConfig(level=logging.INFO)
    create_ticket(
        "Cannot sign in", "Password reset link fails", "alex@example.com"
    )
    create_ticket(
        "Billing question", "Charged twice", "lee@example.com", "high"
    )
    assign_ticket("1", "agent-01")
    update_status("1", "in_progress")
    print_ticket_report()
    logging.info("Tickets created: %d", len(TICKETS))
    print("Ticket 1 open?", is_open("1"))
    ticket_id = input("Ticket id to close (Enter to skip): ")
    if ticket_id:
        close_ticket(ticket_id)
    save_tickets()


if __name__ == "__main__":
    main()