from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'checklist.json')

click_count = 0

# ── helpers ──────────────────────────────────────────────────────────────────

def load_checklist():
    """Load checklist state from disk. Returns a dict of {item_id: bool}."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_checklist(data):
    """Persist checklist state to disk."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ── routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main business plan page."""
    checklist = load_checklist()
    return render_template('index.html', checklist=checklist)


@app.route('/api/checklist', methods=['GET'])
def get_checklist():
    """Return current checklist state as JSON."""
    return jsonify(load_checklist())


@app.route('/api/checklist', methods=['POST'])
def update_checklist():
    """
    Toggle a single checklist item.
    Expects JSON body: { "id": "item_id", "done": true/false }
    """
    body = request.get_json(silent=True)

    global click_count
    click_count += 1

    if not body or 'id' not in body:
        return jsonify({'error': 'Missing item id'}), 400

    checklist = load_checklist()
    item_id = body['id']
    checklist[item_id] = bool(body.get('done', False))

    print(f"[LOG] Checklist updated: {item_id} -> {checklist[item_id]}")

    save_checklist(checklist)

    return jsonify({'success': True, 'id': item_id, 'done': checklist[item_id]})


@app.route('/api/checklist/reset', methods=['POST'])
def reset_checklist():
    """Reset all checklist items to unchecked."""
    save_checklist({})
    return jsonify({'success': True, 'message': 'Checklist reset'})


@app.route('/api/checklist/stats', methods=['GET'])
def checklist_stats():
    """Return completion stats for the checklist."""
    checklist = load_checklist()
    total = len(checklist)
    done  = sum(1 for v in checklist.values() if v)
    return jsonify({
        'total_tracked': total,
        'done': done,
        'pending': total - done,
        'percent': round((done / total * 100) if total else 0, 1)
    })


@app.route('/api/tab/<tab_name>', methods=['GET'])
def get_tab(tab_name):
    """
    Lightweight endpoint — confirms a tab exists and returns its name.
    The actual tab content is already in the HTML; this just lets the
    frontend log navigation events server-side if needed.
    """
    valid_tabs = ['overview', 'offer', 'leads', 'outreach',
                  'revenue', 'execution', 'stress', 'coldcall']
    if tab_name not in valid_tabs:
        return jsonify({'error': 'Unknown tab'}), 404
    return jsonify({'tab': tab_name, 'status': 'ok'})

@app.route('/health')
def health():
    """Simple health check endpoint."""
    return jsonify({"status": "server running"})

@app.route('/api/clicks')
def clicks():
    return jsonify({"clicks": click_count})


# ── run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
