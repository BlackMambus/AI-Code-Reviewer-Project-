import subprocess
import ast
import openai  # Optional: if using LLM-based suggestions

# Optional: Set your OpenAI API key
openai.api_key = "your-api-key"

def run_linter(file_path):
    """Run pylint on the given file and return the output."""
    result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
    return result.stdout

def analyze_ast(file_path):
    """Perform basic AST analysis to detect bad practices."""
    with open(file_path, "r") as f:
        tree = ast.parse(f.read(), filename=file_path)

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and len(node.body) > 50:
            issues.append(f"Function '{node.name}' is too long ({len(node.body)} lines). Consider refactoring.")
        if isinstance(node, ast.Global):
            issues.append(f"Global variable '{node.names}' detected. Avoid using globals.")
    return issues

def ai_suggestions(code):
    """Use OpenAI to get code improvement suggestions."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a code reviewer."},
            {"role": "user", "content": f"Review the following Python code and suggest improvements:\n\n{code}"}
        ]
    )
    return response['choices'][0]['message']['content']

def review_code(file_path):
    print("🔍 Running static analysis...")
    lint_output = run_linter(file_path)
    print(lint_output)

    print("\n🧠 Analyzing AST...")
    ast_issues = analyze_ast(file_path)
    for issue in ast_issues:
        print(f"- {issue}")

    print("\n🤖 AI Suggestions (optional)...")
    with open(file_path, "r") as f:
        code = f.read()
    suggestions = ai_suggestions(code)
    print(suggestions)

# Example usage
if __name__ == "__main__":
    review_code("example.py")




