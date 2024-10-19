import eel

# Initialize Eel
eel.init('web')  # Ensure 'web' is the folder containing your HTML and JS files

# Start the Eel server
eel.start('index.html', size=(1000, 600), block=False)

# Call JavaScript function from Python
eel.DisplayMessage('Eel is working!')
