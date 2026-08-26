import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
from google import genai
from google.genai import types

# CSV dataset load
df = pd.read_csv("science_instruction_response_10000.csv")

# Gemini client
client = genai.Client(
    api_key="meri api key"
)


# ---------------- BOT FUNCTION ----------------

def ask_bot():
    question = entry.get().strip()

    if question == "":
        return

    # User ka question chat mein show karo
    chat.insert(tk.END, "You: " + question + "\n\n")

    # Input box clear
    entry.delete(0, tk.END)

    found = False

    # Dataset mein search
    for i in range(len(df)):
        instruction = str(df.iloc[i]["Instruction"])

        if question.lower() in instruction.lower():
            answer = df.iloc[i]["Response"]

            chat.insert(tk.END, "Bot: " + str(answer) + "\n\n")

            found = True
            break

    # Agar dataset mein answer nahi mila
    if not found:

        chat.insert(tk.END, "Bot: Gemini se answer generate ho raha hai...\n\n")

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",

                contents=f"""
                You are a helpful science tutor.

                Answer the question in ONLY 2 to 3 short lines.
                Use simple English.
                Give a clear and scientifically accurate answer.
                Do not give extra explanation.

                Question: {question}
                """,

                config=types.GenerateContentConfig(
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    )
                )
            )

            chat.insert(
                tk.END,
                "Bot: " + response.text + "\n\n"
            )

        except Exception as e:
            chat.insert(
                tk.END,
                "Bot: Error: " + str(e) + "\n\n"
            )


# ---------------- MAIN WINDOW ----------------

window = tk.Tk()

window.title("Study Assistant Bot")

window.geometry("700x600")


# ---------------- TITLE ----------------

title = tk.Label(
    window,
    text="🤖 Study Assistant Bot",
    font=("Arial", 20, "bold")
)

title.pack(pady=10)


# ---------------- CHAT AREA ----------------

chat = scrolledtext.ScrolledText(
    window,
    width=80,
    height=25,
    font=("Arial", 12)
)

chat.pack(padx=10, pady=10)

chat.insert(
    tk.END,
    "Bot: Hello! 👋\n"
    "Ask me any science question.\n\n"
)


# ---------------- INPUT AREA ----------------

entry = tk.Entry(
    window,
    font=("Arial", 13),
    width=55
)

entry.pack(side=tk.LEFT, padx=10, pady=10)


# ---------------- SEND BUTTON ----------------

send_button = tk.Button(
    window,
    text="Send",
    font=("Arial", 12, "bold"),
    command=ask_bot
)

send_button.pack(side=tk.LEFT, padx=5)


# Enter key se bhi message send hoga
window.bind("<Return>", lambda event: ask_bot())


# ---------------- START APP ----------------

window.mainloop()