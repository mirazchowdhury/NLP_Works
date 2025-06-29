import gradio as gr
import os
import re
import time
import base64
from openai import OpenAI
from together import Together
from PIL import Image
import io

# Function to generate math solution using the Phi-4-reasoning-plus model via OpenRouter
def generate_math_solution_openrouter(api_key, problem_text, history=None):
    if not api_key.strip():
        return "Please enter your OpenRouter API key.", history
    
    if not problem_text.strip():
        return "Please enter a math problem.", history
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        messages = [
            {"role": "system", "content": 
             """You are an expert math tutor who explains concepts clearly and thoroughly.
             Analyze the given math problem and provide a detailed step-by-step solution.
             For each step:
             1. Show the mathematical operation
             2. Explain why this step is necessary
             3. Connect it to relevant mathematical concepts
             
             Format your response with clear section headers using markdown.
             Begin with an "Initial Analysis" section, follow with numbered steps,
             and conclude with a "Final Answer" section."""},
        ]
        
        # Add conversation history if it exists
        if history:
            for exchange in history:
                messages.append({"role": "user", "content": exchange[0]})
                if exchange[1]:  # Check if there's a response
                    messages.append({"role": "assistant", "content": exchange[1]})
        
        # Add the current problem
        messages.append({"role": "user", "content": f"Solve this math problem step-by-step: {problem_text}"})
        
        # Create the completion
        completion = client.chat.completions.create(
            model="microsoft/phi-4-reasoning-plus:free",
            messages=messages,
            extra_headers={
                "HTTP-Referer": "https://advancedmathtutor.edu",
                "X-Title": "Advanced Math Tutor",
            }
        )
        
        solution = completion.choices[0].message.content
        
        # Update history
        if history is None:
            history = []
        history.append((problem_text, solution))
        
        return solution, history
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return error_message, history

# Function to convert image to base64
def image_to_base64(image_path):
    if image_path is None:
        return None
    
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error converting image to base64: {str(e)}")
        return None

# Function to generate math solution using Together AI with support for images
def generate_math_solution_together(api_key, problem_text, image_path=None, history=None):
    if not api_key.strip():
        return "Please enter your Together AI API key.", history
    
    if not problem_text.strip() and image_path is None:
        return "Please enter a math problem or upload an image of a math problem.", history
    
    try:
        client = Together(api_key=api_key)
        
        # Create the base message structure
        messages = [
            {
                "role": "system",
                "content": """You are an expert math tutor who explains concepts clearly and thoroughly.
                 Analyze the given math problem and provide a detailed step-by-step solution.
                 For each step:
                 1. Show the mathematical operation
                 2. Explain why this step is necessary
                 3. Connect it to relevant mathematical concepts
                 
                 Format your response with clear section headers using markdown.
                 Begin with an "Initial Analysis" section, follow with numbered steps,
                 and conclude with a "Final Answer" section."""
            }
        ]
        
        # Add conversation history if it exists
        if history:
            for exchange in history:
                messages.append({"role": "user", "content": exchange[0]})
                if exchange[1]:  # Check if there's a response
                    messages.append({"role": "assistant", "content": exchange[1]})
        
        # Prepare the user message content
        user_message_content = []
        
        # Add text content if provided
        if problem_text.strip():
            user_message_content.append({
                "type": "text",
                "text": f"Solve this math problem: {problem_text}"
            })
        else:
            user_message_content.append({
                "type": "text",
                "text": "Solve this math problem from the image:"
            })
        
        # Add image if provided
        if image_path:
            # Convert image to base64
            base64_image = image_to_base64(image_path)
            if base64_image:
                user_message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })
        
        # Add the user message with content
        messages.append({
            "role": "user",
            "content": user_message_content
        })
        
        # Create the completion
        response = client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=messages,
            stream=False
        )
        
        solution = response.choices[0].message.content
        
        # Update history - for simplicity, just store the text problem
        if history is None:
            history = []
        history.append((problem_text if problem_text.strip() else "Image problem", solution))
        
        return solution, history
        
    except Exception as e:
        error_message = f"Error: {str(e)}"
        return error_message, history

# Define the Gradio interface
def create_demo():
    with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
        gr.Markdown("# 📚 Advanced Math Tutor")
        gr.Markdown("""
        This application provides step-by-step solutions to math problems using advanced AI models.
        Choose between OpenRouter's Phi-4-reasoning-plus for text-based problems or Together AI's 
        Llama-Vision for problems with images.
        """)
        
        # Main tabs
        with gr.Tabs():
            # Text-based problem solver (OpenRouter)
            with gr.TabItem("Text Problem Solver (OpenRouter)"):
                with gr.Row():
                    with gr.Column(scale=1):
                        openrouter_api_key = gr.Textbox(
                            label="OpenRouter API Key", 
                            placeholder="Enter your OpenRouter API key (starts with sk-or-)",
                            type="password"
                        )
                        text_problem_input = gr.Textbox(
                            label="Math Problem", 
                            placeholder="Enter your math problem here...",
                            lines=5
                        )
                        example_problems = gr.Examples(
                            examples=[
                                ["Solve the quadratic equation: 3x² + 5x - 2 = 0"],
                                ["Find the derivative of f(x) = x³ln(x)"],
                                ["Calculate the area of a circle with radius 5 cm"],
                                ["Find all values of x that satisfy the equation: log₂(x-1) + log₂(x+3) = 5"]
                            ],
                            inputs=[text_problem_input],
                            label="Example Problems"
                        )
                        with gr.Row():
                            openrouter_submit_btn = gr.Button("Solve Problem", variant="primary")
                            openrouter_clear_btn = gr.Button("Clear")
                    
                with gr.Column(scale=2):
                    openrouter_solution_output = gr.Markdown(label="Solution")
                
                # Store conversation history (invisible to user)
                openrouter_conversation_history = gr.State(value=None)
                
                # Button actions
                openrouter_submit_btn.click(
                    fn=generate_math_solution_openrouter,
                    inputs=[openrouter_api_key, text_problem_input, openrouter_conversation_history],
                    outputs=[openrouter_solution_output, openrouter_conversation_history]
                )
                
                openrouter_clear_btn.click(
                    fn=lambda: ("", None),
                    inputs=[],
                    outputs=[openrouter_solution_output, openrouter_conversation_history]
                )
            
            # Image-based problem solver (Together AI)
            with gr.TabItem("Image Problem Solver (Together AI)"):
                with gr.Row():
                    with gr.Column(scale=1):
                        together_api_key = gr.Textbox(
                            label="Together AI API Key", 
                            placeholder="Enter your Together AI API key",
                            type="password"
                        )
                        together_problem_input = gr.Textbox(
                            label="Problem Description (Optional)", 
                            placeholder="Enter additional context for the image problem...",
                            lines=3
                        )
                        together_image_input = gr.Image(
                            label="Upload Math Problem Image",
                            type="filepath"
                        )
                        with gr.Row():
                            together_submit_btn = gr.Button("Solve Problem", variant="primary")
                            together_clear_btn = gr.Button("Clear")
                    
                with gr.Column(scale=2):
                    together_solution_output = gr.Markdown(label="Solution")
                
                # Store conversation history (invisible to user)
                together_conversation_history = gr.State(value=None)
                
                # Button actions
                together_submit_btn.click(
                    fn=generate_math_solution_together,
                    inputs=[together_api_key, together_problem_input, together_image_input, together_conversation_history],
                    outputs=[together_solution_output, together_conversation_history]
                )
                
                together_clear_btn.click(
                    fn=lambda: ("", None),
                    inputs=[],
                    outputs=[together_solution_output, together_conversation_history]
                )
            
            # Help tab
            with gr.TabItem("Help"):
                gr.Markdown("""
                ## How to Use the Advanced Math Tutor
                
                ### Getting Started
                
                #### For Text-Based Problems (OpenRouter)
                1. You'll need an API key from OpenRouter
                2. Sign up at [OpenRouter](https://openrouter.ai/) to get your API key
                3. Enter your API key in the designated field in the "Text Problem Solver" tab
                
                #### For Image-Based Problems (Together AI)
                1. You'll need an API key from Together AI
                2. Sign up at [Together AI](https://www.together.ai/) to get your API key
                3. Enter your API key in the designated field in the "Image Problem Solver" tab
                4. Upload an image of your math problem
                5. Optionally add text to provide additional context
                
                ### Solving Math Problems
                - For text problems: Type or paste your math problem in the input field
                - For image problems: Upload a clear image of the math problem
                - Click "Solve Problem" to get a detailed step-by-step solution
                - The solution will include explanations for each step
                
                ### Tips for Best Results
                - Be specific in your problem description
                - Include all necessary information
                - For complex equations, use clear notation
                - For algebraic expressions, use ^ for exponents (e.g., x^2 for x²)
                - Use parentheses to group terms clearly
                - For images, ensure the math problem is clearly visible and well-lit
                
                ### Types of Problems You Can Solve
                - Algebra (equations, inequalities, systems of equations)
                - Calculus (derivatives, integrals, limits)
                - Trigonometry
                - Geometry
                - Statistics and Probability
                - Number Theory
                - And many more!
                """)
        
        # Footer
        gr.Markdown("""
        ---
        ### About
        This application uses Microsoft's Phi-4-reasoning-plus model via OpenRouter for text-based problems
        and Llama-Vision-Free via Together AI for image-based problems. 
        Your API keys are required but not stored permanently.
        """)
    
    return demo

# Launch the app
if __name__ == "__main__":
    demo = create_demo()
    demo.launch()