import customtkinter as ctk

# Custom color schemes
COLORS = {
    'primary': '#4a9eff',
    'primary_dark': '#357ae8',
    'success': '#00c853',
    'warning': '#ff9800',
    'danger': '#d32f2f',
    'dark_bg': '#1a1a1a',
    'darker_bg': '#0d0d0d',
    'card_bg': '#1f1f1f',
    'text_primary': '#ffffff',
    'text_secondary': '#888888',
}

def apply_custom_theme():
    """Áp dụng theme tùy chỉnh"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Custom button style
    ctk.CTkButton.configure(
        corner_radius=10,
        border_width=0,
        font=ctk.CTkFont(size=14)
    )
    
    # Custom entry style
    ctk.CTkEntry.configure(
        corner_radius=10,
        border_width=1,
        font=ctk.CTkFont(size=14)
    )
    
    # Custom frame style
    ctk.CTkFrame.configure(
        corner_radius=15,
        border_width=0
    )