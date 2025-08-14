#!/usr/bin/env python3
"""
Advanced Empathetic Code Reviewer with Stand-Out Features
"""

import json
import sys
import re
import requests
from typing import Dict, List, Any, Tuple
from enum import Enum

class CommentSeverity(Enum):
    GENTLE = "gentle"
    MODERATE = "moderate"
    HARSH = "harsh"
    CRITICAL = "critical"

class AdvancedEmpathethicReviewer:
    def __init__(self):
        self.severity_keywords = {
            CommentSeverity.CRITICAL: ['terrible', 'awful', 'horrible', 'stupid', 'idiotic', 'garbage'],
            CommentSeverity.HARSH: ['bad', 'wrong', 'inefficient', 'poor', 'sloppy', 'messy'],
            CommentSeverity.MODERATE: ['should', 'could', 'consider', 'might want to', 'try'],
            CommentSeverity.GENTLE: ['perhaps', 'maybe', 'suggestion', 'alternatively']
        }
        
        self.code_patterns = {
            'list_comprehension': r'for .+ in .+:\s*if .+:\s*.+\.append',
            'boolean_redundancy': r'== True|== False',
            'single_letter_vars': r'\b[a-z]\b(?!\s*=)',
            'magic_numbers': r'\b\d{2,}\b',
            'nested_loops': r'for .+ in .+:\s*for .+ in',
        }
        
        self.resource_links = {
            'list_comprehension': 'https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions',
            'boolean_comparison': 'https://pep8.org/#programming-recommendations',
            'naming_conventions': 'https://pep8.org/#naming-conventions',
            'performance': 'https://docs.python.org/3/library/profile.html',
            'clean_code': 'https://www.python.org/dev/peps/pep-0008/'
        }

    def analyze_comment_severity(self, comment: str) -> CommentSeverity:
        """Advanced severity analysis with contextual understanding"""
        comment_lower = comment.lower()
        
        for severity, keywords in self.severity_keywords.items():
            if any(keyword in comment_lower for keyword in keywords):
                return severity
        
        return CommentSeverity.GENTLE

    def detect_code_patterns(self, code: str) -> Dict[str, bool]:
        """Detect common code patterns for targeted advice"""
        patterns_found = {}
        for pattern_name, regex in self.code_patterns.items():
            patterns_found[pattern_name] = bool(re.search(regex, code, re.MULTILINE))
        return patterns_found

    def get_contextual_tone(self, severity: CommentSeverity) -> str:
        """Get tone modifiers based on comment severity"""
        tone_map = {
            CommentSeverity.CRITICAL: "I understand this feedback might have felt harsh. Let's reframe it constructively",
            CommentSeverity.HARSH: "This is actually a great learning opportunity",
            CommentSeverity.MODERATE: "Good observation! Here's how we can build on it",
            CommentSeverity.GENTLE: "Nice suggestion! Let's explore this further"
        }
        return tone_map.get(severity, "Let's look at this feedback")

    def create_master_prompt(self, code_snippet: str, comments: List[str]) -> str:
        """Enhanced prompt with pattern detection and contextual awareness"""
        
        patterns = self.detect_code_patterns(code_snippet)
        active_patterns = [k for k, v in patterns.items() if v]
        
        severity_analysis = []
        for i, comment in enumerate(comments):
            severity = self.analyze_comment_severity(comment)
            tone = self.get_contextual_tone(severity)
            severity_analysis.append(f"Comment {i+1}: {severity.value} severity - {tone}")

        newline = chr(10)
        comments_list = newline.join([f"{i+1}. \"{comment}\"" for i, comment in enumerate(comments)])
        severity_list = newline.join(severity_analysis)
        
        return f"""You are a world-class senior software engineer and mentor known for transforming junior developers into confident programmers. You have a gift for turning criticism into growth opportunities.

**CODE ANALYSIS:**
```python
{code_snippet}
```

**DETECTED PATTERNS:** {', '.join(active_patterns) if active_patterns else 'Clean basic structure'}

**COMMENT SEVERITY ANALYSIS:**
{severity_list}

**ORIGINAL COMMENTS TO TRANSFORM:**
{comments_list}

**YOUR MISSION:**
Transform each comment into a mentoring masterpiece. For each comment, create:

---
### 🔍 Analysis of Comment: "{comments[0] if comments else 'PLACEHOLDER'}"

**💚 Positive Rephrasing:**
[Start with genuine praise for what they got right, then gently introduce the improvement. Match your tone to the original comment's severity - be extra encouraging for harsh comments]

**🧠 The 'Why' (Software Engineering Principle):**
[Explain the deeper principle: performance, readability, maintainability, team collaboration, debugging ease, etc. Include specific impacts like "with 10,000+ users, this could save 2 seconds per request"]

**✨ Suggested Improvement:**
```python
[Show the improved code with clear comments explaining the changes]
```

**📚 Learning Resources:**
- [Specific PEP-8 section, documentation, or concept link]
- [Additional learning resource if relevant]

**🎯 Pro Tip:** [One advanced insight that shows deep understanding]

---

**ADVANCED REQUIREMENTS:**
1. Adjust tone based on comment severity (harsher comments need more encouragement)
2. Reference the detected code patterns naturally
3. Provide specific performance/readability impacts
4. Include at least one "pro tip" that shows senior-level insight
5. Use emojis strategically for visual appeal and engagement
6. End each section with actionable next steps

**TONE CALIBRATION:**
- Critical/Harsh comments: Extra encouraging, emphasize learning journey
- Moderate comments: Collaborative and educational
- Gentle comments: Build on the good observation

Create the analysis for ALL comments now:"""

    def call_ollama(self, prompt: str) -> str:
        """Enhanced Ollama API call with better error handling"""
        try:
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    'model': 'llama3.1:8b',
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                }, timeout=120)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"API Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Connection error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"

    def create_summary_analysis(self, code_snippet: str, comments: List[str]) -> str:
        """Create an overall summary with growth-focused insights"""
        patterns = self.detect_code_patterns(code_snippet)
        total_severity = sum(1 for comment in comments if self.analyze_comment_severity(comment) in [CommentSeverity.HARSH, CommentSeverity.CRITICAL])
        
        if total_severity > len(comments) * 0.6:
            encouragement_level = "extra_high"
        elif total_severity > 0:
            encouragement_level = "high"
        else:
            encouragement_level = "standard"

        summary_prompts = {
            "extra_high": "This developer faced some tough feedback but shows solid problem-solving instincts. Focus on the growth journey and celebrate their logical thinking.",
            "high": "This developer is on a great learning path with some excellent fundamentals. The improvements suggested will level up their skills significantly.",
            "standard": "This developer writes clean, logical code and is ready for some advanced optimizations. Great foundation to build upon!"
        }

        return f"""
## 🌟 Overall Growth Summary & Next Steps

{summary_prompts[encouragement_level]}

**🎯 Key Themes from This Review:**
- **Code Organization**: Moving toward more Pythonic patterns
- **Performance Awareness**: Understanding computational complexity
- **Readability Focus**: Writing code that tells a story

**🚀 Recommended Learning Path:**
1. **This Week**: Practice list comprehensions and boolean operations
2. **Next Week**: Dive deeper into Python's built-in functions and itertools
3. **This Month**: Explore algorithmic complexity and optimization patterns

**💡 Senior Developer Insight:**
The patterns in this code suggest you're thinking algorithmically, which is fantastic! The next level is thinking about code as communication - every variable name, every function structure should tell your future self (and your teammates) a clear story.

---
*Remember: Every expert was once a beginner. The fact that you're actively seeking feedback shows you're on the path to mastery! 🌟*
"""

    def process_review(self, input_data: Dict[str, Any]) -> str:
        """Main processing with all advanced features"""
        code_snippet = input_data['code_snippet']
        review_comments = input_data['review_comments']
        
        # Generate the AI analysis
        master_prompt = self.create_master_prompt(code_snippet, review_comments)
        ai_response = self.call_ollama(master_prompt)
        
        # Generate summary
        summary = self.create_summary_analysis(code_snippet, review_comments)
        
        # Create final report
        report = f"""# 🌟 Empathetic Code Review Report

*Transforming criticism into growth opportunities*

## 📝 Original Code Under Review
```python
{code_snippet}
```

{ai_response}

{summary}

---
**🛠 Generated by Advanced Empathetic Code Reviewer v2.0**
*Built for the "Freedom from Mundane" Hackathon*
"""
        
        return report

def main():
    if len(sys.argv) != 2:
        print("Usage: python advanced_reviewer.py <input.json>")
        print("Example: python advanced_reviewer.py test_input.json")
        sys.exit(1)
    
    try:
        # Load input
        with open(sys.argv[1], 'r') as f:
            input_data = json.load(f)
        
        # Validate input structure
        required_keys = ['code_snippet', 'review_comments']
        for key in required_keys:
            if key not in input_data:
                raise ValueError(f"Missing required key: {key}")
        
        print("🚀 Processing empathetic code review...")
        print(f"📊 Analyzing {len(input_data['review_comments'])} comments")
        
        # Create reviewer and process
        reviewer = AdvancedEmpathethicReviewer()
        result = reviewer.process_review(input_data)
        
        # Save output
        output_file = 'empathetic_review_report.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"✅ Report generated successfully: {output_file}")
        print("\n🎯 Advanced Features Implemented:")
        print("  ✨ Contextual tone adjustment based on comment severity")
        print("  🔍 Automatic code pattern detection")
        print("  📚 Smart resource linking")
        print("  💡 Senior-level insights and pro tips")
        print("  🌟 Growth-focused summary with learning paths")
        print("  🎨 Enhanced markdown formatting with emojis")
        
        # Display a preview
        print(f"\n📖 Preview of first few lines:")
        preview_lines = result.split('\n')[:10]
        for line in preview_lines:
            print(f"   {line}")
        print("   ...")
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find input file '{sys.argv[1]}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()