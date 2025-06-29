import gradio as gr
import pandas as pd
import os
from together import Together
import numpy as np

def load_movie_data():
    """Load movie data from CSV file."""
    try:
        df = pd.read_csv('movies_only_2.csv')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

def create_system_prompt(df):
    """Create a system prompt that contains essential information about the available movies."""
    # Get unique genres
    genres = set()
    for genre_list in df['listed_in'].str.split(', '):
        genres.update(genre_list)
    
    genres_str = ", ".join(sorted(genres))
    
    # Sample movies from each genre for context (including descriptions)
    genre_examples = {}
    for genre in genres:
        genre_mask = df['listed_in'].str.contains(genre, na=False)
        genre_movies = df[genre_mask][['title', 'listed_in', 'description']].sample(
            min(3, len(df[genre_mask]))
        )
        genre_examples[genre] = genre_movies
    
    # Create the system prompt
    system_prompt = f"""You are a movie recommendation expert with knowledge of movies in the database.
Available movie genres: {genres_str}

Here are some example movies from each genre with their descriptions:
"""
    
    for genre, movies_df in genre_examples.items():
        system_prompt += f"\n{genre}:\n"
        for _, movie in movies_df.iterrows():
            # Truncate description if too long
            desc = movie['description'][:100] + "..." if len(str(movie['description'])) > 100 else movie['description']
            system_prompt += f"  • {movie['title']} ({movie['listed_in']}) - {desc}\n"
    
    system_prompt += """
When recommending movies, use ONLY movies from the database. Your recommendations should follow this format:
**[Movie Title]** - *[Genre(s)]*
Description: [Brief description of the movie]

Provide 5-7 recommendations unless specified otherwise. Include the movie's description to help users understand what each movie is about. If the user's request is ambiguous, ask clarifying questions.

Focus on matching the user's preferences with appropriate genres and themes from the available movies.
"""
    return system_prompt

def generate_movies_recommendations(api_key, user_query, df):
    try:
        client=Together(api_key=api_key)
        system_prompt=create_system_prompt(df)
        movie_context=build_movie_context(df)

        response=client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Please recommend movies based on this request: {user_query}\n\nHere's the complete movie database for reference:\n{movie_context[:3000]}..."  # Truncate to avoid token limits
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )

        # Extract and return the response
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating recommendations: {e}"


def build_movie_context(df):
    """Build a context string containing all movie information including descriptions."""
    context="Complete Movie Database:\n\n"

    # Add all movies with their information
    for _, row in df.iterrows():
        # Clean and truncate description if needed
        description = str(row['description'])[:150] + "..." if len(str(row['description'])) > 150 else str(row['description'])
        
        context += f"Title: {row['title']}\n"
        context += f"Genres: {row['listed_in']}\n"
        context += f"Description: {description}\n"
        context += "-" * 50 + "\n"   # Title+Genre+Description (List/Column)
    
    return context

def recommend_movies(api_key, user_query):
    if not api_key:
        return "Please enter api key"

    if not user_query.strip():
        return "Please enter your movie preferences or what kind of movie you'd like to watch."

    df=load_movie_data()
    if df is None:
        return "Failed to load movie data. Please make sure 'movies_only.csv' is available."

    # Check if required columns exist
    required_columns = ['title', 'listed_in', 'description']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return f"Missing required columns in CSV: {', '.join(missing_columns)}"
    
    # Generate recommendations
    recommendations = generate_movie_recommendations(api_key, user_query, df)
    return recommendations

# Create Gradio interface
with gr.Blocks(title="Movie Recommendation System", theme=gr.themes.Ocean()) as app:
    gr.Markdown("# 🎬 Movie Recommendation System with Descriptions")
    gr.Markdown("This app recommends movies based on your preferences using the Llama-3.3-70B model and includes detailed descriptions to help you choose.")
    
    with gr.Row():
        with gr.Column(scale=1):
            api_key_input = gr.Textbox(
                label="Together API Key", 
                placeholder="Enter your Together API key here...",
                type="password",
                info="Get your API key from together.ai"
            )
            user_query = gr.Textbox(
                label="What kind of movie would you like to watch?", 
                placeholder="Example: Action movies with strong female leads, or romantic comedies set in Paris",
                lines=3
            )
            submit_button = gr.Button("🎯 Get Recommendations", variant="primary", size="lg")
            
            gr.Markdown("""
            ### 💡 Example queries:
            - "Recommend me comedy movies"
            - "I want to watch a thriller with plot twists"
            - "Movies similar to documentaries about nature"
            - "Family-friendly animation movies"
            - "Dark psychological dramas"
            - "Feel-good movies for a movie night"
            """)
        
        with gr.Column(scale=2):
            output = gr.Textbox(
                label="🎬 Your Movie Recommendations", 
                lines=15,
                show_copy_button=True
            )
    
    submit_button.click(
        fn=recommend_movies,
        inputs=[api_key_input, user_query],
        outputs=output,
        show_progress=True
    )
    
    gr.Markdown("""
    ## 📖 How to use this app
    1. **Get API Key**: Sign up at [together.ai](https://together.ai) and get your free API key
    2. **Enter API Key**: Paste your Together API key in the field above
    3. **Describe Preferences**: Tell us what kind of movie you're in the mood for
    4. **Get Recommendations**: Click the button and receive personalized suggestions with descriptions
    5. **Enjoy**: Choose a movie and enjoy your viewing experience!
    
    ## 🎭 Features
    - **Personalized Recommendations**: AI-powered suggestions based on your preferences
    - **Detailed Descriptions**: Each recommendation comes with a movie description
    - **Genre-Aware**: Understands different movie genres and themes
    - **Flexible Queries**: Accepts natural language requests
    
    ---
    *Powered by Llama-3.3-70B via Together AI*
    """)

# Launch the app
if __name__ == "__main__":
    app.launch(share=True)
    

    
    