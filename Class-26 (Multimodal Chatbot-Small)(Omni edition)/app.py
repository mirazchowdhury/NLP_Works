import gradio as gr
import openai #
import base64
from PIL import Image
import io
import fitz  # PyMuPDF for PDF handling

# Function to extract text from PDF files
def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        pdf_document = fitz.open(pdf_file)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

# Function to generate MCQ quiz from PDF content
def generate_mcq_quiz(pdf_content, num_questions, openai_api_key, model_choice):
    if not openai_api_key:
        return "Error: No API key provided."
    
    openai.api_key = openai_api_key
    limited_content = pdf_content[:8000] if len(pdf_content) > 8000 else pdf_content
    
    prompt = f"""Based on the following document content, generate {num_questions} multiple-choice quiz questions.
For each question:
1. Create a clear question based on key concepts in the document
2. Provide 4 possible answers (A, B, C, D)
3. Indicate the correct answer
4. Briefly explain why the answer is correct
Format the output clearly with each question numbered and separated.
Document content:
{limited_content}
"""
    
    try:
        response = openai.ChatCompletion.create(
            model=model_choice,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating quiz: {str(e)}"

# Function to handle image inputs
def generate_image_response(input_text, image, openai_api_key, model_choice):
    if not openai_api_key:
        return "Error: No API key provided."
    
    openai.api_key = openai_api_key
    
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    try:
        response = openai.ChatCompletion.create(
            model=model_choice,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": input_text},
                        {"type": "image_url", 
                         "image_url": {"url": f"data:image/png;base64,{base64_str}"}
                        }
                    ]
                }
            ],
            max_completion_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {str(e)}"

# Main chatbot function
def chatbot(input_text, image, pdf_file, openai_api_key, model_choice, pdf_content, num_quiz_questions, pdf_quiz_mode, history):
    if history is None:
        history = []
    
    new_pdf_content = pdf_content
    if pdf_file is not None:
        new_pdf_content = extract_text_from_pdf(pdf_file)
    
    if pdf_quiz_mode:
        if new_pdf_content:
            quiz_response = generate_mcq_quiz(new_pdf_content, int(num_quiz_questions), openai_api_key, model_choice)
            history.append((f"👤: [PDF Quiz - {num_quiz_questions} questions]", f"🤖: {quiz_response}"))
        else:
            history.append(("👤: [PDF Quiz]", "🤖: Please upload a PDF file to generate questions."))
    else:
        if image is not None:
            response = generate_image_response(input_text, image, openai_api_key, model_choice)
            if input_text.strip():
                history.append((f"👤: {input_text}", f"🤖: {response}"))
            else:
                history.append((f"👤: [Image]", f"🤖: {response}"))
    
    return "", None, None, new_pdf_content, history

def clear_history():
    return "", None, None, "", []

def update_input_type(choice):
    if choice == "Image":
        return (
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(value=False)
        )
    elif choice == "PDF(QUIZ)":
        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(value=True)
        )

# Custom CSS styling
custom_css = """
    .gradio-container {
        font-family: 'Arial', sans-serif;
        background-color: #f0f4f8;
    }
    .gradio-header {
        background: linear-gradient(135deg, #4a00e0 0%, #8e2de2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
    }
    .gradio-chatbot {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
    }
    #submit-btn {
        background: linear-gradient(135deg, #4a00e0 0%, #8e2de2 100%);
        color: white;
        border-radius: 8px;
    }
    #clear-history {
        background: linear-gradient(135deg, #e53e3e 0%, #f56565 100%);
        color: white;
        border-radius: 8px;
    }
"""

def create_interface():
    with gr.Blocks(css=custom_css) as demo:
        gr.Markdown("""
            <div class="gradio-header">
                <h1>Multimodal Chatbot (Image + PDF Quiz)</h1>
                <h3>Analyze images or generate quizzes from PDFs</h3>
            </div>
        """)
        
        with gr.Accordion("Instructions", open=False):
            gr.Markdown("""
                - **Image Chat**: Upload an image and ask questions about it
                - **PDF Quiz**: Upload a PDF and generate multiple-choice questions
                - Always provide your OpenAI API key
                - Choose appropriate model (o1 for images, o3-mini for text)
            """)
        
        pdf_content = gr.State("")
        
        with gr.Row():
            openai_api_key = gr.Textbox(label="OpenAI API Key", type="password", placeholder="sk-...")
        
        with gr.Row():
            input_type = gr.Radio(["Image", "PDF(QUIZ)"], label="Input Type", value="Image")
        
        with gr.Row():
            input_text = gr.Textbox(label="Question (for images)", visible=True)
            image_input = gr.Image(label="Upload Image", type="pil", visible=True)
            pdf_input = gr.File(label="Upload PDF", visible=False)
            quiz_slider = gr.Slider(1, 20, value=5, step=1, label="Number of Questions", visible=False)
            quiz_mode = gr.Checkbox(visible=False)
        
        with gr.Row():
            model_choice = gr.Dropdown(["o1", "o3-mini"], label="Model", value="o1")
            submit_btn = gr.Button("Submit", elem_id="submit-btn")
            clear_btn = gr.Button("Clear History", elem_id="clear-history")
        
        chat_history = gr.Chatbot()
        
        input_type.change(
            update_input_type,
            inputs=[input_type],
            outputs=[input_text, image_input, pdf_input, quiz_slider, quiz_mode]
        )
        
        submit_btn.click(
            chatbot,
            inputs=[input_text, image_input, pdf_input, openai_api_key, model_choice, pdf_content, quiz_slider, quiz_mode, chat_history],
            outputs=[input_text, image_input, pdf_input, pdf_content, chat_history]
        )
        
        clear_btn.click(
            clear_history,
            outputs=[input_text, image_input, pdf_input, pdf_content, chat_history]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()