
import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

PROPOSAL_PROMPT_TEMPLATE = """
You are an expert freelance proposal writer with an 80%+ client reply rate on platforms like Upwork and Fiverr.
Analyze the following job description and create a high-converting, pitch-perfect proposal.

Job Description:
{job_description}

Desired Tone/Style:
{tone}

Proposal Length:
{length}

Custom Instructions / Extra Notes from Freelancer:
{custom_notes}

Key Rules:
1. First 2 lines MUST hook the client immediately by demonstrating deep understanding of their specific pain points.
2. Show a clear value proposition and past relevant experience/approach.
3. Keep sentences short, crisp, and high-impact.
4. Include 1-2 relevant clarifying questions that encourage the client to reply.
5. End with a subtle, non-pushy Call to Action (CTA).

Generate the proposal formatted neatly with Markdown:
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-proposal', methods=['POST'])
def generate_proposal():
    try:
        data = request.json
        job_description = data.get('job_description', '').strip()
        tone = data.get('tone', 'Professional & Direct')
        length = data.get('length', 'Medium')
        custom_notes = data.get('custom_notes', 'None')

        if not job_description:
            return jsonify({'success': False, 'error': 'Job description cannot be empty.'}), 400

        if not API_KEY:
            return jsonify({'success': False, 'error': 'Google API Key missing on server.'}), 500

        # Gemini Model Initialization
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = PROPOSAL_PROMPT_TEMPLATE.format(
            job_description=job_description, 
            tone=tone, 
            length=length, 
            custom_notes=custom_notes if custom_notes else 'None'
        )
        
        response = model.generate_content(prompt)

        return jsonify({
            'success': True,
            'proposal': response.text
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
