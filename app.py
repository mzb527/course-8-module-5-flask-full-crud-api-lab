from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find event by ID
def find_event(event_id):
    return next((event for event in events if event.id == event_id), None)

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400

    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201  # Return created resource with status 201

# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Missing title"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200  # Return updated resource with status 200

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != event_id]
    return jsonify({"message": "Event deleted"}), 204  # Return success status with no content

if __name__ == "__main__":
    app.run(debug=True)