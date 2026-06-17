import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO


def get_weather():
    city = entry.get()
    api_key = "45138b22cde99e6d60d714c5210cb23a"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            label_res.config(text=f"Температура: {temp}°C")

            icon_id = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"

            img_res = requests.get(icon_url)
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_res.content)))
            label_img.config(image=img)
            label_img.image = img
        else:
            label_res.config(text="Город не найден")
    except:
        label_res.config(text="Ошибка подключения")


root = tk.Tk()
root.title("Погода")

entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Узнать погоду", command=get_weather).pack()

label_res = tk.Label(root, text="")
label_res.pack()

label_img = tk.Label(root)
label_img.pack()

root.mainloop()