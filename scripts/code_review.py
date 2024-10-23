import os
import sys
from github import Github
from groq import Groq
from langchain.llms import Groq
from langchain.prompts import PromptTemplate

class CodeReviewer:
    def __init__(self):
        self.groq_client = Groq(
            api_key=os.getenv('GROQ_API_KEY'),
            model_name="llama2-70b-4096"
        )
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
        self.pr = self.repo.get_pull(int(os.getenv('PR_NUMBER')))

    def get_code_review_prompt(self, code):
        return f"""
        As a senior developer, review the following code and provide feedback.
        Focus on:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Performance considerations
        4. Security concerns
        5. Documentation completeness

        Code to review:
        ```python
        {code}
        ```

        Provide your feedback in a structured format with clear suggestions for improvements.
        """

    def analyze_security(self, file_path):
        import bandit
        from bandit.core import manager
        
        mgr = manager.BanditManager()
        mgr.discover_files([file_path])
        mgr.run_tests()
        return mgr.get_issue_list()

    def check_style(self, file_path):
        from pylint import epylint as lint
        (pylint_stdout, pylint_stderr) = lint.py_run(file_path, return_std=True)
        return pylint_stdout.getvalue()

    def review_file(self, file_path):
        with open(file_path, 'r') as file:
            code = file.read()

        # Get LLM review
        review_prompt = self.get_code_review_prompt(code)
        llm_review = self.groq_client(review_prompt)

        # Security check
        security_issues = self.analyze_security(file_path)
        
        # Style check
        style_issues = self.check_style(file_path)

        return {
            'llm_review': llm_review,
            'security_issues': security_issues,
            'style_issues': style_issues
        }

    def create_review_comment(self, file_path, review_results):
        comment = f"""
        ## AI Code Review for `{file_path}`

        ### LLM Analysis
        {review_results['llm_review']}

        ### Security Check
        {'No security issues found.' if not review_results['security_issues'] else str(review_results['security_issues'])}

        ### Style Guide Compliance
        ```
        {review_results['style_issues']}
        ```

        ---
        Note: This is an automated review. Please verify all suggestions before implementing.
        """
        
        self.pr.create_issue_comment(comment)

    def run_review(self):
        changed_files = os.getenv('CHANGED_FILES').split()
        
        for file_path in changed_files:
            if file_path.endswith('.py'):
                review_results = self.review_file(file_path)
                self.create_review_comment(file_path, review_results)

if __name__ == "__main__":
    reviewer = CodeReviewer()
    reviewer.run_review()
