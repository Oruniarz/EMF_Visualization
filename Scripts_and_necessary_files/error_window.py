import customtkinter as ctk


class ErrorPopup(ctk.CTkToplevel):
    def __init__(self, parent, error_message: str, close_app: bool = False):
        super().__init__(parent)

        self.parent = parent
        self.close_app = close_app

        self.title("Error")
        popup_w, popup_h = 420, 180
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.transient(parent)
        self.grab_set()

        # Center on parent windows
        self.center_on_parent(parent, popup_w, popup_h)

        # UI
        label_title = ctk.CTkLabel(self, text="An error has occurred", font=("Arial", 18, "bold"))
        label_title.pack(pady=(20, 5))

        label_error = ctk.CTkLabel(self, text=error_message, wraplength=380, font=("Arial", 14))
        label_error.pack(pady=(0, 20))

        ok_button = ctk.CTkButton(self, text="OK", command=self.on_ok)
        ok_button.pack(pady=10)

    def center_on_parent(self, parent, w, h):
        parent.update_idletasks()

        # parent position/size
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()

        # compute centered position
        x = px + (pw // 2) - (w // 2)
        y = py + (ph // 2) - (h // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")

    def on_ok(self):
        self.grab_release()
        self.destroy()

        # if critical error -> close whole application
        if self.close_app:
            self.parent.destroy()


def show_error(parent, msg: str, close_app: bool = False):
    ErrorPopup(parent, msg, close_app)
