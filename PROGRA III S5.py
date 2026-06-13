import tkinter as tk
from tkinter import messagebox


#stack#
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("La pila está vacía.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


#edit#
class TextEditor:
    def __init__(self):
        self.content = ""
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.action_history = []

    def write(self, text):
        if not text.strip():
            raise ValueError("No puede escribir texto vacío.")

        self.content += text

        self.undo_stack.push(("write", text))

        self.redo_stack = Stack()

        self.action_history.append(
            f"Escribió: '{text}'"
        )

    def delete(self, n):
        if n <= 0:
            raise ValueError("Ingrese una cantidad válida.")

        if n > len(self.content):
            raise ValueError(
                "No puede borrar más caracteres de los existentes."
            )

        deleted_text = self.content[-n:]

        self.content = self.content[:-n]

        self.undo_stack.push(
            ("delete", deleted_text)
        )

        self.redo_stack = Stack()

        self.action_history.append(
            f"Borró: '{deleted_text}'"
        )

    def undo(self):
        if self.undo_stack.is_empty():
            raise ValueError(
                "No hay acciones para deshacer."
            )

        action, data = self.undo_stack.pop()

        if action == "write":
            self.content = self.content[:-len(data)]

        elif action == "delete":
            self.content += data

        self.redo_stack.push(
            (action, data)
        )

        self.action_history.append(
            "Undo"
        )

    def redo(self):
        if self.redo_stack.is_empty():
            raise ValueError(
                "No hay acciones para rehacer."
            )

        action, data = self.redo_stack.pop()

        if action == "write":
            self.content += data

        elif action == "delete":
            self.content = self.content[:-len(data)]

        self.undo_stack.push(
            (action, data)
        )

        self.action_history.append(
            "Redo"
        )

    def show(self):
        return self.content

    def history(self):
        return self.action_history


#INTER#
editor = TextEditor()


def actualizar_contenido():
    contenido_actual.config(
        text=editor.show()
    )


def escribir_texto():
    try:
        texto = entrada_texto.get()

        editor.write(texto)

        entrada_texto.delete(0, tk.END)

        actualizar_contenido()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def borrar_texto():
    try:
        cantidad = int(
            entrada_borrar.get()
        )

        editor.delete(cantidad)

        entrada_borrar.delete(0, tk.END)

        actualizar_contenido()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Ingrese un número válido."
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def deshacer():
    try:
        editor.undo()

        actualizar_contenido()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def rehacer():
    try:
        editor.redo()

        actualizar_contenido()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def mostrar_historial():
    historial_text.delete(
        1.0,
        tk.END
    )

    historial = editor.history()

    if len(historial) == 0:
        historial_text.insert(
            tk.END,
            "No hay acciones registradas."
        )
    else:
        for accion in historial:
            historial_text.insert(
                tk.END,
                accion + "\n"
            )


ventana = tk.Tk()
ventana.title(
    "Editor de Texto con Pilas (Undo / Redo)"
)
ventana.geometry("700x550")
ventana.resizable(False, False)

titulo = tk.Label(
    ventana,
    text="Editor de Texto con Stack",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=10)

# Escribir
tk.Label(
    ventana,
    text="Texto a escribir:"
).pack()

entrada_texto = tk.Entry(
    ventana,
    width=50
)
entrada_texto.pack(pady=5)

btn_escribir = tk.Button(
    ventana,
    text="Escribir",
    width=20,
    command=escribir_texto
)
btn_escribir.pack(pady=5)

# Borrar
tk.Label(
    ventana,
    text="Cantidad de caracteres a borrar:"
).pack()

entrada_borrar = tk.Entry(
    ventana,
    width=20
)
entrada_borrar.pack(pady=5)

btn_borrar = tk.Button(
    ventana,
    text="Borrar",
    width=20,
    command=borrar_texto
)
btn_borrar.pack(pady=5)

# Undo Redo
frame_botones = tk.Frame(
    ventana
)
frame_botones.pack(pady=10)

btn_undo = tk.Button(
    frame_botones,
    text="Deshacer",
    width=15,
    command=deshacer
)
btn_undo.grid(
    row=0,
    column=0,
    padx=10
)

btn_redo = tk.Button(
    frame_botones,
    text="Rehacer",
    width=15,
    command=rehacer
)
btn_redo.grid(
    row=0,
    column=1,
    padx=10
)

# Contenido actual
tk.Label(
    ventana,
    text="Contenido actual:"
).pack()

contenido_actual = tk.Label(
    ventana,
    text="",
    bg="white",
    relief="solid",
    width=70,
    height=4,
    anchor="nw",
    justify="left"
)
contenido_actual.pack(pady=5)

# Historial
btn_historial = tk.Button(
    ventana,
    text="Mostrar Historial",
    width=20,
    command=mostrar_historial
)
btn_historial.pack(pady=10)

historial_text = tk.Text(
    ventana,
    width=70,
    height=12
)
historial_text.pack(pady=5)

ventana.mainloop()