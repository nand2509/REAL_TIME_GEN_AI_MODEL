import google.generativeai as genai

genai.configure(api_key=" ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Who is Maharaja Dr. Vibhuti Narain Singh?")
print(response.text)



