import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import random
import string
from datetime import datetime
import json
import os

class DigitalLockSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 THE VAULT - Advanced Digital Lock System")
        self.root.geometry("800x850")
        self.root.configure(bg='#0f1b2e')
        self.root.resizable(True, True)
        
        # Initialize entry fields first
        self.old_pass_entry = None
        self.new_pass_entry = None
        self.confirm_pass_entry = None
        self.attempts_var = None
        self.lockout_var = None
        self.audio_var = None
        self.haptic_var = None
        
        # Center the window
        self.center_window()
        
        # Initialize system
        self.password = "1234"
        self.attempts = 0
        self.max_attempts = 3
        self.is_locked = False
        self.current_input = ""
        self.lockout_time = 30  # seconds
        self.audio_feedback = True
        self.haptic_feedback = True
        
        # Load settings and logs
        self.settings_file = "lock_settings.json"
        self.log_file = "access_log.txt"
        self.load_settings()
        
        # Create sound effects
        self.create_sounds()
        
        # Create modern interface
        self.create_main_interface()
        
        # Start security monitoring
        self.security_monitor()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_sounds(self):
        """Create sound feedback system"""
        try:
            import winsound
            self.sound_enabled = True
        except ImportError:
            self.sound_enabled = False
    
    def play_sound(self, sound_type):
        """Play different sounds for feedback"""
        if not self.sound_enabled or not self.audio_feedback:
            return
            
        try:
            import winsound
            sounds = {
                'click': 1000,
                'success': 2000,
                'error': 500,
                'lock': 300
            }
            frequency = sounds.get(sound_type, 1000)
            duration = 100 if sound_type == 'click' else 300
            winsound.Beep(frequency, duration)
        except:
            pass
    
    def create_main_interface(self):
        # Modern gradient background
        self.canvas = tk.Canvas(self.root, bg='#0f1b2e', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Create gradient background
        self.draw_gradient()
        
        # Main container with glass morphism effect
        self.main_frame = tk.Frame(self.canvas, bg='#1e2a3e', relief='flat')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=750, height=800)
        
        # Title with modern design
        title_frame = tk.Frame(self.main_frame, bg='#1e2a3e')
        title_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = tk.Label(title_frame, 
                             text="🔒 THE VAULT", 
                             font=('Arial', 28, 'bold'),
                             fg='white', bg='#1e2a3e')
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(title_frame,
                                text="Advanced Digital Security System",
                                font=('Arial', 12),
                                fg='#64b5f6', bg='#1e2a3e')
        subtitle_label.pack()
        
        # Create Notebook with modern style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background='#0f1b2e', borderwidth=0)
        self.style.configure('TNotebook.Tab', 
                           font=('Arial', 10, 'bold'),
                           padding=[20, 10],
                           background='#1e2a3e',
                           foreground='white')
        self.style.map('TNotebook.Tab', 
                      background=[('selected', '#64b5f6')],
                      foreground=[('selected', 'white')])
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Create tabs
        self.lock_frame = self.create_glass_frame()
        self.admin_frame = self.create_glass_frame()
        self.arch_frame = self.create_glass_frame()
        self.settings_frame = self.create_glass_frame()
        self.help_frame = self.create_glass_frame()
        
        self.notebook.add(self.lock_frame, text='🔐 Digital Lock')
        self.notebook.add(self.admin_frame, text='⚙️ Admin Panel')
        self.notebook.add(self.arch_frame, text='🏗️ Architecture')
        self.notebook.add(self.settings_frame, text='🎛️ Settings')
        self.notebook.add(self.help_frame, text='❓ Help & FAQ')
        
        self.create_lock_interface()
        self.create_admin_interface()
        self.create_architecture_interface()
        self.create_settings_interface()
        self.create_help_interface()
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
    
    def create_glass_frame(self):
        """Create a glass morphism effect frame"""
        frame = tk.Frame(self.notebook, bg='#1e2a3e', relief='flat', bd=0)
        return frame
    
    def draw_gradient(self):
        """Draw animated gradient background"""
        colors = ['#0f1b2e', '#1a2b3e', '#243b4e', '#2e4a5e']
        for i in range(4):
            color = colors[i]
            self.canvas.create_rectangle(0, i*200, 800, (i+1)*200, 
                                       fill=color, outline=color)
    
    def create_lock_interface(self):
        # Status display with modern design
        self.status_frame = tk.Frame(self.lock_frame, 
                                   bg='#1e2a3e',
                                   relief='flat', bd=1)
        self.status_frame.pack(fill='x', padx=20, pady=15)
        
        self.status_label = tk.Label(self.status_frame, 
                                   text="🔓 SYSTEM READY - Enter 4-digit Password", 
                                   font=('Arial', 14, 'bold'),
                                   fg='#4caf50', 
                                   bg='#1e2a3e',
                                   height=3,
                                   wraplength=600)
        self.status_label.pack(fill='x', padx=15, pady=10)
        
        # Password display with animated cursor
        self.display_frame = tk.Frame(self.lock_frame, 
                                    bg='#1e2a3e')
        self.display_frame.pack(fill='x', padx=20, pady=20)
        
        self.password_display = tk.Label(self.display_frame, 
                                       text="• • • •", 
                                       font=('Courier', 32, 'bold'),
                                       fg='white', 
                                       bg='#0a0f18',
                                       width=15, height=2,
                                       relief='sunken',
                                       bd=3)
        self.password_display.pack(pady=15, padx=50)
        
        # Security indicators
        self.create_security_indicators()
        
        # Enhanced keypad - FIXED: Added all missing buttons
        self.create_enhanced_keypad()
        
        # Control buttons
        self.create_control_buttons()
        
        # Hidden input for keyboard - FIXED: Better keyboard input handling
        self.setup_keyboard_input()
        
        # Start cursor animation
        self.animate_cursor()
    
    def create_security_indicators(self):
        """Create security status indicators"""
        indicator_frame = tk.Frame(self.lock_frame, 
                                 bg='#1e2a3e')
        indicator_frame.pack(fill='x', padx=20, pady=10)
        
        # Attempts counter
        self.attempts_label = tk.Label(indicator_frame,
                                     text=f"🔐 Attempts: {self.attempts}/{self.max_attempts}",
                                     font=('Arial', 11, 'bold'),
                                     fg='#ff9800', 
                                     bg='#1e2a3e')
        self.attempts_label.pack(side='left', padx=10)
        
        # Security level
        self.security_label = tk.Label(indicator_frame,
                                     text="🛡️ Security: ACTIVE",
                                     font=('Arial', 11, 'bold'),
                                     fg='#4caf50',
                                     bg='#1e2a3e')
        self.security_label.pack(side='right', padx=10)
    
    def create_enhanced_keypad(self):
        """Create modern keypad with visual feedback - FIXED: Complete keypad"""
        keypad_frame = tk.Frame(self.lock_frame, 
                              bg='#1e2a3e')
        keypad_frame.pack(pady=20, padx=50)
        
        # Complete keypad layout with all digits and functions
        buttons = [
            ('1', '#64b5f6'), ('2', '#64b5f6'), ('3', '#64b5f6'),
            ('4', '#64b5f6'), ('5', '#64b5f6'), ('6', '#64b5f6'), 
            ('7', '#64b5f6'), ('8', '#64b5f6'), ('9', '#64b5f6'),
            ('⌫', '#ff6b6b'), ('0', '#64b5f6'), ('↩', '#4caf50')
        ]
        
        self.keypad_buttons = {}
        
        row, col = 0, 0
        for text, color in buttons:
            cmd = lambda x=text: self.button_click(x)
            
            btn = tk.Button(keypad_frame, text=text, 
                          font=('Arial', 16, 'bold'),
                          bg=color, fg='white',
                          command=cmd, 
                          width=6, height=3,
                          relief='flat',
                          bd=0,
                          activebackground=self.lighten_color(color),
                          cursor='hand2')
            
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.keypad_buttons[text] = btn
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Make keypad frame responsive
        for i in range(4):
            keypad_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            keypad_frame.grid_columnconfigure(i, weight=1)
    
    def lighten_color(self, color, factor=0.3):
        """Lighten a color for hover effect"""
        # Convert hex to RGB
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        # Lighten
        light_rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        # Convert back to hex
        return f'#{light_rgb[0]:02x}{light_rgb[1]:02x}{light_rgb[2]:02x}'
    
    def create_control_buttons(self):
        """Create control buttons with modern design - FIXED: Better layout"""
        control_frame = tk.Frame(self.lock_frame, 
                               bg='#1e2a3e')
        control_frame.pack(fill='x', padx=20, pady=15)
        
        buttons = [
            ("🔄 Clear All", self.clear_input, '#ff9800'),
            ("🚨 Emergency", self.emergency_lock, '#f44336'),
            ("👁️ Show/Hide", self.toggle_visibility, '#9c27b0'),
            ("🔊 Sound", self.toggle_sound, '#607d8b')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(control_frame, text=text, 
                          font=('Arial', 10, 'bold'),
                          bg=color, fg='white',
                          command=command,
                          width=12, height=2,
                          relief='flat')
            btn.pack(side='left', padx=10, expand=True, fill='x')
        
        # Make control buttons responsive
        for i in range(len(buttons)):
            control_frame.columnconfigure(i, weight=1)
    
    def setup_keyboard_input(self):
        """Setup comprehensive keyboard input handling - FIXED: Better keyboard support"""
        # Create a hidden entry for capturing keyboard input
        self.hidden_entry = tk.Entry(self.lock_frame, font=('Arial', 1), width=1, bg='black', fg='black')
        self.hidden_entry.pack()
        self.hidden_entry.place(x=-100, y=-100)  # Move off-screen
        self.hidden_entry.focus_set()
        
        # Bind all keyboard events
        self.hidden_entry.bind('<KeyPress>', self.handle_keypress)
        
        # Bind focus events to ensure hidden entry always has focus
        self.root.bind('<Button-1>', lambda e: self.hidden_entry.focus_set())
        self.root.bind('<FocusIn>', lambda e: self.hidden_entry.focus_set())
        
        # Additional keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.button_click('↩'))
        self.root.bind('<BackSpace>', lambda e: self.button_click('⌫'))
        self.root.bind('<Delete>', lambda e: self.clear_input())
        
        # Number key bindings
        for i in range(10):
            self.root.bind(str(i), lambda e, num=str(i): self.button_click(num))
    
    def animate_cursor(self):
        """Animate cursor in password display"""
        current_text = self.password_display.cget('text')
        if "|" in current_text:
            new_text = current_text.replace("|", "•")
        else:
            # Find position for cursor
            display_chars = list(current_text.replace("•", "_").replace(" ", ""))
            if len(self.current_input) < 4:
                display_chars[len(self.current_input)] = "|"
            new_text = " ".join(display_chars)
        
        self.password_display.config(text=new_text)
        self.root.after(500, self.animate_cursor)
    
    def create_admin_interface(self):
        # Admin panel with modern design
        title = tk.Label(self.admin_frame, 
                        text="🔧 Administrator Control Panel", 
                        font=('Arial', 18, 'bold'),
                        fg='white', 
                        bg='#1e2a3e')
        title.pack(pady=20)
        
        # Create admin sections
        self.create_password_section()
        self.create_access_log_section()
        self.create_system_info_section()
    
    def create_password_section(self):
        """Password management section"""
        pass_frame = tk.LabelFrame(self.admin_frame, 
                                 text=" Password Management ",
                                 font=('Arial', 12, 'bold'),
                                 fg='white', 
                                 bg='#1e2a3e',
                                 labelanchor='n')
        pass_frame.pack(fill='x', padx=20, pady=10)
        
        # Current password
        tk.Label(pass_frame, text="Current Password:", 
                font=('Arial', 11), fg='white', 
                bg='#1e2a3e').pack(anchor='w', pady=5)
        
        self.current_pass_label = tk.Label(pass_frame, 
                                         text="•" * len(self.password),
                                         font=('Courier', 14, 'bold'),
                                         fg='#ffeb3b', 
                                         bg='#0a0f18',
                                         width=20, height=2)
        self.current_pass_label.pack(pady=5)
        
        # Change password form
        form_frame = tk.Frame(pass_frame, bg='#1e2a3e')
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Initialize entry fields
        self.old_pass_entry = tk.Entry(form_frame, font=('Arial', 12), show='•', width=25)
        self.new_pass_entry = tk.Entry(form_frame, font=('Arial', 12), show='•', width=25)
        self.confirm_pass_entry = tk.Entry(form_frame, font=('Arial', 12), show='•', width=25)
        
        fields = [
            ("Current Password:", self.old_pass_entry, True),
            ("New Password (4 digits):", self.new_pass_entry, True),
            ("Confirm New Password:", self.confirm_pass_entry, True)
        ]
        
        for i, (label_text, entry, show_stars) in enumerate(fields):
            tk.Label(form_frame, text=label_text, 
                    font=('Arial', 10), fg='white', 
                    bg='#1e2a3e').grid(row=i, column=0, sticky='w', pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='ew')
        
        # Password strength indicator
        self.strength_label = tk.Label(form_frame, text="", 
                                      font=('Arial', 9),
                                      fg='white', 
                                      bg='#1e2a3e')
        self.strength_label.grid(row=3, column=1, sticky='w', pady=5)
        
        # Bind strength checker
        self.new_pass_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # Action buttons
        btn_frame = tk.Frame(form_frame, bg='#1e2a3e')
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Change Password", 
                 font=('Arial', 11, 'bold'),
                 bg='#ff9800', fg='white',
                 command=self.change_password,
                 width=15).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Generate Random", 
                 font=('Arial', 11, 'bold'),
                 bg='#2196f3', fg='white',
                 command=self.generate_random_password,
                 width=15).pack(side='left', padx=10)
        
        tk.Button(btn_frame, text="Show Current", 
                 font=('Arial', 11, 'bold'),
                 bg='#9c27b0', fg='white',
                 command=self.toggle_current_password,
                 width=15).pack(side='left', padx=10)
        
        # Admin message
        self.admin_message = tk.Label(pass_frame, text="", 
                                    font=('Arial', 10, 'bold'),
                                    fg='white', 
                                    bg='#1e2a3e')
        self.admin_message.pack(pady=10)
    
    def create_access_log_section(self):
        """Access log display section"""
        log_frame = tk.LabelFrame(self.admin_frame, 
                                text=" Access Log ",
                                font=('Arial', 12, 'bold'),
                                fg='white', 
                                bg='#1e2a3e',
                                labelanchor='n')
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Log display
        log_text_frame = tk.Frame(log_frame, bg='black')
        log_text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_text_frame, 
                              font=('Courier', 9),
                              fg='#00ff00', bg='black',
                              width=60, height=8,
                              wrap='word')
        
        scrollbar = tk.Scrollbar(log_text_frame, orient='vertical', 
                               command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load initial logs
        self.load_access_logs()
        
        # Log controls
        log_controls = tk.Frame(log_frame, bg='#1e2a3e')
        log_controls.pack(fill='x', padx=10, pady=5)
        
        tk.Button(log_controls, text="Refresh Logs", 
                 font=('Arial', 10),
                 bg='#2196f3', fg='white',
                 command=self.load_access_logs,
                 width=12).pack(side='left', padx=5)
        
        tk.Button(log_controls, text="Clear Logs", 
                 font=('Arial', 10),
                 bg='#f44336', fg='white',
                 command=self.clear_logs,
                 width=12).pack(side='left', padx=5)
        
        tk.Button(log_controls, text="Export Logs", 
                 font=('Arial', 10),
                 bg='#4caf50', fg='white',
                 command=self.export_logs,
                 width=12).pack(side='left', padx=5)
    
    def create_system_info_section(self):
        """System information section"""
        info_frame = tk.LabelFrame(self.admin_frame, 
                                 text=" System Information ",
                                 font=('Arial', 12, 'bold'),
                                 fg='white', 
                                 bg='#1e2a3e',
                                 labelanchor='n')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        info_text = f"""
System Status: {'🔒 LOCKED' if self.is_locked else '🔓 UNLOCKED'}
Total Access Attempts: {self.attempts}
Failed Attempts: {self.attempts % self.max_attempts}
Security Level: HIGH
Last Password Change: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Auto-lock: ENABLED
Sound Feedback: {'ENABLED' if self.audio_feedback else 'DISABLED'}
        """
        
        info_label = tk.Label(info_frame, text=info_text,
                            font=('Courier', 10),
                            fg='white', 
                            bg='#1e2a3e',
                            justify='left')
        info_label.pack(pady=10, padx=10)
    
    def create_architecture_interface(self):
        """Create interactive architecture diagram"""
        title = tk.Label(self.arch_frame, 
                        text="🏗️ Computer Architecture Visualization", 
                        font=('Arial', 18, 'bold'),
                        fg='white', 
                        bg='#1e2a3e')
        title.pack(pady=20)
        
        # Interactive architecture diagram
        arch_canvas = tk.Canvas(self.arch_frame, 
                              bg='black',
                              width=700, height=400,
                              highlightthickness=0)
        arch_canvas.pack(pady=20, padx=20)
        
        # Draw architecture components
        components = [
            ("🖥️ INPUT UNIT", 100, 50, "Keypad Scanner\nKeyboard Input"),
            ("💾 REGISTERS", 300, 50, "AX, BX, CX, DX\nTemporary Storage"),
            ("⚡ ALU", 500, 50, "Arithmetic Logic Unit\nPassword Comparison"),
            ("🎮 CONTROL UNIT", 200, 150, "State Machine\nSystem Controller"),
            ("💿 MEMORY", 400, 150, "Password Storage\n0x100 Memory Address"),
            ("🚪 OUTPUT UNIT", 300, 250, "Lock Mechanism\nAccess Control")
        ]
        
        self.arch_components = {}
        
        for name, x, y, description in components:
            # Create component rectangle
            rect = arch_canvas.create_rectangle(x-80, y-30, x+80, y+30,
                                              fill='#1e2a3e', outline='#64b5f6',
                                              width=2)
            
            # Component text
            text = arch_canvas.create_text(x, y, text=name,
                                         font=('Arial', 10, 'bold'),
                                         fill='white')
            
            # Description text (hidden initially)
            desc = arch_canvas.create_text(x, y+60, text=description,
                                         font=('Arial', 8),
                                         fill='#b0b0b0',
                                         state='hidden')
            
            self.arch_components[rect] = (name, desc, False)
            
            # Bind click events
            arch_canvas.tag_bind(rect, '<Button-1>', 
                               lambda e, r=rect: self.toggle_component_info(arch_canvas, r))
            arch_canvas.tag_bind(text, '<Button-1>', 
                               lambda e, r=rect: self.toggle_component_info(arch_canvas, r))
        
        # Draw connections
        connections = [(100, 50, 200, 150), (200, 150, 300, 50),
                      (300, 50, 400, 150), (400, 150, 500, 50),
                      (500, 50, 300, 250), (200, 150, 300, 250)]
        
        for x1, y1, x2, y2 in connections:
            arch_canvas.create_line(x1, y1, x2, y2, 
                                  arrow=tk.LAST, 
                                  fill='#64b5f6', 
                                  width=2,
                                  arrowshape=(8, 10, 5))
        
        # Data flow animation
        self.animate_data_flow(arch_canvas)
    
    def toggle_component_info(self, canvas, component_id):
        """Toggle component information display"""
        name, desc_id, visible = self.arch_components[component_id]
        new_state = 'normal' if not visible else 'hidden'
        canvas.itemconfig(desc_id, state=new_state)
        self.arch_components[component_id] = (name, desc_id, not visible)
    
    def animate_data_flow(self, canvas):
        """Animate data flow through architecture"""
        points = [(100, 50), (200, 150), (300, 50), (400, 150), 
                 (500, 50), (300, 250)]
        
        if hasattr(self, 'data_packet'):
            canvas.delete(self.data_packet)
        
        # Create moving data packet
        self.current_point = 0
        self.animate_packet(canvas, points)
    
    def animate_packet(self, canvas, points):
        """Animate packet movement"""
        if self.current_point >= len(points) - 1:
            self.current_point = 0
        
        x1, y1 = points[self.current_point]
        x2, y2 = points[self.current_point + 1]
        
        # Create packet
        packet = canvas.create_oval(x1-5, y1-5, x1+5, y1+5,
                                  fill='#ffeb3b', outline='#ff9800')
        
        # Animate movement
        self.animate_packet_move(canvas, packet, x1, y1, x2, y2, points)
        
        self.current_point += 1
    
    def animate_packet_move(self, canvas, packet, x1, y1, x2, y2, points):
        """Move packet along path"""
        steps = 20
        for i in range(steps + 1):
            x = x1 + (x2 - x1) * i / steps
            y = y1 + (y2 - y1) * i / steps
            canvas.coords(packet, x-5, y-5, x+5, y+5)
            self.root.update()
            time.sleep(0.05)
        
        canvas.delete(packet)
        self.root.after(100, lambda: self.animate_packet(canvas, points))
    
    def create_settings_interface(self):
        """Create system settings interface"""
        title = tk.Label(self.settings_frame, 
                        text="🎛️ System Settings & Configuration", 
                        font=('Arial', 18, 'bold'),
                        fg='white', 
                        bg='#1e2a3e')
        title.pack(pady=20)
        
        # Security settings
        security_frame = tk.LabelFrame(self.settings_frame, 
                                     text=" Security Settings ",
                                     font=('Arial', 12, 'bold'),
                                     fg='white', 
                                     bg='#1e2a3e',
                                     labelanchor='n')
        security_frame.pack(fill='x', padx=20, pady=10)
        
        # Max attempts setting
        attempts_frame = tk.Frame(security_frame, bg='#1e2a3e')
        attempts_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(attempts_frame, text="Max Attempts Before Lockout:", 
                font=('Arial', 11), fg='white', 
                bg='#1e2a3e').pack(side='left')
        
        self.attempts_var = tk.StringVar(value=str(self.max_attempts))
        attempts_spinbox = tk.Spinbox(attempts_frame, 
                                    from_=1, to=10,
                                    textvariable=self.attempts_var,
                                    font=('Arial', 11),
                                    width=5,
                                    command=self.update_max_attempts)
        attempts_spinbox.pack(side='right', padx=10)
        
        # Lockout time setting
        lockout_frame = tk.Frame(security_frame, bg='#1e2a3e')
        lockout_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(lockout_frame, text="Lockout Duration (seconds):", 
                font=('Arial', 11), fg='white', 
                bg='#1e2a3e').pack(side='left')
        
        self.lockout_var = tk.StringVar(value=str(self.lockout_time))
        lockout_spinbox = tk.Spinbox(lockout_frame, 
                                   from_=10, to=300,
                                   textvariable=self.lockout_var,
                                   font=('Arial', 11),
                                   width=5,
                                   command=self.update_lockout_time)
        lockout_spinbox.pack(side='right', padx=10)
        
        # Feedback settings
        feedback_frame = tk.LabelFrame(self.settings_frame, 
                                     text=" User Feedback ",
                                     font=('Arial', 12, 'bold'),
                                     fg='white', 
                                     bg='#1e2a3e',
                                     labelanchor='n')
        feedback_frame.pack(fill='x', padx=20, pady=10)
        
        self.audio_var = tk.BooleanVar(value=self.audio_feedback)
        audio_cb = tk.Checkbutton(feedback_frame, 
                                text="Enable Audio Feedback",
                                variable=self.audio_var,
                                font=('Arial', 11),
                                fg='white', 
                                bg='#1e2a3e',
                                selectcolor='#1e2a3e',
                                command=self.toggle_audio_feedback)
        audio_cb.pack(anchor='w', padx=10, pady=5)
        
        self.haptic_var = tk.BooleanVar(value=self.haptic_feedback)
        haptic_cb = tk.Checkbutton(feedback_frame, 
                                 text="Enable Haptic Feedback (Visual)",
                                 variable=self.haptic_var,
                                 font=('Arial', 11),
                                 fg='white', 
                                 bg='#1e2a3e',
                                 selectcolor='#1e2a3e',
                                 command=self.toggle_haptic_feedback)
        haptic_cb.pack(anchor='w', padx=10, pady=5)
        
        # System actions
        action_frame = tk.LabelFrame(self.settings_frame, 
                                   text=" System Actions ",
                                   font=('Arial', 12, 'bold'),
                                   fg='white', 
                                   bg='#1e2a3e',
                                   labelanchor='n')
        action_frame.pack(fill='x', padx=20, pady=10)
        
        action_buttons = [
            ("Reset System", self.reset_system, '#ff9800'),
            ("Backup Settings", self.backup_settings, '#2196f3'),
            ("Restore Settings", self.restore_settings, '#4caf50'),
            ("Factory Reset", self.factory_reset, '#f44336')
        ]
        
        btn_frame = tk.Frame(action_frame, bg='#1e2a3e')
        btn_frame.pack(pady=10)
        
        for text, command, color in action_buttons:
            tk.Button(btn_frame, text=text, 
                     font=('Arial', 10, 'bold'),
                     bg=color, fg='white',
                     command=command,
                     width=15, height=2).pack(side='left', padx=10)
    
    def create_help_interface(self):
        """Create comprehensive help and FAQ section"""
        title = tk.Label(self.help_frame, 
                        text="❓ Help Center & Frequently Asked Questions", 
                        font=('Arial', 18, 'bold'),
                        fg='white', 
                        bg='#1e2a3e')
        title.pack(pady=20)
        
        # Create notebook for help sections
        help_notebook = ttk.Notebook(self.help_frame)
        help_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Quick Start Guide
        quickstart_frame = tk.Frame(help_notebook, bg='#1e2a3e')
        help_notebook.add(quickstart_frame, text='🚀 Quick Start')
        
        quickstart_text = """
QUICK START GUIDE:

1. BASIC OPERATION:
   • Enter 4-digit password using keypad or keyboard
   • Press 'Enter' or ↩ button to submit
   • Use 'Clear' to reset input

2. SECURITY FEATURES:
   • 3 attempts before temporary lockout
   • Visual and audio feedback
   • Access logging

3. ADMIN FUNCTIONS:
   • Change password in Admin Panel
   • View access logs
   • Configure system settings

4. TROUBLESHOOTING:
   • If locked out, wait 30 seconds
   • Check caps lock is off
   • Ensure numeric input only

5. KEYBOARD SHORTCUTS:
   • Enter: Submit password
   • Backspace: Delete last digit
   • Escape: Clear all input
   • F1: Show this help
        """
        
        quickstart_label = tk.Label(quickstart_frame, text=quickstart_text,
                                  font=('Courier', 10),
                                  fg='white', 
                                  bg='#1e2a3e',
                                  justify='left')
        quickstart_label.pack(pady=10, padx=10, anchor='w')
        
        # FAQ Section
        faq_frame = tk.Frame(help_notebook, bg='#1e2a3e')
        help_notebook.add(faq_frame, text='❔ FAQ')
        
        faqs = [
            ("Q: What if I forget the password?", 
             "A: Contact system administrator. There's no password recovery for security reasons."),
            
            ("Q: Why is the system locked?", 
             "A: System locks after 3 failed attempts. Wait 30 seconds or contact admin."),
            
            ("Q: Can I use letters in the password?", 
             "A: No, only 4-digit numeric passwords are supported for security."),
            
            ("Q: How do I change settings?", 
             "A: Use the Settings tab to configure security and feedback options."),
            
            ("Q: Where are logs stored?", 
             "A: Logs are stored in 'access_log.txt' and can be exported from Admin Panel."),
            
            ("Q: Is there a master override?", 
             "A: No master override exists for security. Contact administrator if needed.")
        ]
        
        faq_canvas = tk.Canvas(faq_frame, bg='#1e2a3e',
                              highlightthickness=0)
        scrollbar = tk.Scrollbar(faq_frame, orient='vertical', 
                               command=faq_canvas.yview)
        scrollable_frame = tk.Frame(faq_canvas, bg='#1e2a3e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: faq_canvas.configure(scrollregion=faq_canvas.bbox("all"))
        )
        
        faq_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        faq_canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, (question, answer) in enumerate(faqs):
            q_label = tk.Label(scrollable_frame, text=question,
                             font=('Arial', 11, 'bold'),
                             fg='#64b5f6', 
                             bg='#1e2a3e',
                             justify='left', wraplength=600)
            q_label.pack(anchor='w', padx=10, pady=(10, 0))
            
            a_label = tk.Label(scrollable_frame, text=answer,
                             font=('Arial', 10),
                             fg='white', 
                             bg='#1e2a3e',
                             justify='left', wraplength=600)
            a_label.pack(anchor='w', padx=20, pady=(0, 10))
        
        faq_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Troubleshooting Guide
        trouble_frame = tk.Frame(help_notebook, bg='#1e2a3e')
        help_notebook.add(trouble_frame, text='🔧 Troubleshooting')
        
        trouble_text = """
COMMON ISSUES & SOLUTIONS:

🔒 SYSTEM WON'T UNLOCK:
• Verify password is correct
• Check if system is temporarily locked
• Ensure you're using numeric input only

🎹 KEYPAD NOT RESPONDING:
• Try keyboard input instead
• Check if system is locked
• Restart the application

🔊 NO SOUND FEEDBACK:
• Check audio settings in Settings tab
• Verify system volume is not muted
• Check if audio is enabled

📱 DISPLAY ISSUES:
• Resize window if elements are missing
• Check system display scaling
• Restart the application

⚡ PERFORMANCE ISSUES:
• Close other applications
• Check system resources
• Reduce animation effects in settings

🆘 EMERGENCY PROCEDURES:
• Use Emergency Lock for immediate security
• Contact administrator if locked out
• Document any error messages
        """
        
        trouble_label = tk.Label(trouble_frame, text=trouble_text,
                               font=('Courier', 10),
                               fg='white', 
                               bg='#1e2a3e',
                               justify='left')
        trouble_label.pack(pady=10, padx=10, anchor='w')
    
    def button_click(self, value):
        """Handle button clicks with enhanced feedback - FIXED: Better keyboard integration"""
        if self.is_locked:
            self.play_sound('error')
            return
            
        self.play_sound('click')
        
        if value == '⌫':
            self.current_input = self.current_input[:-1]
        elif value == '↩':
            self.check_password()
        elif value.isdigit() and len(self.current_input) < 4:
            self.current_input += value
            # Visual feedback for button press
            if value in self.keypad_buttons:
                self.animate_button_press(self.keypad_buttons[value])
        
        self.update_display()
        
        # Ensure hidden entry maintains focus for keyboard input
        self.hidden_entry.focus_set()
    
    def animate_button_press(self, button):
        """Animate button press for better feedback"""
        original_bg = button.cget('bg')
        button.config(bg='white', fg=original_bg)
        self.root.after(150, lambda: button.config(bg=original_bg, fg='white'))
    
    def handle_keypress(self, event):
        """Handle keyboard input with enhanced features - FIXED: Better key handling"""
        if self.is_locked:
            self.play_sound('error')
            return
            
        key = event.char
        keysym = event.keysym
        
        # Handle number keys
        if key.isdigit() and len(self.current_input) < 4:
            self.current_input += key
            self.play_sound('click')
            self.update_display()
        
        # Handle special keys
        elif keysym in ['Return', 'KP_Enter']:
            self.button_click('↩')
        elif keysym in ['BackSpace', 'Delete']:
            self.button_click('⌫')
        elif keysym == 'Escape':
            self.clear_input()
        elif keysym == 'F1':
            self.notebook.select(4)  # Switch to help tab
        
        # Clear the hidden entry after each keypress to avoid accumulation
        self.hidden_entry.delete(0, tk.END)
    
    def update_display(self):
        """Update password display with enhanced visuals"""
        display_chars = []
        for i in range(4):
            if i < len(self.current_input):
                display_chars.append("•")
            else:
                display_chars.append("•")
        
        display_text = " ".join(display_chars)
        self.password_display.config(text=display_text)
        
        # Update attempts counter
        self.attempts_label.config(
            text=f"🔐 Attempts: {self.attempts % self.max_attempts}/{self.max_attempts}"
        )
    
    def clear_input(self):
        """Clear current input"""
        self.current_input = ""
        self.update_display()
        self.hidden_entry.focus_set()
        self.play_sound('click')
    
    def check_password(self):
        """Enhanced password checking with comprehensive logging"""
        if len(self.current_input) != 4:
            self.show_message("❌ Password must be exactly 4 digits!", "error")
            self.log_access("FAILED", "Invalid length")
            return
        
        if self.current_input == self.password:
            self.show_message("✅ ACCESS GRANTED! Door Unlocked!", "success")
            self.log_access("SUCCESS", "Correct password")
            self.attempts = 0
            self.is_locked = False
            self.security_label.config(text="🛡️ Security: ACTIVE", fg='#4caf50')
            self.play_sound('success')
            
            # Enhanced success animation
            self.animate_success()
            
            # Reset after delay
            self.root.after(3000, self.reset_after_success)
        else:
            self.attempts += 1
            remaining = self.max_attempts - (self.attempts % self.max_attempts)
            
            self.log_access("FAILED", f"Wrong password: {self.current_input}")
            
            if self.attempts % self.max_attempts == 0:
                self.show_message("🚨 SYSTEM LOCKED! Too many failed attempts!", "error")
                self.log_access("LOCKED", f"Too many attempts: {self.attempts}")
                self.is_locked = True
                self.security_label.config(text="🚨 Security: LOCKED", fg='#f44336')
                self.play_sound('lock')
                
                # Start lockout timer
                self.start_lockout_timer()
            else:
                self.show_message(f"❌ Access Denied! {remaining} attempts remaining.", "error")
                self.play_sound('error')
            
            self.current_input = ""
            self.update_display()
        
        self.hidden_entry.focus_set()
    
    def animate_success(self):
        """Animate success feedback"""
        original_bg = self.password_display.cget('bg')
        original_fg = self.password_display.cget('fg')
        
        # Flash green
        for i in range(3):
            self.password_display.config(bg='#4caf50', fg='white')
            self.root.update()
            time.sleep(0.2)
            self.password_display.config(bg=original_bg, fg=original_fg)
            self.root.update()
            time.sleep(0.2)
    
    def start_lockout_timer(self):
        """Start countdown timer for lockout"""
        if not self.is_locked:
            return
            
        remaining = self.lockout_time
        self.lockout_timer(remaining)
    
    def lockout_timer(self, seconds):
        """Update lockout timer display"""
        if seconds > 0 and self.is_locked:
            mins, secs = divmod(seconds, 60)
            timer_text = f"⏰ Lockout: {mins:02d}:{secs:02d}"
            self.status_label.config(text=timer_text, fg='#ff9800')
            self.root.after(1000, lambda: self.lockout_timer(seconds - 1))
        elif self.is_locked:
            self.is_locked = False
            self.attempts = 0
            self.show_message("🔓 System Ready - Enter 4-digit Password", "ready")
            self.security_label.config(text="🛡️ Security: ACTIVE", fg='#4caf50')
    
    def reset_after_success(self):
        """Reset system after successful access"""
        self.current_input = ""
        self.update_display()
        self.show_message("🔓 System Ready - Enter 4-digit Password", "ready")
    
    def show_message(self, message, msg_type):
        """Show status messages with enhanced styling"""
        colors = {
            "success": "#4caf50",
            "error": "#f44336", 
            "ready": "#64b5f6",
            "warning": "#ff9800"
        }
        
        self.status_label.config(
            text=message, 
            fg=colors.get(msg_type, "#64b5f6")
        )
        
        # Add message to log if it's important
        if msg_type in ['success', 'error']:
            self.log_access("SYSTEM", message)
    
    def log_access(self, event_type, details):
        """Log access attempts with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {event_type}: {details}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Logging error: {e}")
        
        # Update admin log display if on admin tab
        if hasattr(self, 'log_text'):
            self.load_access_logs()
    
    def load_access_logs(self):
        """Load and display access logs"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    logs = f.read()
                
                self.log_text.config(state='normal')
                self.log_text.delete('1.0', tk.END)
                self.log_text.insert('1.0', logs)
                self.log_text.config(state='disabled')
                self.log_text.see(tk.END)
            else:
                self.log_text.config(state='normal')
                self.log_text.delete('1.0', tk.END)
                self.log_text.insert('1.0', "No access logs found.")
                self.log_text.config(state='disabled')
        except Exception as e:
            self.log_text.config(state='normal')
            self.log_text.delete('1.0', tk.END)
            self.log_text.insert('1.0', f"Error loading logs: {e}")
            self.log_text.config(state='disabled')
    
    def clear_logs(self):
        """Clear access logs with confirmation"""
        if messagebox.askyesno("Confirm", "Clear all access logs?"):
            try:
                open(self.log_file, 'w').close()
                self.load_access_logs()
                self.admin_message.config(text="✅ Logs cleared successfully!", fg="#4caf50")
            except Exception as e:
                self.admin_message.config(text=f"❌ Error clearing logs: {e}", fg="#f44336")
    
    def export_logs(self):
        """Export logs to file"""
        try:
            export_file = f"access_log_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(self.log_file, 'r', encoding='utf-8') as source:
                with open(export_file, 'w', encoding='utf-8') as target:
                    target.write(source.read())
            self.admin_message.config(text=f"✅ Logs exported to {export_file}", fg="#4caf50")
        except Exception as e:
            self.admin_message.config(text=f"❌ Export failed: {e}", fg="#f44336")
    
    def change_password(self):
        """Enhanced password change with validation"""
        # Check if entries exist
        if not hasattr(self, 'old_pass_entry') or self.old_pass_entry is None:
            self.admin_message.config(text="❌ System not ready. Please try again.", fg="#f44336")
            return
            
        old_pass = self.old_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        if old_pass != self.password:
            self.admin_message.config(text="❌ Current password is incorrect!", fg="#f44336")
            self.play_sound('error')
            return
        
        if len(new_pass) != 4 or not new_pass.isdigit():
            self.admin_message.config(text="❌ New password must be 4 digits!", fg="#f44336")
            self.play_sound('error')
            return
        
        if new_pass != confirm_pass:
            self.admin_message.config(text="❌ New passwords don't match!", fg="#f44336")
            self.play_sound('error')
            return
        
        # Check if new password is too simple
        if self.is_weak_password(new_pass):
            if not messagebox.askyesno("Warning", 
                                     "This password may be easy to guess.\nDo you want to use it anyway?"):
                return
        
        self.password = new_pass
        self.current_pass_label.config(text="•" * len(self.password))
        self.admin_message.config(text="✅ Password changed successfully!", fg="#4caf50")
        self.log_access("PASSWORD_CHANGE", "Password updated successfully")
        self.play_sound('success')
        
        # Clear entries
        self.old_pass_entry.delete(0, tk.END)
        self.new_pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.delete(0, tk.END)
    
    def is_weak_password(self, password):
        """Check if password is weak"""
        weak_patterns = ['0000', '1111', '1234', '4321', '9999']
        return password in weak_patterns
    
    def check_password_strength(self, event=None):
        """Check and display password strength"""
        if not hasattr(self, 'new_pass_entry') or self.new_pass_entry is None:
            return
            
        password = self.new_pass_entry.get()
        
        if len(password) == 0:
            self.strength_label.config(text="", fg="white")
        elif len(password) < 4:
            self.strength_label.config(text="Too short", fg="#f44336")
        elif self.is_weak_password(password):
            self.strength_label.config(text="Weak - Easy to guess", fg="#ff9800")
        else:
            self.strength_label.config(text="Strong", fg="#4caf50")
    
    def generate_random_password(self):
        """Generate a random 4-digit password"""
        if not hasattr(self, 'new_pass_entry') or self.new_pass_entry is None:
            return
            
        new_password = ''.join(random.choices(string.digits, k=4))
        self.new_pass_entry.delete(0, tk.END)
        self.new_pass_entry.insert(0, new_password)
        self.confirm_pass_entry.delete(0, tk.END)
        self.confirm_pass_entry.insert(0, new_password)
        self.check_password_strength()
        self.admin_message.config(text="🔒 Random password generated!", fg="#2196f3")
    
    def toggle_current_password(self):
        """Toggle between showing and hiding current password"""
        current_text = self.current_pass_label.cget('text')
        if current_text.startswith('•'):
            self.current_pass_label.config(text=self.password)
        else:
            self.current_pass_label.config(text='•' * len(self.password))
    
    def toggle_visibility(self):
        """Toggle password visibility in lock interface"""
        # This would toggle between showing • and actual digits
        self.admin_message.config(text="👁️ Visibility toggle - Feature in development", fg="#9c27b0")
    
    def emergency_lock(self):
        """Immediately lock the system"""
        self.is_locked = True
        self.attempts = self.max_attempts
        self.show_message("🚨 EMERGENCY LOCK ACTIVATED!", "error")
        self.security_label.config(text="🚨 Security: EMERGENCY LOCK", fg='#f44336')
        self.log_access("EMERGENCY", "Emergency lock activated by user")
        self.play_sound('lock')
    
    def toggle_sound(self):
        """Toggle sound feedback"""
        self.audio_feedback = not self.audio_feedback
        status = "ENABLED" if self.audio_feedback else "DISABLED"
        self.show_message(f"🔊 Sound feedback {status}", "ready")
        self.save_settings()
    
    def toggle_audio_feedback(self):
        """Toggle audio feedback from settings"""
        if hasattr(self, 'audio_var') and self.audio_var is not None:
            self.audio_feedback = self.audio_var.get()
            self.save_settings()
    
    def toggle_haptic_feedback(self):
        """Toggle haptic feedback from settings"""
        if hasattr(self, 'haptic_var') and self.haptic_var is not None:
            self.haptic_feedback = self.haptic_var.get()
            self.save_settings()
    
    def update_max_attempts(self):
        """Update maximum attempts from settings"""
        if hasattr(self, 'attempts_var') and self.attempts_var is not None:
            try:
                self.max_attempts = int(self.attempts_var.get())
                self.save_settings()
            except ValueError:
                pass
    
    def update_lockout_time(self):
        """Update lockout time from settings"""
        if hasattr(self, 'lockout_var') and self.lockout_var is not None:
            try:
                self.lockout_time = int(self.lockout_var.get())
                self.save_settings()
            except ValueError:
                pass
    
    def reset_system(self):
        """Reset system to default state"""
        if messagebox.askyesno("Confirm Reset", "Reset system to default state?"):
            self.attempts = 0
            self.is_locked = False
            self.current_input = ""
            self.update_display()
            self.show_message("🔓 System Ready - Enter 4-digit Password", "ready")
            self.security_label.config(text="🛡️ Security: ACTIVE", fg='#4caf50')
            self.log_access("SYSTEM", "System reset to default state")
    
    def backup_settings(self):
        """Backup system settings"""
        try:
            backup_data = {
                'password': self.password,
                'max_attempts': self.max_attempts,
                'lockout_time': self.lockout_time,
                'audio_feedback': self.audio_feedback,
                'haptic_feedback': self.haptic_feedback
            }
            
            with open('system_backup.json', 'w') as f:
                json.dump(backup_data, f)
            
            self.admin_message.config(text="✅ Settings backed up successfully!", fg="#4caf50")
        except Exception as e:
            self.admin_message.config(text=f"❌ Backup failed: {e}", fg="#f44336")
    
    def restore_settings(self):
        """Restore system settings from backup"""
        try:
            if os.path.exists('system_backup.json'):
                with open('system_backup.json', 'r') as f:
                    backup_data = json.load(f)
                
                self.password = backup_data.get('password', self.password)
                self.max_attempts = backup_data.get('max_attempts', self.max_attempts)
                self.lockout_time = backup_data.get('lockout_time', self.lockout_time)
                self.audio_feedback = backup_data.get('audio_feedback', self.audio_feedback)
                self.haptic_feedback = backup_data.get('haptic_feedback', self.haptic_feedback)
                
                # Update UI
                self.current_pass_label.config(text='•' * len(self.password))
                if hasattr(self, 'attempts_var') and self.attempts_var is not None:
                    self.attempts_var.set(str(self.max_attempts))
                if hasattr(self, 'lockout_var') and self.lockout_var is not None:
                    self.lockout_var.set(str(self.lockout_time))
                if hasattr(self, 'audio_var') and self.audio_var is not None:
                    self.audio_var.set(self.audio_feedback)
                if hasattr(self, 'haptic_var') and self.haptic_var is not None:
                    self.haptic_var.set(self.haptic_feedback)
                
                self.admin_message.config(text="✅ Settings restored successfully!", fg="#4caf50")
            else:
                self.admin_message.config(text="❌ No backup file found!", fg="#f44336")
        except Exception as e:
            self.admin_message.config(text=f"❌ Restore failed: {e}", fg="#f44336")
    
    def factory_reset(self):
        """Factory reset system with confirmation"""
        if messagebox.askyesno("Factory Reset", 
                             "This will reset ALL settings and logs!\nAre you absolutely sure?",
                             icon='warning'):
            if messagebox.askyesno("Confirm Again", 
                                 "This cannot be undone! Continue?"):
                try:
                    # Reset to defaults
                    self.password = "1234"
                    self.max_attempts = 3
                    self.lockout_time = 30
                    self.audio_feedback = True
                    self.haptic_feedback = True
                    self.attempts = 0
                    self.is_locked = False
                    self.current_input = ""
                    
                    # Update UI
                    self.current_pass_label.config(text='•' * len(self.password))
                    if hasattr(self, 'attempts_var') and self.attempts_var is not None:
                        self.attempts_var.set(str(self.max_attempts))
                    if hasattr(self, 'lockout_var') and self.lockout_var is not None:
                        self.lockout_var.set(str(self.lockout_time))
                    if hasattr(self, 'audio_var') and self.audio_var is not None:
                        self.audio_var.set(self.audio_feedback)
                    if hasattr(self, 'haptic_var') and self.haptic_var is not None:
                        self.haptic_var.set(self.haptic_feedback)
                    self.update_display()
                    self.show_message("🔓 System Ready - Enter 4-digit Password", "ready")
                    
                    # Clear logs
                    open(self.log_file, 'w').close()
                    self.load_access_logs()
                    
                    self.admin_message.config(text="✅ Factory reset complete!", fg="#4caf50")
                    self.log_access("SYSTEM", "Factory reset performed")
                    
                except Exception as e:
                    self.admin_message.config(text=f"❌ Reset failed: {e}", fg="#f44336")
    
    def load_settings(self):
        """Load system settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                
                self.password = settings.get('password', self.password)
                self.max_attempts = settings.get('max_attempts', self.max_attempts)
                self.lockout_time = settings.get('lockout_time', self.lockout_time)
                self.audio_feedback = settings.get('audio_feedback', self.audio_feedback)
                self.haptic_feedback = settings.get('haptic_feedback', self.haptic_feedback)
        except Exception as e:
            print(f"Settings load error: {e}")
    
    def save_settings(self):
        """Save system settings to file"""
        try:
            settings = {
                'password': self.password,
                'max_attempts': self.max_attempts,
                'lockout_time': self.lockout_time,
                'audio_feedback': self.audio_feedback,
                'haptic_feedback': self.haptic_feedback
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Settings save error: {e}")
    
    def security_monitor(self):
        """Continuous security monitoring"""
        # Check for security issues
        if self.attempts >= self.max_attempts * 2:  # Multiple lockouts
            self.log_access("SECURITY", f"Multiple lockouts detected: {self.attempts}")
        
        # Schedule next check
        self.root.after(10000, self.security_monitor)  # Check every 10 seconds
    
    def on_tab_change(self, event):
        """Handle tab change events"""
        current_tab = self.notebook.index(self.notebook.select())
        tab_names = ['Lock', 'Admin', 'Architecture', 'Settings', 'Help']
        self.log_access("NAVIGATION", f"Switched to {tab_names[current_tab]} tab")
        
        # Refresh data when switching to admin tab
        if current_tab == 1:  # Admin tab
            self.load_access_logs()

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = DigitalLockSystem(root)
        
        # Set application icon (if available)
        try:
            root.iconbitmap('lock_icon.ico')  # You can create this icon file
        except:
            pass
        
        # Bind global shortcuts
        root.bind('<F1>', lambda e: app.notebook.select(4))  # F1 for help
        root.bind('<Escape>', lambda e: app.clear_input())   # ESC to clear
        
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"The application encountered an error:\n{e}")

if __name__ == "__main__":
    main() 