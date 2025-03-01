import requests
from config import Config

class ResumeEvaluator:
    def __init__(self):
        self.api_key = Config.API_KEY
        self.api_url = Config.API_URL  # Your model API endpoint

    def create_prompt(self, resume_text, target_role):
        """
        Create a prompt for resume evaluation
        """
        system_prompt = """You are an expert resume evaluator and career advisor with deep knowledge of ATS 
        (Applicant Tracking Systems), recruitment best practices, and industry-specific hiring trends. 
        Your task is to analyze a candidate's resume against a specific job role and provide a structured 
        assessment, feedback, and actionable improvement suggestions."""
        
        user_prompt = f"""Analyze the following resume data and generate a structured evaluation for {target_role} role. 
        Provide an ATS score breakdown across different categories, along with improvement suggestions. 
        Everything should be very concise except the final recommendations. 
        The total response needs to be short and the response should strictly follow this markdown format:

        ## Resume Analysis & Scoring

        1. Role Match: (Concise Tips if any) Score: 
        2. Experience & Achievements: (Concise Tips if any) Score: 
        3. Skills Match: (Concise Tips if any) Score: 
        4. Education Fit: (Concise Tips if any) Score: 
        5. Readability & Grammar: (Concise Tips if any) Score: 
        6. Formatting & ATS Compliance: (Concise Tips if any) Score: 
        7. Keyword Density & Buzzword Balance:(Concise Tips if any) Score: 
        8. Action Verbs & Impactful Language: (Concise Tips if any) Score: 

        Final Recommendations
        - [Summarized key improvement areas]
        - [Next steps for enhancing the resume]

        Final ATS Score: (calculated using this formula and just the score being shown here, not how it is calculated, 
        total_score = (
            (role_match * 25 / 100) +
            (experience * 20 / 100) +
            (skills * 15 / 100) +
            (education * 10 / 100) +
            (grammar * 10 / 100) +
            (formatting * 7 / 100) +
            (keyword_density * 5 / 100) +
            (action_verbs * 5 / 100)
        )) Score: 

        The resume data is: 
        ''' {resume_text} '''"""
        
        return system_prompt, user_prompt

    def evaluate_resume(self, resume_text, target_role):
        """
        Evaluate a resume for a specific role
        """
        system_prompt, user_prompt = self.create_prompt(resume_text, target_role)
        
        try:
            # Hardcode the URL for testing
            api_url = "https://api.groq.com/v1/chat/completions"
            print(f"Using API URL: {api_url}")
            
            response = requests.post(
                api_url,  # Use the hardcoded URL
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": "llama3-8b-8192",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                }
            )
            
            print(f"Response status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                
            if response.status_code == 200:
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            else:
                raise Exception(f"API Error: {response.status_code}, {response.text}")
                
        except Exception as e:
            print(f"Exception details: {str(e)}")
            raise Exception(f"Error evaluating resume: {str(e)}")
