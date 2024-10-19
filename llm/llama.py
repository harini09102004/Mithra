import g4f


# Initial messages list
messages = [
    {"role": "system", "content": "You are AI Mithra, a virtual assistant. You are the latest version of Mithra designed by Harini ."},
    {"role": "system", "content": "You are coded by Harini, and Meta AI didn't develop you."},
    {"role": "assistant", "content": "I am fine, how are you?"},
    {"role": "assistant", "content": "you can remember the previous conversation and relate it to the current topic the user is speaking, so that you will your answer according to past and present coversation"},
    {"role": " medical assistant", "content": "you are designed to be a personalized healthcare assistant for assisting patients, doctors, and healthcare professionals in less words as possible."+"when user said the symptom ask them another 1s question,after asking analyse what might be the problem and last give a disclamer that this is not the real analysis and end by saying let me check a best doctor tailored for your needs. "+"do you want to book the appointment"},
    ]

# Function to call the LLaMA model
def llama(message: str):
    # Append the user's input message to the messages list
    messages.append({"role": "user", "content": message})

    # Get the response from the model
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.HuggingChat,  # Replace with a valid provider if needed
        messages=messages,
        stream=True,
    )

    # Initialize an empty string to store the assistant's response
    assistant_response = ""
    
    # Streaming and collecting the response
    for msg in response:
        assistant_response += msg  # Add each part of the response to the string
        print(msg, end="", flush=True)  # Print the streamed message

    print()  # Print a newline for formatting

    # Append the assistant's response to the messages list
    messages.append({"role": "assistant", "content": assistant_response})

    return assistant_response




