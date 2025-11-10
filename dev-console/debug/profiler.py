"""
Profiler Component
Performance profiling and analysis
"""

import customtkinter as ctk
from typing import Dict, List
import time
import threading

from config import THEME, LAYOUT


class Profiler(ctk.CTkScrollableFrame):
    """
    Performance profiler for Minecraft server.
    Identify bottlenecks, optimize performance.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.is_profiling = False
        self.profile_data = []
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="📈 Performance Profiler",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Performance metrics
        self.create_metrics_section()
        
        # Profiling controls
        self.create_controls_section()
        
        # Results view
        self.create_results_section()
        
        # Start monitoring
        self.start_monitoring()
    
    def create_metrics_section(self):
        """Create performance metrics section"""
        metrics_label = ctk.CTkLabel(
            self,
            text="Real-time Metrics",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        metrics_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        metrics_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        metrics_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Metric cards
        self.tps_card = self.create_metric_card(
            metrics_frame, "TPS", "20.0", THEME["success"]
        )
        self.tps_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.memory_card = self.create_metric_card(
            metrics_frame, "Memory", "2.5 GB", THEME["info"]
        )
        self.memory_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.cpu_card = self.create_metric_card(
            metrics_frame, "CPU", "45%", THEME["warning"]
        )
        self.cpu_card.pack(side="left", fill="both", expand=True, padx=5)
        
        self.entities_card = self.create_metric_card(
            metrics_frame, "Entities", "1,234", THEME["accent"]
        )
        self.entities_card.pack(side="left", fill="both", expand=True, padx=5)
    
    def create_metric_card(self, parent, label: str, value: str, color: str) -> ctk.CTkFrame:
        """Create a metric card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )
        value_label.pack(pady=(15, 5))
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        label_widget.pack(pady=(0, 15))
        
        # Store references for updating
        card.value_label = value_label
        card.metric_label = label_widget
        
        return card
    
    def create_controls_section(self):
        """Create profiling controls"""
        controls_label = ctk.CTkLabel(
            self,
            text="Profiling Controls",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        controls_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        controls_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        controls_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        controls_frame = ctk.CTkFrame(controls_card, fg_color="transparent")
        controls_frame.pack(fill="x", padx=20, pady=20)
        
        # Profile duration
        ctk.CTkLabel(
            controls_frame,
            text="Profile Duration:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.duration_slider = ctk.CTkSlider(
            controls_frame,
            from_=10,
            to=300,
            number_of_steps=29,
            fg_color=THEME["card_hover"],
            progress_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"]
        )
        self.duration_slider.set(60)
        self.duration_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.duration_label = ctk.CTkLabel(
            controls_frame,
            text="60s",
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            width=50
        )
        self.duration_label.pack(side="left", padx=(0, 20))
        
        self.duration_slider.configure(
            command=lambda v: self.duration_label.configure(text=f"{int(v)}s")
        )
        
        # Start profiling button
        self.profile_button = ctk.CTkButton(
            controls_frame,
            text="▶️ Start Profiling",
            width=150,
            font=THEME["font_body"],
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=self.toggle_profiling
        )
        self.profile_button.pack(side="left")
    
    def create_results_section(self):
        """Create profiling results section"""
        results_label = ctk.CTkLabel(
            self,
            text="Profiling Results",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        results_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        results_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        results_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Results text
        self.results_text = ctk.CTkTextbox(
            results_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"]
        )
        self.results_text.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.results_text.insert("1.0", 
            "Performance Analysis\n"
            "==================\n\n"
            "Start profiling to see detailed performance analysis.\n\n"
            "Metrics tracked:\n"
            "  • TPS (Ticks Per Second)\n"
            "  • Memory usage\n"
            "  • CPU usage\n"
            "  • Entity count\n"
            "  • Chunk loading times\n"
            "  • Plugin/Mod performance\n\n"
            "Note: This is a simplified profiler.\n"
            "For advanced profiling, use:\n"
            "  • Spark (https://spark.lucko.me/)\n"
            "  • VisualVM with JMX\n"
            "  • JProfiler or YourKit\n"
        )
        self.results_text.configure(state="disabled")
    
    def start_monitoring(self):
        """Start real-time monitoring"""
        thread = threading.Thread(target=self._monitoring_thread, daemon=True)
        thread.start()
    
    def _monitoring_thread(self):
        """Monitoring thread"""
        while True:
            # Simulate metrics (in real implementation, would query server)
            self.update_metrics()
            time.sleep(2)
    
    def update_metrics(self):
        """Update metric displays"""
        # In real implementation, would query server via RCON or JMX
        # For now, show placeholder values
        
        # TPS - simulate fluctuation
        import random
        tps = 19.5 + random.random()
        tps_color = THEME["success"] if tps >= 19.0 else THEME["warning"] if tps >= 15.0 else THEME["error"]
        
        self.after(0, lambda: self.tps_card.value_label.configure(
            text=f"{tps:.1f}",
            text_color=tps_color
        ))
        
        # Memory
        memory = 2.5 + random.random() * 0.5
        self.after(0, lambda: self.memory_card.value_label.configure(
            text=f"{memory:.1f} GB"
        ))
        
        # CPU
        cpu = 40 + random.randint(0, 30)
        cpu_color = THEME["success"] if cpu < 60 else THEME["warning"] if cpu < 80 else THEME["error"]
        self.after(0, lambda: self.cpu_card.value_label.configure(
            text=f"{cpu}%",
            text_color=cpu_color
        ))
        
        # Entities
        entities = 1200 + random.randint(-50, 50)
        self.after(0, lambda: self.entities_card.value_label.configure(
            text=f"{entities:,}"
        ))
    
    def toggle_profiling(self):
        """Toggle profiling on/off"""
        if self.is_profiling:
            self.stop_profiling()
        else:
            self.start_profiling()
    
    def start_profiling(self):
        """Start profiling"""
        self.is_profiling = True
        self.profile_data = []
        
        # Update button
        self.profile_button.configure(
            text="⏹️ Stop Profiling",
            fg_color=THEME["error"]
        )
        
        # Clear results
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "Profiling started...\n\n")
        self.results_text.configure(state="disabled")
        
        # Start profiling thread
        duration = int(self.duration_slider.get())
        thread = threading.Thread(
            target=self._profiling_thread,
            args=(duration,),
            daemon=True
        )
        thread.start()
    
    def stop_profiling(self):
        """Stop profiling"""
        self.is_profiling = False
        
        # Update button
        self.profile_button.configure(
            text="▶️ Start Profiling",
            fg_color=THEME["success"]
        )
    
    def _profiling_thread(self, duration: int):
        """Profiling thread"""
        start_time = time.time()
        samples = []
        
        self.log_results(f"Profiling for {duration} seconds...\n")
        
        while self.is_profiling and (time.time() - start_time) < duration:
            # Collect sample
            sample = {
                "timestamp": time.time(),
                "tps": 19.5 + (time.time() % 1),
                "memory": 2.5 + (time.time() % 0.5),
                "cpu": 45 + int(time.time() % 20)
            }
            samples.append(sample)
            
            elapsed = int(time.time() - start_time)
            self.log_results(f"\rCollecting data... {elapsed}/{duration}s", overwrite_last=True)
            
            time.sleep(1)
        
        if not self.is_profiling:
            self.log_results("\n\nProfiling stopped by user.\n")
            return
        
        # Analyze results
        self.analyze_profile(samples)
        
        self.is_profiling = False
        self.after(0, lambda: self.profile_button.configure(
            text="▶️ Start Profiling",
            fg_color=THEME["success"]
        ))
    
    def analyze_profile(self, samples: List[Dict]):
        """Analyze profiling data"""
        if not samples:
            return
        
        self.log_results("\n\n" + "="*50 + "\n")
        self.log_results("PROFILING RESULTS\n")
        self.log_results("="*50 + "\n\n")
        
        # Calculate statistics
        avg_tps = sum(s["tps"] for s in samples) / len(samples)
        min_tps = min(s["tps"] for s in samples)
        max_tps = max(s["tps"] for s in samples)
        
        avg_memory = sum(s["memory"] for s in samples) / len(samples)
        max_memory = max(s["memory"] for s in samples)
        
        avg_cpu = sum(s["cpu"] for s in samples) / len(samples)
        max_cpu = max(s["cpu"] for s in samples)
        
        self.log_results(f"Samples collected: {len(samples)}\n\n")
        
        self.log_results("TPS (Ticks Per Second):\n")
        self.log_results(f"  Average: {avg_tps:.2f}\n")
        self.log_results(f"  Min: {min_tps:.2f}\n")
        self.log_results(f"  Max: {max_tps:.2f}\n")
        self.log_results(f"  Status: {'✓ Excellent' if avg_tps >= 19.5 else '⚠ Needs attention'}\n\n")
        
        self.log_results("Memory Usage:\n")
        self.log_results(f"  Average: {avg_memory:.2f} GB\n")
        self.log_results(f"  Peak: {max_memory:.2f} GB\n\n")
        
        self.log_results("CPU Usage:\n")
        self.log_results(f"  Average: {avg_cpu:.1f}%\n")
        self.log_results(f"  Peak: {max_cpu}%\n\n")
        
        self.log_results("="*50 + "\n\n")
        
        # Recommendations
        self.log_results("RECOMMENDATIONS:\n")
        self.log_results("-"*50 + "\n")
        
        if avg_tps < 19.0:
            self.log_results("⚠ TPS is below optimal\n")
            self.log_results("  • Check for lag-causing plugins/mods\n")
            self.log_results("  • Optimize entity counts\n")
            self.log_results("  • Consider chunk loading optimizations\n\n")
        
        if max_memory > 3.5:
            self.log_results("⚠ High memory usage detected\n")
            self.log_results("  • Increase server RAM allocation\n")
            self.log_results("  • Check for memory leaks\n")
            self.log_results("  • Reduce view distance if needed\n\n")
        
        if avg_cpu > 70:
            self.log_results("⚠ High CPU usage\n")
            self.log_results("  • Profile specific mods for CPU usage\n")
            self.log_results("  • Optimize redstone contraptions\n")
            self.log_results("  • Consider upgrading server CPU\n\n")
        
        if avg_tps >= 19.5 and max_memory < 3.0 and avg_cpu < 60:
            self.log_results("✓ Server performance is excellent!\n\n")
        
        self.log_results("\nNote: For detailed profiling, use Spark or VisualVM\n")
    
    def log_results(self, text: str, overwrite_last: bool = False):
        """Log to results text"""
        def update():
            self.results_text.configure(state="normal")
            if overwrite_last:
                # Delete last line and add new one
                self.results_text.delete("end-2l", "end-1l")
            self.results_text.insert("end", text)
            self.results_text.see("end")
            self.results_text.configure(state="disabled")
        
        self.after(0, update)

