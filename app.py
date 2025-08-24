from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime
from reviewer import review_snippet

app = Flask(__name__)

SNIPPETS_FILE = "snippets.json"

def load_snippets():
    """Load snippets from JSON file"""
    if os.path.exists(SNIPPETS_FILE):
        with open(SNIPPETS_FILE, 'r') as f:
            return json.load(f)
    return {"snippets": []}

def save_snippets(snippets_data):
    """Save snippets to JSON file"""
    with open(SNIPPETS_FILE, 'w') as f:
        json.dump(snippets_data, f, indent=2)

@app.route('/')
def index():
    """Main page with snippet management"""
    snippets_data = load_snippets()
    return render_template('index.html', snippets=snippets_data['snippets'])

@app.route('/add_snippet', methods=['POST'])
def add_snippet():
    """Add a new snippet from form data"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['filename', 'language', 'content']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Load existing snippets
        snippets_data = load_snippets()
        
        # Generate new ID
        new_id = max([s['id'] for s in snippets_data['snippets']], default=0) + 1
        
        # Create new snippet
        new_snippet = {
            'id': new_id,
            'filename': data['filename'],
            'language': data['language'],
            'content': data['content'].split('\n') if isinstance(data['content'], str) else data['content']
        }
        
        # Add to snippets
        snippets_data['snippets'].append(new_snippet)
        save_snippets(snippets_data)
        
        return jsonify({'success': True, 'snippet': new_snippet})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_snippet/<int:snippet_id>', methods=['DELETE'])
def delete_snippet(snippet_id):
    """Delete a snippet by ID"""
    try:
        snippets_data = load_snippets()
        snippets_data['snippets'] = [s for s in snippets_data['snippets'] if s['id'] != snippet_id]
        save_snippets(snippets_data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run_review')
def run_review():
    """Run code review on all snippets"""
    try:
        snippets_data = load_snippets()
        results = []
        
        for snippet in snippets_data['snippets']:
            review = review_snippet(snippet)
            results.append({
                'id': snippet['id'],
                'filename': snippet['filename'],
                'language': snippet.get('language', ''),
                'code': '\n'.join(snippet['content']),
                'review': review
            })
        
        # Save results
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        os.makedirs('output', exist_ok=True)
        with open('output/review_results.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/view_results')
def view_results():
    """View review results"""
    try:
        if os.path.exists('output/review_results.json'):
            with open('output/review_results.json', 'r') as f:
                results = json.load(f)
            return render_template('results.html', results=results)
        else:
            return render_template('results.html', results=None)
    except Exception as e:
        return render_template('results.html', results=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
