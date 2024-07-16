"""
while True:

    numero = int(input('ingrese un numero:'))
    numero2 = int(input('ingrese otro numero:'))

    operacion = numero * numero2

    print("sin puntuacion: ", numero, numero2, operacion)

    print(f"con puntuacion: \n{numero:,}\n{numero2:,}\n{operacion:,}")
"""

import tkinter as tk


def animate():
    for i in range(10):
        for j in range(500):
            for n in range(1):
                root.geometry(f"+{n}+{j}")
                root.update()
                root.after(0)  # Espera 10 ms


root = tk.Tk()
root.geometry("+0+100")

button = tk.Button(root, text="Animate", command=animate)
button.pack()

root.mainloop()
