import google.generativeai as genai

genai.configure(api_key="AIzaSyBH9pjDICFfC4RqNF2luI86P1LVlLyCF78")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Who is Maharaja Dr. Vibhuti Narain Singh?")
print(response.text)



