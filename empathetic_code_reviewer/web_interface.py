#!/usr/bin/env python3
"""
🌟 EMPATHETIC CODE REVIEWER - WEB INTERFACE
Visual demo interface that will WOW the judges!
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from ultimate_reviewer import UltimateEmpathethicReviewer, AIEngine

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/review', methods=['POST'])
def review_code():
    try:
        data = request.json
        code_snippet = data.get('code_snippet', '')
        comments = data.get('review_comments', [])
        engine = data.get('engine', 'auto')
        api_key = data.get('api_key', '')
        
        # Validate input
        if not code_snippet or not comments:
            return jsonify({'error': 'Code snippet and comments required'}), 400
        
        # Create input data
        input_data = {
            'code_snippet': code_snippet,
            'review_comments': comments
        }
        
        # Select AI engine
        ai_engine = AIEngine.AUTO
        if engine == 'gemini':
            ai_engine = AIEngine.GEMINI
        elif engine == 'ollama':
            ai_engine = AIEngine.OLLAMA
        
        # Process review
        reviewer = UltimateEmpathethicReviewer(ai_engine, api_key if api_key else None)
        result = reviewer.process_review(input_data)
        
        return jsonify({
            'success': True,
            'report': result,
            'engine_used': reviewer.engine.value,
            'word_count': len(result.split()),
            'section_count': result.count('###')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/demo', methods=['GET'])
def get_demo_data():
    """Provide demo data for quick testing"""
    demo_data = {
        'code_snippet': '''def get_active_users(users):
    results = []
    for u in users:
        if u.is_active == True and u.profile_complete == True:
            results.append(u)
    return results''',
        'review_comments': [
            "This is inefficient. Don't loop twice conceptually.",
            "Variable 'u' is a bad name.",
            "Boolean comparison '== True' is redundant."
        ]
    }
    return jsonify(demo_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)