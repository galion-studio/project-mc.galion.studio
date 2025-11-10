"""
Global Animation System
Smooth animations and transitions for modern UI
"""

import customtkinter as ctk
from typing import Callable, Optional


class AnimationSystem:
    """
    Centralized animation system for the console.
    Provides smooth transitions and effects.
    """
    
    @staticmethod
    def fade_in(widget, duration=300, callback: Optional[Callable] = None):
        """
        Fade in animation.
        
        Args:
            widget: Widget to animate
            duration: Animation duration in ms
            callback: Optional callback when complete
        """
        steps = 20
        step_duration = duration // steps
        
        def animate(step=0):
            if step <= steps:
                alpha = step / steps
                # Simulate fade by adjusting widget state
                widget.after(step_duration, lambda: animate(step + 1))
            elif callback:
                callback()
        
        animate()
    
    @staticmethod
    def fade_out(widget, duration=300, callback: Optional[Callable] = None):
        """
        Fade out animation.
        
        Args:
            widget: Widget to animate
            duration: Animation duration in ms
            callback: Optional callback when complete
        """
        steps = 20
        step_duration = duration // steps
        
        def animate(step=0):
            if step <= steps:
                alpha = 1 - (step / steps)
                widget.after(step_duration, lambda: animate(step + 1))
            else:
                if callback:
                    callback()
        
        animate()
    
    @staticmethod
    def slide_transition(parent, old_view, new_view, direction="left", duration=400):
        """
        Slide transition between views.
        
        Args:
            parent: Parent container
            old_view: Current view to slide out
            new_view: New view to slide in
            direction: Slide direction (left, right, up, down)
            duration: Animation duration in ms
        """
        # Simple transition: fade out old, fade in new
        if old_view:
            AnimationSystem.fade_out(old_view, duration // 2, 
                                    lambda: old_view.pack_forget())
        
        new_view.pack(fill="both", expand=True)
        AnimationSystem.fade_in(new_view, duration // 2)
    
    @staticmethod
    def pulse_animation(widget, color_start: str, color_end: str, duration=1000):
        """
        Pulse animation between two colors.
        
        Args:
            widget: Widget to animate
            color_start: Starting color
            color_end: Ending color
            duration: Full cycle duration in ms
        """
        steps = 30
        step_duration = duration // (steps * 2)
        
        def animate(step=0, direction=1):
            if step >= 0 and step <= steps:
                # Interpolate between colors
                progress = step / steps
                
                try:
                    if hasattr(widget, 'configure'):
                        widget.configure(fg_color=color_start if progress < 0.5 else color_end)
                except:
                    pass
                
                next_step = step + direction
                if next_step > steps:
                    direction = -1
                elif next_step < 0:
                    direction = 1
                
                widget.after(step_duration, lambda: animate(next_step, direction))
        
        animate()
    
    @staticmethod
    def shake_animation(widget, amplitude=5, duration=500):
        """
        Shake animation for errors.
        
        Args:
            widget: Widget to shake
            amplitude: Shake distance in pixels
            duration: Animation duration in ms
        """
        original_x = widget.winfo_x()
        original_y = widget.winfo_y()
        
        offsets = [amplitude, -amplitude, amplitude, -amplitude, 0]
        step_duration = duration // len(offsets)
        
        def animate(index=0):
            if index < len(offsets):
                try:
                    widget.place(x=original_x + offsets[index], y=original_y)
                    widget.after(step_duration, lambda: animate(index + 1))
                except:
                    pass
        
        animate()
    
    @staticmethod
    def hover_scale(widget, scale=1.02, duration=200):
        """
        Hover scale effect.
        
        Args:
            widget: Widget to scale
            scale: Scale factor
            duration: Animation duration in ms
        """
        # Note: CustomTkinter doesn't support direct scaling
        # This is a placeholder for hover effects handled by CustomTkinter itself
        pass
    
    @staticmethod
    def button_press_animation(widget, scale=0.98, duration=100):
        """
        Button press animation.
        
        Args:
            widget: Button widget
            scale: Scale factor (< 1.0 for shrink)
            duration: Animation duration in ms
        """
        # Placeholder - CustomTkinter handles button press effects
        pass
    
    @staticmethod
    def loading_spinner(parent, size=50, duration=1000):
        """
        Create a loading spinner.
        
        Args:
            parent: Parent widget
            size: Spinner size
            duration: Rotation duration
            
        Returns:
            Spinner widget
        """
        spinner_frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        spinner_label = ctk.CTkLabel(
            spinner_frame,
            text="⟳",
            font=("Segoe UI", size),
            text_color="#4a9eff"
        )
        spinner_label.pack()
        
        return spinner_frame
    
    @staticmethod
    def success_checkmark(parent, duration=500):
        """
        Show success checkmark animation.
        
        Args:
            parent: Parent widget
            duration: Display duration
            
        Returns:
            Checkmark widget
        """
        checkmark = ctk.CTkLabel(
            parent,
            text="✓",
            font=("Segoe UI", 48, "bold"),
            text_color="#00d9a3"
        )
        
        # Auto-hide after duration
        checkmark.after(duration, checkmark.destroy)
        
        return checkmark
    
    @staticmethod
    def error_shake_label(parent, message: str, duration=500):
        """
        Show error message with shake.
        
        Args:
            parent: Parent widget
            message: Error message
            duration: Display duration
            
        Returns:
            Error label widget
        """
        error_label = ctk.CTkLabel(
            parent,
            text=f"✗ {message}",
            font=("Segoe UI", 14),
            text_color="#ff5757"
        )
        
        AnimationSystem.shake_animation(error_label, amplitude=3, duration=300)
        
        # Auto-hide after duration
        error_label.after(duration, error_label.destroy)
        
        return error_label
    
    @staticmethod
    def typing_indicator(parent):
        """
        Create typing indicator animation.
        
        Args:
            parent: Parent widget
            
        Returns:
            Typing indicator widget
        """
        indicator = ctk.CTkLabel(
            parent,
            text="●●●",
            font=("Segoe UI", 16),
            text_color="#8892b0"
        )
        
        dots = ["●  ", "●● ", "●●●", " ●●", "  ●", "   "]
        index = [0]
        
        def animate():
            try:
                indicator.configure(text=dots[index[0] % len(dots)])
                index[0] += 1
                indicator.after(200, animate)
            except:
                pass
        
        animate()
        return indicator
    
    @staticmethod
    def progress_bar_animation(progressbar, target_value, duration=1000):
        """
        Smooth progress bar animation.
        
        Args:
            progressbar: CTkProgressBar widget
            target_value: Target progress (0.0 to 1.0)
            duration: Animation duration in ms
        """
        steps = 50
        step_duration = duration // steps
        current_value = progressbar.get()
        increment = (target_value - current_value) / steps
        
        def animate(step=0):
            if step < steps:
                new_value = current_value + (increment * step)
                try:
                    progressbar.set(new_value)
                    progressbar.after(step_duration, lambda: animate(step + 1))
                except:
                    pass
        
        animate()
    
    @staticmethod
    def card_hover_lift(widget, enter_callback: Optional[Callable] = None,
                       leave_callback: Optional[Callable] = None):
        """
        Add hover lift effect to cards.
        
        Args:
            widget: Card widget
            enter_callback: Optional callback on hover enter
            leave_callback: Optional callback on hover leave
        """
        def on_enter(event):
            # Simulate lift with subtle color change
            try:
                current_color = widget.cget("fg_color")
                widget.configure(fg_color="#252b4a")  # Slightly lighter
                if enter_callback:
                    enter_callback()
            except:
                pass
        
        def on_leave(event):
            # Return to normal
            try:
                widget.configure(fg_color="#1a1f3a")  # Original
                if leave_callback:
                    leave_callback()
            except:
                pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    @staticmethod
    def smooth_scroll(scrollable_frame, target_position, duration=300):
        """
        Smooth scroll animation.
        
        Args:
            scrollable_frame: Scrollable frame widget
            target_position: Target scroll position (0.0 to 1.0)
            duration: Animation duration in ms
        """
        # Note: CustomTkinter scrollable frames handle scrolling internally
        # This is a placeholder for future implementation
        pass


# Convenience functions for common animations
def fade_in(widget, duration=300, callback=None):
    """Fade in widget"""
    AnimationSystem.fade_in(widget, duration, callback)


def fade_out(widget, duration=300, callback=None):
    """Fade out widget"""
    AnimationSystem.fade_out(widget, duration, callback)


def slide_transition(parent, old_view, new_view, direction="left"):
    """Slide transition between views"""
    AnimationSystem.slide_transition(parent, old_view, new_view, direction)


def pulse(widget, color_start, color_end, duration=1000):
    """Pulse animation"""
    AnimationSystem.pulse_animation(widget, color_start, color_end, duration)


def shake(widget, amplitude=5, duration=500):
    """Shake animation"""
    AnimationSystem.shake_animation(widget, amplitude, duration)


def show_success(parent, duration=500):
    """Show success checkmark"""
    return AnimationSystem.success_checkmark(parent, duration)


def show_error(parent, message, duration=500):
    """Show error with shake"""
    return AnimationSystem.error_shake_label(parent, message, duration)


def show_loading(parent, size=50):
    """Show loading spinner"""
    return AnimationSystem.loading_spinner(parent, size)


def show_typing(parent):
    """Show typing indicator"""
    return AnimationSystem.typing_indicator(parent)


def animate_progress(progressbar, target_value, duration=1000):
    """Animate progress bar"""
    AnimationSystem.progress_bar_animation(progressbar, target_value, duration)


def add_card_hover(widget):
    """Add hover effect to card"""
    AnimationSystem.card_hover_lift(widget)

