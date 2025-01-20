import customtkinter as ctk
import requests
import threading
import random
from datetime import datetime

class SpammerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Webhook Master")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        
        # Main container
        self.grid_columnconfigure(0, weight=1)
        
        # Webhook URL input
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Webhook URL", width=400)
        self.url_entry.grid(pady=20)
        
        # Message input
        self.message_text = ctk.CTkTextbox(self, width=400, height=100)
        self.message_text.grid(pady=20)
        
        # Controls frame
        controls = ctk.CTkFrame(self)
        controls.grid(pady=20)
        
        self.delay_entry = ctk.CTkEntry(controls, placeholder_text="Delay (seconds)", width=100)
        self.delay_entry.pack(side="left", padx=5)
        
        self.count_entry = ctk.CTkEntry(controls, placeholder_text="Count", width=100)
        self.count_entry.pack(side="left", padx=5)
        
        # Buttons
        self.start_btn = ctk.CTkButton(self, text="Start Spamming", command=self.start_spam)
        self.start_btn.grid(pady=10)
        
        # Status
        self.status = ctk.CTkLabel(self, text="Ready")
        self.status.grid(pady=10)
        
        # Log
        self.log = ctk.CTkTextbox(self, width=400, height=150)
        self.log.grid(pady=20)
        
    def log_message(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{timestamp}] {msg}\n")
        self.log.see("end")
        
    def spam_thread(self):
        webhook = self.url_entry.get()
        message = self.message_text.get("1.0", "end-1c")
        delay = float(self.delay_entry.get() or 0.5)
        count = int(self.count_entry.get() or 10)
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        for i in range(count):
            try:
                payload = {
                    "content": message,
                    "username": f"Spammer-{random.randint(1000,9999)}"
                }
                
                response = requests.post(webhook, json=payload, headers=headers)
                
                if response.status_code == 204:
                    self.log_message(f"Message {i+1} sent successfully!")
                else:
                    self.log_message(f"Failed to send message {i+1}: {response.status_code}")
                    
            except Exception as e:
                self.log_message(f"Error: {str(e)}")
                
            threading.Event().wait(delay)
            
        self.status.configure(text="Ready")
        self.start_btn.configure(state="normal")
        
    def start_spam(self):
        self.start_btn.configure(state="disabled")
        self.status.configure(text="Spamming...")
        threading.Thread(target=self.spam_thread).start()

if __name__ == "__main__":
    app = SpammerGUI()
    app.mainloop()

