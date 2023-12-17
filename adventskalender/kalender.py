import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Canvas
from PIL import Image, ImageTk
import random




factor = 2
url = "https://lionskn-adventskalender.de/"
numbers_to_search = ['8562', '8565', '8566', '8567']

base_path = "gifs/loose"
start_index = 1
end_index = 13

# Generate the list of GIF paths using a list comprehension
gif_paths = [f"{base_path}{i}.gif" for i in range(start_index, end_index + 1)]


def load_gif_frames(gif_path, factor):
    img = Image.open(gif_path)    
    frames = []
    try:
        while True:      
            resized_img = img.resize((img.width * factor, img.height * factor), Image.Resampling.LANCZOS)
            frames.append(ImageTk.PhotoImage(resized_img))
            img.seek(img.tell() + 1)

    except EOFError:
        pass
    return frames


# Send a GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all occurrences of the specified numbers
    found_numbers = [number for number in numbers_to_search if soup.find(string=number)]

    # Display a pop-up window with a GIF based on the result
    root = Tk()
    root.title("Result")

    if found_numbers:
        gif_path = "gifs/win.gif" 
        message = f"GEWONNEN!!! JAAAAA!!!\n {', '.join(found_numbers)}"
    else:
        gif_path = random.choice(gif_paths) 
        message = "wieder mal verloren :("

    frames = load_gif_frames(gif_path, factor)
    
    canvas = Canvas(root, width=frames[0].width(), height=frames[0].height())
    canvas.pack()

    def update_frame(idx):
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=frames[idx])
        root.after(100, update_frame, (idx + 1) % len(frames))

    update_frame(0)

    Label(root, text=message, font=("Arial", 26)).pack()

    # Center the root window on the screen
    root.update_idletasks()
    root.withdraw()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))
    root.deiconify()

    root.mainloop()

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
