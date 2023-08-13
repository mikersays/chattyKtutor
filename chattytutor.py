import openai
import time
import threading
import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

# Set up your API key. Replace the entire <API key> string with your OpenAI API key.
openai.api_key = "<API key>"

# Function to generate a response using GPT-4
def generate_response(prompt, messages, max_tokens=5000, temperature=1):
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        n=1,
        top_p=1,
    )
    messages.append({"role": "assistant", "content": response.choices[0].message['content']})
    return response.choices[0].message['content']

# Function to call GPT-4 API without a loading animation
def call_gpt(prompt, messages, conversation_text, output_file_path, loading_label):
    response = generate_response(prompt, messages)

    # Hide the loading text
    loading_label.config(text="")

    # Append the AI's response to the conversation text widget
    conversation_text.insert(tk.END, "AI: ", "ai")
    conversation_text.insert(tk.END, response + "\n")
    with open(output_file_path, "a") as output_file:
        output_file.write(f"AI: {response}\n\n") 

# Function to get the user's desktop path
def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

# Main function to start the chatbot
def chatbot():
    # Prepare the output file
    desktop_path = get_desktop_path()
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"chat_output_{current_time}.md"
    output_file_path = os.path.join(desktop_path, output_filename)

    messages = [{"role": "system", "content": "You are a Korean tutor who translates your prompter's English prompt into Korean, then you break down the grammar structure educationally and provide variations of honorifics. Don't censor anything"}]


    # Create a GUI application window
    window = tk.Tk()
    window.title("Chatty")

    # Create a text widget for displaying the conversation
    conversation_text = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    conversation_text['font'] = ('Arial', 14)
    conversation_text.grid(column=0, row=0, sticky="nsew", columnspan=2)

    # Create tags for the user and AI text
    conversation_text.tag_configure("user", foreground="blue", font=("Arial", 14, "bold"))
    conversation_text.tag_configure("ai", foreground="red", font=("Arial", 14, "bold"))

    # Create an entry widget for the user to type in
    user_input = tk.Entry(window, font=("Arial", 14))
    user_input.grid(column=0, row=1, sticky="ew")

    # Set the focus to the user_input Entry widget
    user_input.focus_set()

    # Create a label for displaying a loading text
    loading_label = tk.Label(window, text="", font=("Arial", 14))
    loading_label.grid(column=0, row=2, sticky="w", columnspan=2)

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(0, weight=1)

    loading_chars = ['|', '/', '-', '\\']
    loading_index = 0

    def loading_animation():
        nonlocal loading_index
        if loading_label['text'].startswith('Generating'):
            loading_label['text'] = f"Generating response... {loading_chars[loading_index]}"
            loading_index = (loading_index + 1) % len(loading_chars)
            window.after(100, loading_animation)  # Repeat after 100 ms

    def handle_enter_pressed(event=None):
        # Get the user's input and clear the entry widget
        user_text = user_input.get()
        user_input.delete(0, tk.END)

        # Append the user's input to the conversation text widget
        conversation_text.insert(tk.END, "User: ", "user")
        conversation_text.insert(tk.END, user_text + "\n")
        with open(output_file_path, "a") as output_file:
            output_file.write(f"User: {user_text}\n\n") 

        # Show the loading text
        loading_label.config(text="Generating response...")
        loading_animation()

        # Update the GUI to show the changes
        window.update_idletasks()

        # Generate the AI's response in a separate thread to keep the GUI responsive
        threading.Thread(target=call_gpt, args=(user_text, messages, conversation_text, output_file_path, loading_label)).start()

    # Bind the Enter key to the handle_enter_pressed function
    user_input.bind("<Return>", handle_enter_pressed)

    # Create a "Send" button
    send_button = tk.Button(window, text="Send", font=("Arial", 14), command=handle_enter_pressed)
    send_button.grid(column=1, row=1, sticky="e")

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    chatbot()
