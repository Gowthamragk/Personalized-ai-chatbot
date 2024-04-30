import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai


class GeminiChatApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Gemini Chat")
        self.master.geometry("600x400")

        self.chat_history = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20)
        self.chat_history.pack(padx=10, pady=10)

        self.user_input_frame = tk.Frame(master)
        self.user_input_frame.pack(padx=10, pady=10)

        self.user_input = tk.Entry(self.user_input_frame, width=50)
        self.user_input.grid(row=0, column=0, padx=10, pady=10)

        self.send_button = tk.Button(self.user_input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=10, pady=10)

        # Configure Gemini with your API key
        api_key = "AIzaSyCfvWO0cVqAUW2u6YcjbvNm6WaqlPYivps"
        self.configure_gemini(api_key)

        # Set up the model
        self.generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                           generation_config=self.generation_config,
                                           safety_settings=self.safety_settings)

        self.display_greeting()

    def configure_gemini(self, api_key):
        genai.configure(api_key=api_key)

    def generate_gemini_response(self, prompt_parts):
        response = self.model.generate_content(prompt_parts)
        return response.text

    def send_message(self):
        user_input_text = self.user_input.get()
        self.display_message("You", user_input_text)

        if user_input_text.lower() == "exit":
            self.display_message("Gemini", "Goodbye!")
            self.master.quit()
        else:
            prompt_parts = [user_input_text]
            gemini_response = self.generate_gemini_response(prompt_parts)
            self.display_message("Gemini", gemini_response)

        self.user_input.delete(0, tk.END)

    def display_message(self, sender, message):
        self.chat_history.insert(tk.END, f"{sender}: {message}\n")
        self.chat_history.see(tk.END)

    def display_greeting(self):
        greeting_message = "Welcome to Gemini Chat! You can start chatting by typing your message below."
        self.display_message("Gemini", greeting_message)


def main():
    root = tk.Tk()
    app = GeminiChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()