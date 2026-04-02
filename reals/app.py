import sys, os, threading, subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QCheckBox, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

BG      = "#0f0f0f"
CARD    = "#1a1a1a"
ACCENT  = "#e8e0d5"
MUTED   = "#666666"
SUCCESS = "#7dbb8a"
ERROR   = "#e07070"


class Runner(QThread):
    log     = pyqtSignal(str, str)
    done    = pyqtSignal(bool)

    def __init__(self, count, dry_run):
        super().__init__()
        self.count   = count
        self.dry_run = dry_run

    def run(self):
        cmd = [sys.executable, "main.py", "--count", str(self.count)]
        if self.dry_run:
            cmd.append("--dry-run")
        try:
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, cwd=os.path.dirname(os.path.abspath(__file__))
            )
            for line in proc.stdout:
                line = line.rstrip()
                if not line: continue
                tag = "success" if "✅" in line or "Done" in line else \
                      "error"   if "error" in line.lower() else "info"
                self.log.emit(line, tag)
            proc.wait()
            self.done.emit(proc.returncode == 0)
        except Exception as ex:
            self.log.emit(f"❌ {ex}", "error")
            self.done.emit(False)


class RealsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reals")
        self.setFixedSize(520, 660)
        self.setStyleSheet(f"background-color: {BG};")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 30)
        root.setSpacing(0)

        title = QLabel("Reals")
        title.setFont(QFont("Georgia", 30, QFont.Bold))
        title.setStyleSheet(f"color: {ACCENT};")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        sub = QLabel("print your feed. put down your phone.")
        sub.setFont(QFont("Georgia", 11))
        sub.setStyleSheet(f"color: {MUTED};")
        sub.setAlignment(Qt.AlignCenter)
        root.addWidget(sub)

        div = QLabel()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {MUTED}; margin-top: 24px; margin-bottom: 24px;")
        root.addWidget(div)

        card = QWidget()
        card.setStyleSheet(f"background: {CARD}; border-radius: 8px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 16)

        row = QHBoxLayout()
        lbl = QLabel("Reels to capture")
        lbl.setFont(QFont("Helvetica Neue", 11))
        lbl.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        row.addWidget(lbl)

        self.count_label = QLabel("8")
        self.count_label.setFont(QFont("Helvetica Neue", 11))
        self.count_label.setStyleSheet(f"color: {ACCENT}; background: transparent;")
        self.count_label.setAlignment(Qt.AlignRight)
        row.addWidget(self.count_label)
        card_layout.addLayout(row)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(4)
        self.slider.setMaximum(20)
        self.slider.setValue(8)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 4px; background: #333; border-radius: 2px; }
            QSlider::handle:horizontal { background: #e8e0d5; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }
            QSlider::sub-page:horizontal { background: #e8e0d5; border-radius: 2px; }
        """)
        self.slider.valueChanged.connect(lambda v: self.count_label.setText(str(v)))
        card_layout.addWidget(self.slider)
        root.addWidget(card)

        self.dry_run = QCheckBox("Dry run  (skip AI — free)")
        self.dry_run.setFont(QFont("Helvetica Neue", 9))
        self.dry_run.setStyleSheet(f"color: {MUTED}; margin-top: 12px;")
        root.addWidget(self.dry_run)

        self.btn = QPushButton("Print my Reals →")
        self.btn.setFont(QFont("Helvetica Neue", 13, QFont.Bold))
        self.btn.setFixedHeight(48)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.btn.setStyleSheet(f"""
            QPushButton {{ background: {ACCENT}; color: {BG}; border: none; border-radius: 6px; margin-top: 20px; }}
            QPushButton:hover {{ background: #ffffff; }}
            QPushButton:disabled {{ background: {MUTED}; color: #333; }}
        """)
        self.btn.clicked.connect(self._start)
        root.addWidget(self.btn)

        self.progress = QProgressBar()
        self.progress.setFixedHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 0)
        self.progress.setStyleSheet(f"""
            QProgressBar {{ background: #222; border: none; border-radius: 1px; margin-top: 10px; }}
            QProgressBar::chunk {{ background: {ACCENT}; border-radius: 1px; }}
        """)
        self.progress.hide()
        root.addWidget(self.progress)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setFont(QFont("Menlo", 9))
        self.log.setStyleSheet(f"""
            QTextEdit {{ background: #111; color: {MUTED}; border: none; border-radius: 6px; padding: 10px; margin-top: 16px; }}
        """)
        self.log.setFixedHeight(180)
        root.addWidget(self.log)

    def _append_log(self, msg, tag):
        color = SUCCESS if tag == "success" else ERROR if tag == "error" else MUTED
        self.log.append(f'<span style="color:{color};">{msg}</span>')

    def _start(self):
        self.log.clear()
        self.btn.setEnabled(False)
        self.btn.setText("Running…")
        self.progress.show()
        self.runner = Runner(self.slider.value(), self.dry_run.isChecked())
        self.runner.log.connect(self._append_log)
        self.runner.done.connect(self._finished)
        self.runner.start()

    def _finished(self, success):
        self.btn.setEnabled(True)
        self.btn.setText("Print my Reals →")
        self.progress.hide()
        if success:
            self._append_log("✅ Opening reals.pdf…", "success")
            pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reals.pdf")
            if os.path.exists(pdf):
                subprocess.run(["open", pdf])
        else:
            self._append_log("❌ Something went wrong. Check the log above.", "error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealsApp()
    window.show()
    sys.exit(app.exec_())

# ── remove old tkinter code below ──
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import subprocess
import os
import sys

# ── colours ──────────────────────────────────────────────────────────────────
BG       = "#0f0f0f"
CARD     = "#1a1a1a"
ACCENT   = "#e8e0d5"       # warm off-white
MUTED    = "#666666"
BTN_BG   = "#e8e0d5"
BTN_FG   = "#0f0f0f"
BTN_HOV  = "#ffffff"
LOG_BG   = "#111111"
LOG_FG   = "#888888"
SUCCESS  = "#7dbb8a"
ERROR    = "#e07070"

FONT_HEAD  = ("Georgia", 28, "bold")
FONT_SUB   = ("Georgia", 11, "italic")
FONT_LABEL = ("Helvetica Neue", 11)
FONT_SMALL = ("Helvetica Neue", 9)
FONT_BTN   = ("Helvetica Neue", 12, "bold")
FONT_LOG   = ("Menlo", 9)


class RealsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reals")
        self.geometry("520x640")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._running = False
        self._build_ui()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── top padding ──
        tk.Frame(self, bg=BG, height=40).pack()

        # ── logo ──
        tk.Label(self, text="Reals", font=FONT_HEAD,
                 bg=BG, fg=ACCENT).pack()
        tk.Label(self, text="print your feed. put down your phone.",
                 font=FONT_SUB, bg=BG, fg=MUTED).pack(pady=(4, 0))

        # ── divider ──
        tk.Frame(self, bg=MUTED, height=1, width=400).pack(pady=24)

        # ── count slider ──
        card = tk.Frame(self, bg=CARD, padx=24, pady=20)
        card.pack(padx=40, fill="x")

        top_row = tk.Frame(card, bg=CARD)
        top_row.pack(fill="x")
        tk.Label(top_row, text="Reels to capture", font=FONT_LABEL,
                 bg=CARD, fg=ACCENT).pack(side="left")

        self.count_var = tk.IntVar(value=8)
        self.count_label = tk.Label(top_row, text="8", font=FONT_LABEL,
                                    bg=CARD, fg=ACCENT, width=3, anchor="e")
        self.count_label.pack(side="right")

        slider = ttk.Scale(card, from_=4, to=20, orient="horizontal",
                           variable=self.count_var,
                           command=self._on_slider)
        slider.pack(fill="x", pady=(10, 0))

        self._style_slider()

        # ── dry run toggle ──
        self.dry_run_var = tk.BooleanVar(value=False)
        dr_frame = tk.Frame(self, bg=BG)
        dr_frame.pack(padx=40, pady=(14, 0), anchor="w")
        self.dr_check = tk.Checkbutton(
            dr_frame, text="Dry run  (skip AI — free)",
            variable=self.dry_run_var,
            font=FONT_SMALL, bg=BG, fg=MUTED,
            activebackground=BG, activeforeground=ACCENT,
            selectcolor=BG, relief="flat", bd=0,
            cursor="hand2"
        )
        self.dr_check.pack(side="left")

        # ── main button ──
        self.btn = tk.Button(
            self, text="Print my Reals →",
            font=FONT_BTN, bg=BTN_BG, fg=BTN_FG,
            activebackground=BTN_HOV, activeforeground=BTN_FG,
            relief="flat", bd=0, padx=24, pady=12,
            cursor="hand2", command=self._start
        )
        self.btn.pack(pady=28)
        self.btn.bind("<Enter>", lambda e: self.btn.config(bg=BTN_HOV))
        self.btn.bind("<Leave>", lambda e: self.btn.config(bg=BTN_BG))

        # ── progress bar ──
        self.progress = ttk.Progressbar(self, mode="indeterminate", length=440)
        self.progress.pack(padx=40)

        # ── log ──
        tk.Frame(self, bg=BG, height=12).pack()
        self.log = scrolledtext.ScrolledText(
            self, height=10, font=FONT_LOG,
            bg=LOG_BG, fg=LOG_FG,
            relief="flat", bd=0,
            wrap="word", state="disabled"
        )
        self.log.pack(padx=40, pady=(0, 24), fill="x")

        # colour tags
        self.log.tag_config("success", foreground=SUCCESS)
        self.log.tag_config("error",   foreground=ERROR)
        self.log.tag_config("info",    foreground=LOG_FG)

    def _style_slider(self):
        s = ttk.Style()
        s.theme_use("default")
        s.configure("Horizontal.TScale",
                    background=CARD, troughcolor="#333",
                    sliderlength=18, sliderrelief="flat")

    # ── helpers ──────────────────────────────────────────────────────────────

    def _on_slider(self, val):
        self.count_label.config(text=str(int(float(val))))

    def _log(self, msg, tag="info"):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.config(state="disabled")

    def _set_running(self, running: bool):
        self._running = running
        if running:
            self.btn.config(state="disabled", text="Running…", bg=MUTED)
            self.progress.start(12)
        else:
            self.btn.config(state="normal", text="Print my Reals →", bg=BTN_BG)
            self.progress.stop()
            self.progress["value"] = 0

    # ── run pipeline ─────────────────────────────────────────────────────────

    def _start(self):
        if self._running:
            return
        self._set_running(True)
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        count    = self.count_var.get()
        dry_run  = self.dry_run_var.get()

        self._log(f"🚀 Starting Reals — {count} reels, dry_run={dry_run}")

        cmd = [sys.executable, "main.py", "--count", str(count)]
        if dry_run:
            cmd.append("--dry-run")

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )

            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                tag = "success" if "✅" in line or "Done" in line else \
                      "error"   if "Error" in line or "error" in line else "info"
                self.after(0, self._log, line, tag)

            proc.wait()

            if proc.returncode == 0:
                self.after(0, self._log, "✅ Done! Opening reals.pdf…", "success")
                self.after(0, self._open_pdf)
            else:
                self.after(0, self._log, "❌ Something went wrong. Check the log above.", "error")

        except Exception as ex:
            self.after(0, self._log, f"❌ {ex}", "error")
        finally:
            self.after(0, self._set_running, False)

    def _open_pdf(self):
        pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reals.pdf")
        if os.path.exists(pdf):
            subprocess.run(["open", pdf])   # macOS
        else:
            self._log("⚠️  reals.pdf not found", "error")


if __name__ == "__main__":
    app = RealsApp()
    app.mainloop()