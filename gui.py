
# Professional MAYA GUI template
import customtkinter as ctk
import threading
import app as maya
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window=ctk.CTk()
window.title("🤖 MAYA AI Assistant")
window.geometry("1100x700")
window.resizable(False,False)

def update_status(text):
    status.configure(text="Status : "+text)
    window.update_idletasks()

def add_message(sender,message):
    textbox.configure(state="normal")
    textbox.insert("end",f"{sender}: {message}\n\n")
    textbox.configure(state="disabled")
    textbox.see("end")

def clear_chat():
    textbox.configure(state="normal")
    textbox.delete("1.0","end")
    textbox.configure(state="disabled")

def start_assistant():
    threading.Thread(target=maya.start_maya,daemon=True).start()

maya.update_status=update_status
maya.add_message=add_message

left=ctk.CTkFrame(window,width=220)
left.pack(side="left",fill="y")

ctk.CTkLabel(left,text="🤖",font=("Arial",60)).pack(pady=20)
ctk.CTkLabel(left,text="MAYA AI",font=("Arial",24,"bold")).pack()

clock=ctk.CTkLabel(left,text="")
clock.pack()

def tick():
    clock.configure(text=datetime.datetime.now().strftime("%I:%M:%S %p"))
    window.after(1000,tick)
tick()

ctk.CTkButton(left,text="🎤 Start",command=start_assistant).pack(fill="x",padx=15,pady=10)
ctk.CTkButton(left,text="🗑 Clear",command=clear_chat).pack(fill="x",padx=15,pady=5)
ctk.CTkButton(left,text="❌ Exit",command=window.destroy).pack(fill="x",padx=15,pady=5)

status=ctk.CTkLabel(left,text="Status : Ready")
status.pack(side="bottom",pady=20)

right=ctk.CTkFrame(window)
right.pack(side="right",fill="both",expand=True,padx=10,pady=10)

ctk.CTkLabel(right,text="Conversation",font=("Arial",22,"bold")).pack(pady=10)

textbox=ctk.CTkTextbox(right,font=("Consolas",15))
textbox.pack(fill="both",expand=True,padx=10,pady=10)
textbox.configure(state="disabled")

add_message("🤖 MAYA","Hello! I am your AI Assistant.")

window.mainloop()
