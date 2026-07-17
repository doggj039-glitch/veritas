
# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Disclosure Analysis Tool
Simple report analyzer for disclosure/report issues.
"""

import os
import re
import threading
import tkinter as tk
import webbrowser
import urllib.parse
from datetime import datetime
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

from ai_integration import AIIntegration
# Local modules
from config import (
    APP_TITLE,
    APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
)
from document_processor import DocumentProcessor
from legal_dictionary import (
    LEGAL_DICTIONARY, TERMINOLOGY_RULES, DEFLECTION_PATTERNS
)
from privacy_scrubber import scrub_party_identifiers
from report_generator import ReportGenerator
from pipeline_runner import PipelineRunner

# ─── Color Scheme ──────────────────────────────────────────────────────────────
COLORS = {
    "bg_dark": "#111111",
    "bg_medium": "#151515",
    "bg_light": "#1d1d1d",
    "accent": "#5f5f5f",
    "accent2": "#3f3f3f",
    "text_primary": "#efefef",
    "text_secondary": "#9a9a9a",
    "text_highlight": "#ffffff",
    "success": "#707070",
    "warning": "#6a6a6a",
    "danger": "#555555",
    "info": "#8a8a8a",
    "panel_bg": "#121212",
    "card_bg": "#171717",
    "input_bg": "#1b1b1b",
    "green_light": "#8a8a8a",
    "orange_light": "#7a7a7a",
    "red_light": "#6a6a6a",
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LAST_DOCUMENT_STATE_PATH = os.path.join(os.getcwd(), ".last_document_state.json")
LOGO_ICON_PATH = os.path.join(BASE_DIR, "assets", "project_phoenix_logo_icon.png")
LOGO_BG_PATH = os.path.join(BASE_DIR, "assets", "project_phoenix_logo.png")
BUILD_TAG = datetime.utcnow().strftime("%Y%m%d-%H%M%S")


def _about_dialog():
    messagebox.showinfo("About",
        f"Disclosure Analysis Tool\n"
        f"Version {APP_VERSION}\n\n"
        f"Simple disclosure analysis tool.\n\n"
        f"This tool checks report text against dictionary definitions\n"
        f"and highlights potential issues in plain language.\n\n"
        f"It is not legal advice."
    )


def _normalize_legal_term(term_key, term_data):
    return {
        "definition": term_data.get("definition") or term_data.get("legal_definition", ""),
        "preferred_form": term_data.get("preferred_form") or term_key.replace("_", " "),
        "category": term_data.get("category", "general"),
        "source": term_data.get("source") or term_data.get("legal_source", "Legal Dictionary"),
        "aliases": term_data.get("aliases", []),
        "misuses": term_data.get("misuses", []),
    }


class LegalAnalyzerApp:
    """Main application class for the document analyzer GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_TITLE} v{APP_VERSION} [{BUILD_TAG}]")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1200, 750)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Core objects
        self.doc_processor = DocumentProcessor()
        self.report_generator = ReportGenerator()
        self.ai = AIIntegration()
        self.pipeline = PipelineRunner()
        self.pipeline.status_callback = self._on_pipeline_status
        self.research_result = {}
        self._last_report_folder = None

        # State
        self.document_text = ""
        self.document_metadata = {}
        self.analysis_results = {}
        self.display_results = {}
        self.terminology_issues = []
        self.deflection_issues = []
        self.ai_results = {}
        self.logo_bg_image = None
        self.logo_bg_source = None
        self.logo_bg_render = None
        self.logo_banner_render = None
        self.bg_canvas = None
        self.bg_canvas_image_id = None
        self.ui_root = None
        self.ui_window_id = None

        self._load_brand_assets()
        self._build_background()

        # Disclaimer Label
        parent = self.ui_root if self.ui_root is not None else self.root
        disclaimer_frame = tk.Frame(parent, bg="#101010")
        disclaimer_frame.pack(side="top", fill="x")
        tk.Label(disclaimer_frame, text="RESEARCH AND STATISTICS TOOL ONLY — NOT LEGAL ADVICE — VERIFY ALL RESULTS", 
                 bg="#101010", fg="#d8d8d8", font=("Helvetica", 10, "bold"), pady=5).pack()

        # Build UI tabs
        self.notebook = ttk.Notebook(self.root)
        self._build_styles()
        self._build_ui()
        self.root.after(50, self._restore_last_document_state)

    def _load_brand_assets(self):
        if os.path.exists(LOGO_BG_PATH):
            self.logo_bg_source = Image.open(LOGO_BG_PATH)
        # Intentionally do not set a custom window icon.

    def _build_background(self):
        if self.logo_bg_source is None:
            return
        self.bg_canvas = tk.Canvas(self.root, bd=0, highlightthickness=0)
        self.bg_canvas.pack(fill=tk.BOTH, expand=True)
        self.bg_canvas_image_id = self.bg_canvas.create_image(0, 0, anchor=tk.NW)
        self.ui_root = tk.Frame(self.bg_canvas, bg="")
        self.ui_window_id = self.bg_canvas.create_window(0, 0, anchor=tk.NW, window=self.ui_root)
        self.root.bind("<Configure>", self._refresh_background_image, add="+")
        self._refresh_background_image()

    def _refresh_background_image(self, event=None):
        if self.logo_bg_source is None or self.bg_canvas is None:
            return
        width = max(self.root.winfo_width(), 1)
        height = max(self.root.winfo_height(), 1)
        resized = self.logo_bg_source.resize((width, height), Image.LANCZOS)
        self.logo_bg_render = ImageTk.PhotoImage(resized)
        self.bg_canvas.config(width=width, height=height)
        self.bg_canvas.itemconfigure(self.bg_canvas_image_id, image=self.logo_bg_render)
        self.bg_canvas.coords(self.bg_canvas_image_id, 0, 0)
        if self.ui_window_id is not None:
            self.bg_canvas.itemconfigure(self.ui_window_id, width=width, height=height)
            self.bg_canvas.coords(self.ui_window_id, 0, 0)

    def _build_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # General
        self.style.configure(".", background=COLORS["bg_dark"], foreground=COLORS["text_primary"],
                              fieldbackground=COLORS["input_bg"], borderwidth=0)
        self.style.configure("TFrame", background=COLORS["bg_dark"])
        self.style.configure("TLabel", background=COLORS["bg_dark"], foreground=COLORS["text_primary"],
                              font=("Segoe UI", 10))
        self.style.configure("TButton", background=COLORS["accent"], foreground="white",
                              font=("Segoe UI", 10, "bold"), padding=(12, 6))
        self.style.map("TButton",
                        background=[("active", COLORS["accent2"]), ("pressed", COLORS["bg_light"])])
        self.style.configure("Accent.TButton", background=COLORS["info"], foreground="white")
        self.style.configure("Success.TButton", background=COLORS["success"], foreground="white")
        self.style.configure("Danger.TButton", background=COLORS["danger"], foreground="white")
        self.style.configure("Warning.TButton", background=COLORS["warning"], foreground="black")
        self.style.configure(
            "SidebarTab.TButton",
            background=COLORS["card_bg"],
            foreground=COLORS["text_primary"],
            font=("Segoe UI", 10, "bold"),
            padding=(12, 10),
            anchor="w",
        )
        self.style.map(
            "SidebarTab.TButton",
            background=[("active", COLORS["bg_medium"]), ("pressed", COLORS["bg_light"])],
            foreground=[("active", "white")],
        )
        self.style.configure(
            "SidebarTabActive.TButton",
            background=COLORS["accent"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(12, 10),
            anchor="w",
        )

        # Notebook tabs
        self.style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=COLORS["bg_medium"],
                              foreground=COLORS["text_primary"], padding=[16, 8],
                              font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab",
                        background=[("selected", COLORS["accent"])],
                        foreground=[("selected", "white")])
        # Force-hide notebook tab strips globally and for this tabless style.
        self.style.layout("TNotebook.Tab", [])
        self.style.layout("Tabless.TNotebook", [("Notebook.client", {"sticky": "nswe"})])
        self.style.layout("Tabless.TNotebook.Tab", [])

        # Treeview
        self.style.configure("Treeview", background=COLORS["card_bg"],
                              foreground=COLORS["text_primary"],
                              fieldbackground=COLORS["card_bg"],
                              font=("Segoe UI", 9), rowheight=28)
        self.style.configure("Treeview.Heading", background=COLORS["bg_medium"],
                              foreground=COLORS["text_highlight"],
                              font=("Segoe UI", 9, "bold"))
        self.style.map("Treeview", background=[("selected", COLORS["accent2"])])

        # Entry / combobox
        self.style.configure("TEntry", fieldbackground=COLORS["input_bg"],
                              foreground=COLORS["text_primary"])
        self.style.configure("TCombobox", fieldbackground=COLORS["input_bg"],
                              foreground=COLORS["text_primary"])

        # Labels
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"),
                              foreground=COLORS["text_highlight"])
        self.style.configure("Subheader.TLabel", font=("Segoe UI", 11, "bold"),
                              foreground=COLORS["text_primary"])
        self.style.configure("Info.TLabel", foreground=COLORS["info"])
        self.style.configure("Success.TLabel", foreground=COLORS["success"])
        self.style.configure("Warning.TLabel", foreground=COLORS["warning"])
        self.style.configure("Danger.TLabel", foreground=COLORS["danger"])

        # Labelframe
        self.style.configure("TLabelframe", background=COLORS["bg_dark"],
                              foreground=COLORS["text_secondary"])
        self.style.configure("TLabelframe.Label", background=COLORS["bg_dark"],
                              foreground=COLORS["text_secondary"], font=("Segoe UI", 10, "bold"))

        # Progress bar
        self.style.configure("TProgressbar", background=COLORS["accent"],
                              troughcolor=COLORS["input_bg"])

    # ─── UI Construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Menu Bar ──
        menubar = tk.Menu(self.root, bg=COLORS["bg_medium"], fg=COLORS["text_primary"],
                           activebackground=COLORS["accent"], activeforeground="white")
        file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["card_bg"], fg=COLORS["text_primary"])
        file_menu.add_command(label="Open Document...", command=self._open_document)
        file_menu.add_command(label="Paste Text...", command=self._paste_text)
        file_menu.add_separator()
        file_menu.add_command(label="Export HTML Report...", command=self._export_html)
        file_menu.add_command(label="Export Text Report...", command=self._export_txt)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["card_bg"], fg=COLORS["text_primary"])
        tools_menu.add_command(label="Legal Dictionary Lookup...", command=self._dict_lookup_dialog)
        tools_menu.add_separator()
        tools_menu.add_command(label="AI Ask a Question...", command=self._ai_question_dialog)
        menubar.add_cascade(label="Tools", menu=tools_menu)

        settings_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["card_bg"], fg=COLORS["text_primary"])
        settings_menu.add_command(label="API Keys...", command=self._settings_dialog)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS["card_bg"], fg=COLORS["text_primary"])
        help_menu.add_command(label="About", command=_about_dialog)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # ── Main Paned Layout ──
        container = self.ui_root if self.ui_root is not None else self.root
        main_pane = ttk.PanedWindow(container, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Left panel — navigation & controls
        left_frame = ttk.Frame(main_pane, width=280)
        main_pane.add(left_frame, weight=0)

        # Right panel — content tabs
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=1)

        self._build_left_panel(left_frame)
        self._build_right_panel(right_frame)

        # Status bar
        self.status_var = tk.StringVar(value="Ready — No document loaded")
        status_bar = ttk.Label(container, textvariable=self.status_var, relief=tk.SUNKEN,
                                anchor=tk.W, font=("Segoe UI", 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)

    def _build_left_panel(self, parent):
        # ── Logo / Title ──
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=8, pady=(8, 4))
        ttk.Label(title_frame, text="Disclosure Analysis Tool", style="Header.TLabel").pack(anchor=tk.W)
        ttk.Label(
            title_frame,
            text=f"Disclosure Analysis Tool v{APP_VERSION}",
            foreground=COLORS["text_secondary"],
        ).pack(anchor=tk.W)

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=6)

        # ── Document Load ──
        load_frame = ttk.LabelFrame(parent, text="📂 Document", padding=8)
        load_frame.pack(fill=tk.X, padx=8, pady=4)

        ttk.Button(load_frame, text="Open File", command=self._open_document).pack(fill=tk.X, pady=2)
        ttk.Button(load_frame, text="Paste Text", command=self._paste_text).pack(fill=tk.X, pady=2)

        self.doc_info_label = ttk.Label(load_frame, text="No document loaded", foreground=COLORS["text_secondary"])
        self.doc_info_label.pack(anchor=tk.W, pady=(6, 0))

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=6)

        # ── Analysis Controls ──
        analysis_frame = ttk.LabelFrame(parent, text="🔍 Analysis", padding=8)
        analysis_frame.pack(fill=tk.X, padx=8, pady=4)

        ttk.Button(analysis_frame, text="▶ Run Full Analysis",
                    command=self._run_full_analysis, style="Success.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="📖 Dictionary & Terminology",
                    command=self._run_terminology).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="🚫 Deflection / Ambiguity",
                    command=self._run_deflection).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="🤖 AI Verify Analysis",
                    command=self._run_ai_verify, style="Accent.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="🔬 Run Research",
                    command=self._run_research, style="Success.TButton").pack(fill=tk.X, pady=2)

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=6)

        # ── Export ──
        export_frame = ttk.LabelFrame(parent, text="📄 Export", padding=8)
        export_frame.pack(fill=tk.X, padx=8, pady=4)

        ttk.Button(export_frame, text="📥 HTML Report",
                    command=self._export_html).pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="📥 Text Report",
                    command=self._export_txt).pack(fill=tk.X, pady=2)

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=8, pady=6)

        # ── Quick Dictionary Lookup ──
        dict_frame = ttk.LabelFrame(parent, text="📖 Quick Lookup", padding=8)
        dict_frame.pack(fill=tk.X, padx=8, pady=4)

        self.dict_entry_var = tk.StringVar()
        dict_entry = ttk.Entry(dict_frame, textvariable=self.dict_entry_var)
        dict_entry.pack(fill=tk.X, pady=2)
        dict_entry.bind("<Return>", lambda e: self._quick_dict_lookup())

        ttk.Button(dict_frame, text="Look Up", command=self._quick_dict_lookup).pack(fill=tk.X, pady=2)

        self.dict_result_label = ttk.Label(dict_frame, text="", wraplength=240,
                                             foreground=COLORS["info"], font=("Segoe UI", 9))
        self.dict_result_label.pack(anchor=tk.W, pady=4)

        # ── Progress ──
        self.progress = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode="determinate", length=250)
        self.progress.pack(fill=tk.X, padx=8, pady=(8, 4))

    def _build_right_panel(self, parent):
        if self.logo_bg_source is not None:
            banner = self.logo_bg_source.resize((1200, 420), Image.LANCZOS)
            self.logo_banner_render = ImageTk.PhotoImage(banner)
            tk.Label(
                parent,
                image=self.logo_banner_render,
                bg=COLORS["bg_dark"],
                bd=0,
                highlightthickness=0,
            ).pack(fill=tk.X, pady=(0, 8))

        shell = ttk.Frame(parent)
        shell.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        nav_frame = ttk.Frame(shell, width=220)
        nav_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        content_frame = ttk.Frame(shell)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.view_nav_frame = nav_frame
        self.view_buttons = {}
        self.view_order = []

        self.notebook = ttk.Notebook(content_frame, style="Tabless.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Document View
        self.doc_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.doc_tab, text="  📄 Document  ")
        self.view_order.append(("📄 Document", self.doc_tab))
        self._build_document_tab(self.doc_tab)

        # Tab 2: Terminology
        self.term_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.term_tab, text="  📖 Terminology  ")
        self.view_order.append(("📖 Terminology", self.term_tab))
        self._build_terminology_tab(self.term_tab)

        # Tab 3: Deflection / Ambiguity
        self.deflection_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.deflection_tab, text="  🚫 Deflection  ")
        self.view_order.append(("🚫 Deflection", self.deflection_tab))
        self._build_deflection_tab(self.deflection_tab)

        # Tab 4: AI Analysis
        self.ai_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ai_tab, text="  🤖 AI Analysis  ")
        self.view_order.append(("🤖 AI Analysis", self.ai_tab))
        self._build_ai_tab(self.ai_tab)

        # Tab 5: Dictionary
        self.dict_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dict_tab, text="  📕 Dictionary  ")
        self.view_order.append(("📕 Dictionary", self.dict_tab))
        self._build_dictionary_tab(self.dict_tab)

        # Tab 6: Research Map (VERITAS)
        self.research_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.research_tab, text="  🔬 Research Map  ")
        self.view_order.append(("🔬 Research Map", self.research_tab))
        self._build_research_tab(self.research_tab)

        self._build_view_nav()
        self.notebook.bind("<<NotebookTabChanged>>", self._sync_view_nav)
        self._sync_view_nav()

    def _build_view_nav(self):
        ttk.Label(self.view_nav_frame, text="Analysis Views", style="Subheader.TLabel").pack(
            anchor=tk.W, padx=4, pady=(4, 8)
        )
        for label, tab in self.view_order:
            btn = ttk.Button(
                self.view_nav_frame,
                text=label,
                style="SidebarTab.TButton",
                command=lambda t=tab: self._select_view(t),
            )
            btn.pack(fill=tk.X, pady=2)
            self.view_buttons[str(tab)] = btn

    def _select_view(self, tab):
        self.notebook.select(tab)
        self._sync_view_nav()

    def _sync_view_nav(self, event=None):
        current = str(self.notebook.select())
        for key, btn in self.view_buttons.items():
            btn.configure(style="SidebarTabActive.TButton" if key == current else "SidebarTab.TButton")

    # ── Document Tab ──────────────────────────────────────────────────────────

    def _build_document_tab(self, parent):
        # Document text viewer
        header = ttk.Frame(parent)
        header.pack(fill=tk.X, padx=8, pady=(8, 0))
        ttk.Label(header, text="Document Viewer", style="Subheader.TLabel").pack(side=tk.LEFT)

        self.doc_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 11),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            insertbackground="white", selectbackground=COLORS["accent2"],
            relief=tk.FLAT, borderwidth=2
        )
        self.doc_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Highlight tags
        self.doc_text.tag_configure("breach_indicator", foreground=COLORS["danger"],
                                     underline=True)
        self.doc_text.tag_configure("deflection", foreground=COLORS["warning"],
                                     background="#4a3000")
        self.doc_text.tag_configure("term_issue", foreground=COLORS["orange_light"],
                                     underline=True)

    # ── Terminology Tab ───────────────────────────────────────────────────────

    def _build_terminology_tab(self, parent):
        ttk.Label(parent, text="Terminology & Consistency Check", style="Subheader.TLabel").pack(
            anchor=tk.W, padx=8, pady=(8, 4))

        # Issues tree
        term_frame = ttk.LabelFrame(parent, text="Terminology Issues Found", padding=6)
        term_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        cols = ("term", "type", "issue", "correct_form", "source")
        self.term_tree = ttk.Treeview(term_frame, columns=cols, show="headings", height=12)
        self.term_tree.heading("term", text="Term / Phrase")
        self.term_tree.heading("type", text="Type")
        self.term_tree.heading("issue", text="Issue")
        self.term_tree.heading("correct_form", text="Correct Form")
        self.term_tree.heading("source", text="Source")
        self.term_tree.column("term", width=180)
        self.term_tree.column("type", width=100)
        self.term_tree.column("issue", width=250)
        self.term_tree.column("correct_form", width=180)
        self.term_tree.column("source", width=200)
        self.term_tree.pack(fill=tk.BOTH, expand=True)
        self.term_tree.bind("<<TreeviewSelect>>", self._on_term_select)

        # Detail
        self.term_detail_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 10),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            relief=tk.FLAT, height=8
        )
        self.term_detail_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

    # ── Deflection Tab ────────────────────────────────────────────────────────

    def _build_deflection_tab(self, parent):
        ttk.Label(parent, text="Deflection & Ambiguity Detection", style="Subheader.TLabel").pack(
            anchor=tk.W, padx=8, pady=(8, 4))

        defl_frame = ttk.LabelFrame(parent, text="Detected Issues", padding=6)
        defl_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        cols = ("pattern_type", "severity", "count", "description", "suggestion")
        self.defl_tree = ttk.Treeview(defl_frame, columns=cols, show="headings", height=10)
        self.defl_tree.heading("pattern_type", text="Pattern Type")
        self.defl_tree.heading("severity", text="Severity")
        self.defl_tree.heading("count", text="Count")
        self.defl_tree.heading("description", text="Description")
        self.defl_tree.heading("suggestion", text="Suggestion")
        self.defl_tree.column("pattern_type", width=150)
        self.defl_tree.column("severity", width=70, anchor=tk.CENTER)
        self.defl_tree.column("count", width=60, anchor=tk.CENTER)
        self.defl_tree.column("description", width=350)
        self.defl_tree.column("suggestion", width=300)
        self.defl_tree.pack(fill=tk.BOTH, expand=True)

        self.defl_detail_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 10),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            relief=tk.FLAT, height=8
        )
        self.defl_detail_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

    # ── AI Tab ────────────────────────────────────────────────────────────────

    def _build_ai_tab(self, parent):
        ttk.Label(parent, text="AI-Powered Verification & Analysis", style="Subheader.TLabel").pack(
            anchor=tk.W, padx=8, pady=(8, 4))

        # AI status
        self.ai_status_label = ttk.Label(parent, text="AI: Not configured",
                                           foreground=COLORS["warning"])
        self.ai_status_label.pack(anchor=tk.W, padx=8, pady=2)

        # AI controls
        ai_ctrl = ttk.Frame(parent)
        ai_ctrl.pack(fill=tk.X, padx=8, pady=4)

        ttk.Button(ai_ctrl, text="Verify Findings",
                    command=lambda: self._ai_verify_specific("findings"),
                    style="Accent.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(ai_ctrl, text="Verify Terminology",
                    command=lambda: self._ai_verify_specific("terms"),
                    style="Accent.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(ai_ctrl, text="Detect Deflection",
                    command=lambda: self._ai_verify_specific("deflection"),
                    style="Accent.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(ai_ctrl, text="Validate Cross-Refs",
                    command=lambda: self._ai_verify_specific("crossref"),
                    style="Accent.TButton").pack(side=tk.LEFT, padx=4)
        ttk.Button(ai_ctrl, text="Executive Summary",
                    command=lambda: self._ai_verify_specific("summary"),
                    style="Accent.TButton").pack(side=tk.LEFT, padx=4)

        # AI output
        self.ai_output = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 10),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            insertbackground="white", relief=tk.FLAT
        )
        self.ai_output.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Ask AI
        ask_frame = ttk.Frame(parent)
        ask_frame.pack(fill=tk.X, padx=8, pady=(4, 8))

        self.ai_ask_var = tk.StringVar()
        ai_entry = ttk.Entry(ask_frame, textvariable=self.ai_ask_var, font=("Segoe UI", 10))
        ai_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ai_entry.bind("<Return>", lambda e: self._ai_ask())
        ttk.Button(ask_frame, text="Ask AI", command=self._ai_ask,
                    style="Accent.TButton").pack(side=tk.RIGHT)

    # ── Dictionary Tab ────────────────────────────────────────────────────────

    def _build_dictionary_tab(self, parent):
        ttk.Label(parent, text="Legal Dictionary", style="Subheader.TLabel").pack(
            anchor=tk.W, padx=8, pady=(8, 4))

        # Search bar
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, padx=8, pady=4)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.dict_search_var = tk.StringVar()
        dict_search = ttk.Entry(search_frame, textvariable=self.dict_search_var, width=40,
                                 font=("Segoe UI", 10))
        dict_search.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
        dict_search.bind("<Return>", lambda e: self._search_dictionary())

        ttk.Button(search_frame, text="Search", command=self._search_dictionary).pack(side=tk.LEFT, padx=4)

        # Category filter
        ttk.Label(search_frame, text="Category:").pack(side=tk.LEFT, padx=(8, 2))
        self.dict_cat_var = tk.StringVar(value="All")
        categories = sorted({
            _normalize_legal_term(term_key, term_data)["category"]
            for term_key, term_data in LEGAL_DICTIONARY.items()
        })
        cat_combo = ttk.Combobox(search_frame, textvariable=self.dict_cat_var, width=18,
                                  values=["All"] + categories,
                                  state="readonly")
        cat_combo.pack(side=tk.LEFT, padx=4)

        # Dictionary list
        dict_list_frame = ttk.Frame(parent)
        dict_list_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        cols = ("term", "category", "preferred_form", "source")
        self.dict_tree = ttk.Treeview(dict_list_frame, columns=cols, show="headings", height=10)
        self.dict_tree.heading("term", text="Term")
        self.dict_tree.heading("category", text="Category")
        self.dict_tree.heading("preferred_form", text="Preferred Form")
        self.dict_tree.heading("source", text="Source")
        self.dict_tree.column("term", width=200)
        self.dict_tree.column("category", width=130)
        self.dict_tree.column("preferred_form", width=200)
        self.dict_tree.column("source", width=250)
        self.dict_tree.pack(fill=tk.BOTH, expand=True)
        self.dict_tree.bind("<<TreeviewSelect>>", self._on_dict_select)

        # Definition display
        self.dict_def_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 10),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            relief=tk.FLAT, height=10
        )
        self.dict_def_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Initial populate
        self._populate_dictionary_tree()

    # ══════════════════════════════════════════════════════════════════════════
    # FILE OPERATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def _open_document(self):
        home_dir = os.path.expanduser("~")
        downloads_dir = os.path.join(home_dir, "Downloads")
        initial_dir = downloads_dir if os.path.isdir(downloads_dir) else home_dir
        filetypes = [
            ("All Files", "*"),
            ("All Supported", ("*.pdf", "*.docx", "*.txt", "*.md", "*.rtf")),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Text Files", ("*.txt", "*.md", "*.rtf")),
        ]
        path = filedialog.askopenfilename(
            title="Open Legal Document",
            filetypes=filetypes,
            initialdir=initial_dir,
        )
        if not path:
            return

        self.status_var.set(f"Loading document: {os.path.basename(path)}...")
        self.root.update_idletasks()

        try:
            result = self.doc_processor.load_document(path)
            self.document_text = result["text"]
            self.document_metadata = result["metadata"]
            self.doc_text.delete("1.0", tk.END)
            self.doc_text.insert("1.0", self.document_text)

            meta = self.document_metadata
            self.doc_info_label.config(
                text=f"📄 {meta['file_name']}\n   {meta['word_count']:,} words | {meta['paragraph_count']} paragraphs"
            )
            self.status_var.set(f"Loaded: {meta['file_name']} — {meta['word_count']:,} words")
            self._save_last_document_state()
            self.root.after(50, self._autorun_full_analysis)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load document:\n{e}")
            self.status_var.set("Error loading document")

    def _paste_text(self):
        """Open a dialog to paste text directly."""
        dlg = tk.Toplevel(self.root)
        dlg.title("Paste Document Text")
        dlg.geometry("800x500")
        dlg.transient(self.root)
        dlg.grab_set()

        ttk.Label(dlg, text="Paste your legal document text below:", style="Subheader.TLabel").pack(
            padx=10, pady=8)

        text_area = scrolledtext.ScrolledText(dlg, wrap=tk.WORD, font=("Consolas", 11),
                                              bg=COLORS["input_bg"], fg=COLORS["text_primary"],
                                              insertbackground="white", relief=tk.FLAT)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        name_var = tk.StringVar(value="pasted_document")
        name_frame = ttk.Frame(dlg)
        name_frame.pack(fill=tk.X, padx=10, pady=4)
        ttk.Label(name_frame, text="Document name:").pack(side=tk.LEFT)
        ttk.Entry(name_frame, textvariable=name_var, width=40).pack(side=tk.LEFT, padx=4)

        def _confirm():
            content = text_area.get("1.0", tk.END).strip()
            if not content:
                messagebox.showwarning("Empty", "Please paste some text.", parent=dlg)
                return
            self.document_text = content
            self.document_metadata = {
                "file_name": name_var.get(),
                "format": ".txt",
                "char_count": len(content),
                "word_count": len(content.split()),
                "paragraph_count": len([p for p in content.split("\n\n") if p.strip()]),
                "sentence_count": 0,
            }
            self.doc_text.delete("1.0", tk.END)
            self.doc_text.insert("1.0", content)
            meta = self.document_metadata
            self.doc_info_label.config(
                text=f"📄 {meta['file_name']}\n   {meta['word_count']:,} words | {meta['paragraph_count']} paragraphs"
            )
            self.status_var.set(f"Loaded pasted document — {meta['word_count']:,} words")
            self._save_last_document_state()
            dlg.destroy()
            self.root.after(50, self._autorun_full_analysis)

        ttk.Button(dlg, text="Load Document", command=_confirm, style="Success.TButton").pack(pady=8)

    # ══════════════════════════════════════════════════════════════════════════
    # ANALYSIS
    # ══════════════════════════════════════════════════════════════════════════

    def _check_document_loaded(self):
        if not self.document_text.strip():
            messagebox.showwarning("No Document", "Please load a document first (File → Open or Paste Text).")
            return False
        return True

    def _save_last_document_state(self):
        # Do not persist raw disclosure content or metadata to disk.
        try:
            if os.path.exists(LAST_DOCUMENT_STATE_PATH):
                os.remove(LAST_DOCUMENT_STATE_PATH)
        except OSError:
            pass

    def _restore_last_document_state(self):
        # Legacy state files are removed on startup rather than restored.
        self._save_last_document_state()

    def _on_close(self):
        self._save_last_document_state()
        self.root.destroy()

    def _results_for_display(self):
        return self.display_results or self.analysis_results

    def _autorun_full_analysis(self):
        try:
            self._run_full_analysis(notify=False)
        except Exception as e:
            self.status_var.set("Autorun analysis failed")
            messagebox.showerror("Analysis Error", f"Automatic analysis failed:\n{e}")

    def _run_full_analysis(self, notify=True):
        if not self._check_document_loaded():
            return

        self.status_var.set("Running full analysis...")
        self.progress["value"] = 0
        self.root.update_idletasks()

        # Terminology
        self.progress["value"] = 30
        self._do_terminology_analysis()
        self.root.update_idletasks()

        # Deflection
        self.progress["value"] = 60
        self._do_deflection_analysis()
        self.root.update_idletasks()

        # Assemble combined results for reporting/export/AI review
        self.progress["value"] = 85
        self.analysis_results = {
            "document_metadata": dict(self.document_metadata),
            "terminology_issues": self.terminology_issues,
            "deflection_issues": self.deflection_issues,
        }
        self.display_results = scrub_party_identifiers(self.analysis_results)
        self.root.update_idletasks()

        # Highlight document
        self._highlight_document()
        self._save_last_document_state()

        self.progress["value"] = 100
        self.status_var.set("Full analysis complete.")
        if notify:
            messagebox.showinfo("Analysis Complete", "Full document analysis is complete.\nReview all tabs for results.")

    def _run_terminology(self):
        if not self._check_document_loaded():
            return
        self._do_terminology_analysis()
        self._highlight_document()
        self.status_var.set("Terminology analysis complete.")

    def _run_deflection(self):
        if not self._check_document_loaded():
            return
        self._do_deflection_analysis()
        self._highlight_document()
        self.status_var.set("Deflection analysis complete.")

    def _clean_flag_phrase(self, phrase):
        """Remove rule annotations so scanning uses the actual text to match."""
        return re.sub(r"\s*\([^)]*\)", "", phrase).strip()

    def _is_context_only_phrase(self, phrase):
        """Skip entries that are guidance notes rather than literal search terms."""
        lowered = phrase.lower()
        markers = [
            "when ", "unless ", "mid-sentence", "sentence context", "abbreviating",
            "strictly,", "strictly ", "in preference to",
        ]
        return any(marker in lowered for marker in markers)

    def _find_phrase_matches(self, text, phrase):
        """Find case-insensitive phrase matches with word boundaries."""
        cleaned = self._clean_flag_phrase(phrase)
        if not cleaned or self._is_context_only_phrase(phrase):
            return []

        pattern = r"\s+".join(re.escape(part) for part in cleaned.split())
        if re.search(r"\w", cleaned):
            pattern = rf"(?<!\w){pattern}(?!\w)"
        return list(re.finditer(pattern, text, re.IGNORECASE))

    def _collect_issue_snippets(self, text, matches, limit=5):
        snippets = []
        for match in matches[:limit]:
            snippet = text[max(0, match.start() - 25):min(len(text), match.end() + 25)].strip()
            if snippet:
                snippets.append(snippet.replace("\n", " "))
        return snippets

    def _add_issue(self, bucket, key, payload, matches):
        if not matches:
            return

        spans = [(match.start(), match.end()) for match in matches]
        existing = bucket.get(key)
        if existing:
            existing["count"] += len(matches)
            existing["spans"].extend(spans)
            existing["matches"].extend(self._collect_issue_snippets(self.document_text, matches))
            existing["matches"] = existing["matches"][:5]
            return

        payload["count"] = len(matches)
        payload["spans"] = spans
        payload["matches"] = self._collect_issue_snippets(self.document_text, matches)
        bucket[key] = payload

    def _do_terminology_analysis(self):
        """Run terminology and consistency analysis."""
        issue_map = {}
        text = self.document_text

        # Check dictionary misuses
        for term_key, term_data in LEGAL_DICTIONARY.items():
            normalized = _normalize_legal_term(term_key, term_data)
            canonical_term = term_key.replace("_", " ").lower()
            preferred_form = normalized["preferred_form"]
            for misuse in normalized["misuses"]:
                cleaned_misuse = self._clean_flag_phrase(misuse)
                if not cleaned_misuse:
                    continue
                if cleaned_misuse.lower() in {canonical_term, preferred_form.lower()}:
                    continue
                matches = self._find_phrase_matches(text, misuse)
                self._add_issue(issue_map, (cleaned_misuse.lower(), "misuse"), {
                        "term": misuse,
                        "type": "misuse",
                        "issue": f"'{misuse}' is not the preferred form of this term",
                        "correct_form": preferred_form,
                        "source": normalized["source"],
                        "definition": normalized["definition"],
                        "category": normalized["category"],
                    }, matches)

        # Check terminology rules
        for rule_key, rule_data in TERMINOLOGY_RULES.items():
            for incorrect in rule_data.get("incorrect", []):
                cleaned_incorrect = self._clean_flag_phrase(incorrect)
                if not cleaned_incorrect:
                    continue
                if cleaned_incorrect.lower() == rule_data["correct"].lower():
                    continue
                matches = self._find_phrase_matches(text, incorrect)
                self._add_issue(issue_map, (cleaned_incorrect.lower(), "spelling/format"), {
                        "term": cleaned_incorrect,
                        "type": "spelling/format",
                        "issue": f"Incorrect form — {rule_data.get('note', '')}",
                        "correct_form": rule_data["correct"],
                        "source": "Terminology Standards",
                        "definition": rule_data.get("note", ""),
                        "category": "consistency",
                    }, matches)

        self.terminology_issues = sorted(
            issue_map.values(),
            key=lambda issue: (-issue["count"], issue["term"].lower())
        )
        # Populate tree
        self._populate_term_tree()

    def _do_deflection_analysis(self):
        """Run deflection and ambiguity pattern analysis."""
        self.deflection_issues = []
        text = self.document_text

        for pattern_name, pattern_data in DEFLECTION_PATTERNS.items():
            total_count = 0
            matches_detail = []
            spans = []
            for pat in pattern_data["patterns"]:
                matches = list(re.finditer(pat, text, re.IGNORECASE))
                count = len(matches)
                total_count += count
                for m in matches:
                    matches_detail.append(m.group(0).strip())
                    spans.append((m.start(), m.end()))

            if total_count > 0:
                self.deflection_issues.append({
                    "pattern_type": pattern_name.replace("_", " ").title(),
                    "severity": pattern_data["severity"],
                    "count": total_count,
                    "description": pattern_data["description"],
                    "suggestion": pattern_data["suggestion"],
                    "matches": list(dict.fromkeys(matches_detail))[:10],
                    "spans": spans,
                })

        self.deflection_issues.sort(key=lambda issue: (-issue["count"], issue["pattern_type"]))
        self._populate_defl_tree()

    # ── Populate UI Components ────────────────────────────────────────────────

    def _populate_term_tree(self):
        for item in self.term_tree.get_children():
            self.term_tree.delete(item)

        for issue in self.terminology_issues:
            tag = "danger" if issue["type"] == "americanism" else "warning" if issue["type"] == "misuse" else ""
            self.term_tree.insert("", tk.END, values=(
                issue["term"],
                issue["type"],
                issue["issue"][:60],
                issue["correct_form"],
                issue["source"][:40],
            ), tags=(tag,))

        self.term_tree.tag_configure("danger", foreground=COLORS["red_light"])
        self.term_tree.tag_configure("warning", foreground=COLORS["orange_light"])

    def _on_term_select(self, event):
        sel = self.term_tree.selection()
        if not sel:
            return
        vals = self.term_tree.item(sel[0], "values")
        # Find matching issue
        for issue in self.terminology_issues:
            if issue["term"] == vals[0] and issue["type"] == vals[1]:
                self.term_detail_text.delete("1.0", tk.END)
                self.term_detail_text.insert(tk.END, f"TERM: {issue['term']}\n")
                self.term_detail_text.insert(tk.END, f"TYPE: {issue['type']}\n")
                self.term_detail_text.insert(tk.END, f"ISSUE: {issue['issue']}\n")
                self.term_detail_text.insert(tk.END, f"CORRECT FORM: {issue['correct_form']}\n")
                self.term_detail_text.insert(tk.END, f"\nDEFINITION:\n{issue.get('definition', 'N/A')}\n")
                self.term_detail_text.insert(tk.END, f"\nSOURCE: {issue.get('source', 'N/A')}\n")
                break

    def _populate_defl_tree(self):
        for item in self.defl_tree.get_children():
            self.defl_tree.delete(item)

        for issue in self.deflection_issues:
            sev_color = {"high": COLORS["red_light"], "medium": COLORS["orange_light"],
                         "low": COLORS["green_light"]}.get(issue["severity"], COLORS["text_primary"])
            self.defl_tree.insert("", tk.END, values=(
                issue["pattern_type"],
                issue["severity"].upper(),
                issue["count"],
                issue["description"][:60],
                issue["suggestion"][:50],
            ), tags=(issue["severity"],))

        self.defl_tree.tag_configure("high", foreground=COLORS["red_light"])
        self.defl_tree.tag_configure("medium", foreground=COLORS["orange_light"])
        self.defl_tree.tag_configure("low", foreground=COLORS["green_light"])

    def _highlight_document(self):
        """Highlight issue indicators and terminology issues in the document."""
        text_widget = self.doc_text

        # Remove existing tags
        for tag in ["breach_indicator", "deflection", "term_issue"]:
            text_widget.tag_remove(tag, "1.0", tk.END)

        content = text_widget.get("1.0", tk.END)
        content_lower = content.lower()

        # Highlight issue indicators
        breach_words = ["violation", "infringement", "breach", "unreasonable", "arbitrary",
                        "unconstitutional", "unlawful", "without warrant", "without reasonable grounds",
                        "grossly disproportionate", "denied", "not informed", "failure to inform",
                        "excessive", "overbroad"]
        for word in breach_words:
            for m in re.finditer(re.escape(word), content, re.IGNORECASE):
                start = f"1.0+{m.start()}c"
                end = f"1.0+{m.end()}c"
                text_widget.tag_add("breach_indicator", start, end)

        # Highlight deflection patterns
        for issue in self.deflection_issues:
            for start_idx, end_idx in issue.get("spans", []):
                start = f"1.0+{start_idx}c"
                end = f"1.0+{end_idx}c"
                text_widget.tag_add("deflection", start, end)

        # Highlight term issues
        for issue in self.terminology_issues:
            for start_idx, end_idx in issue.get("spans", []):
                start = f"1.0+{start_idx}c"
                end = f"1.0+{end_idx}c"
                text_widget.tag_add("term_issue", start, end)

    # ══════════════════════════════════════════════════════════════════════════
    # AI INTEGRATION
    # ══════════════════════════════════════════════════════════════════════════

    def _update_ai_status(self):
        """Update AI connection status indicator."""
        if self.ai.is_configured():
            provider_name = "GPT-4" if self.ai.provider == "openai" else "Gemini"
            self.ai_status_label.config(text=f"AI: ✅ Connected ({provider_name})", foreground=COLORS["success"])
        else:
            self.ai_status_label.config(text="AI: ❌ Not configured (Settings → API Keys)",
                                        foreground=COLORS["warning"])

    def _run_ai_verify(self):
        if not self._check_document_loaded():
            return
        self._ai_verify_specific("findings")

    def _ai_verify_specific(self, analysis_type):
        if not self.ai.is_configured():
            messagebox.showwarning("AI Not Configured",
                "OpenAI API key not configured.\n\n"
                "Go to Settings → API Keys to add your key, "
                "or set the OPENAI_API_KEY environment variable.")
            return

        if not self._check_document_loaded():
            return

        self.status_var.set(f"Running AI verification ({analysis_type})... Please wait.")
        self.root.update_idletasks()

        def _worker():
            try:
                if analysis_type == "findings":
                    result = self.ai.verify_findings(self.analysis_results, self.document_text)
                elif analysis_type == "terms":
                    result = self.ai.verify_legal_terms(self.document_text, self.terminology_issues)
                elif analysis_type == "deflection":
                    result = self.ai.detect_deflection(self.document_text, self.deflection_issues)
                elif analysis_type == "crossref":
                    result = self.ai.validate_cross_references(self.analysis_results, self.document_text)
                elif analysis_type == "summary":
                    result = self.ai.generate_summary(self.analysis_results)
                else:
                    result = {"error": "Unknown analysis type", "content": None}

                # Update UI from main thread
                self.root.after(0, self._display_ai_result, analysis_type, result)
            except Exception as e:
                self.root.after(0, self._display_ai_error, str(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_ai_result(self, analysis_type, result):
        if result.get("error") and not result.get("content"):
            self.ai_output.insert(tk.END, f"\n⚠️ ERROR: {result['error']}\n")
            self.status_var.set(f"AI error: {result['error'][:60]}")
            return

        content = result.get("content", "No response")
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.ai_output.insert(tk.END,
            f"\n{'═'*70}\n"
            f"🤖 AI VERIFICATION — {analysis_type.upper()} — {timestamp}\n"
            f"{'═'*70}\n\n"
            f"{content}\n\n"
        )
        self.ai_output.see(tk.END)

        usage = self.ai.get_usage_stats()
        self.status_var.set(
            f"AI analysis complete ({analysis_type}). Tokens: {usage['total_tokens']:,} | Cost: ~${usage['estimated_cost_usd']:.4f}"
        )

    def _display_ai_error(self, error):
        self.ai_output.insert(tk.END, f"\n❌ AI Error: {error}\n")
        self.status_var.set(f"AI error: {error[:60]}")

    def _ai_ask(self):
        question = self.ai_ask_var.get().strip()
        if not question:
            return
        if not self.ai.is_configured():
            messagebox.showwarning("AI Not Configured", "Configure API key in Settings first.")
            return

        self.status_var.set("Sending question to AI...")
        self.root.update_idletasks()

        def _worker():
            try:
                result = self.ai.ask_custom_question(question, self.document_text[:2000] if self.document_text else "")
                self.root.after(0, self._display_ai_result, "custom", result)
            except Exception as e:
                self.root.after(0, self._display_ai_error, str(e))

        threading.Thread(target=_worker, daemon=True).start()
        self.ai_ask_var.set("")

    # ══════════════════════════════════════════════════════════════════════════
    # DICTIONARY
    # ══════════════════════════════════════════════════════════════════════════

    def _populate_dictionary_tree(self, filter_text="", category="All"):
        for item in self.dict_tree.get_children():
            self.dict_tree.delete(item)

        for term_key, term_data in LEGAL_DICTIONARY.items():
            normalized = _normalize_legal_term(term_key, term_data)
            if filter_text and filter_text.lower() not in term_key.lower() and filter_text.lower() not in normalized["preferred_form"].lower():
                continue
            if category != "All" and normalized["category"] != category:
                continue

            self.dict_tree.insert("", tk.END, iid=term_key, values=(
                term_key.replace("_", " ").title(),
                normalized["category"],
                normalized["preferred_form"],
                normalized["source"][:50],
            ))

    def _search_dictionary(self):
        query = self.dict_search_var.get().strip()
        category = self.dict_cat_var.get()
        self._populate_dictionary_tree(query, category)

    def _on_dict_select(self, event):
        sel = self.dict_tree.selection()
        if not sel:
            return
        term_key = sel[0]
        term_data = LEGAL_DICTIONARY.get(term_key)

        self.dict_def_text.delete("1.0", tk.END)
        if not term_data:
            return
        normalized = _normalize_legal_term(term_key, term_data)

        self.dict_def_text.insert(tk.END, f"TERM: {term_key.replace('_', ' ').title()}\n")
        self.dict_def_text.insert(tk.END, f"{'═'*60}\n\n")
        self.dict_def_text.insert(tk.END, f"DEFINITION:\n{normalized['definition']}\n\n")
        self.dict_def_text.insert(tk.END, f"PREFERRED FORM: {normalized['preferred_form']}\n")
        self.dict_def_text.insert(tk.END, f"CATEGORY: {normalized['category']}\n")
        self.dict_def_text.insert(tk.END, f"SOURCE: {normalized['source']}\n\n")

        if normalized["aliases"]:
            self.dict_def_text.insert(tk.END, f"ALIASES: {', '.join(normalized['aliases'])}\n")
        if normalized["misuses"]:
            self.dict_def_text.insert(tk.END, f"\n⚠️ MISUSES TO AVOID:\n")
            for m in normalized["misuses"]:
                self.dict_def_text.insert(tk.END, f"  ✗ '{m}'\n")

    def _quick_dict_lookup(self):
        query = self.dict_entry_var.get().strip().lower()
        if not query:
            self.dict_result_label.config(text="Enter a term to look up.")
            return

        # Search dictionary
        for term_key, term_data in LEGAL_DICTIONARY.items():
            normalized = _normalize_legal_term(term_key, term_data)
            if query == term_key.lower() or query in [a.lower() for a in normalized["aliases"]]:
                self.dict_result_label.config(
                    text=f"✓ {normalized['preferred_form']}\n{normalized['definition'][:200]}..."
                )
                return

        self.dict_result_label.config(text=f"'{query}' not found in dictionary.\nTry the Dictionary tab for a full search.")

    def _dict_lookup_dialog(self):
        """Open a full dictionary lookup dialog."""
        self.notebook.select(self.dict_tab)

    # ══════════════════════════════════════════════════════════════════════════
    # SETTINGS & DIALOGS
    # ══════════════════════════════════════════════════════════════════════════

    def _settings_dialog(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("API Key Settings")
        dlg.geometry("600x350")
        dlg.transient(self.root)
        dlg.grab_set()

        ttk.Label(dlg, text="API Configuration", style="Subheader.TLabel").pack(padx=10, pady=8)
        ttk.Label(dlg, text="API keys are stored in memory only (not saved to disk).",
                   foreground=COLORS["text_secondary"]).pack(padx=10)

        # AI Provider Selection
        provider_frame = ttk.LabelFrame(dlg, text="AI Provider", padding=10)
        provider_frame.pack(fill=tk.X, padx=10, pady=5)
        
        provider_var = tk.StringVar(value=self.ai.provider)
        ttk.Radiobutton(provider_frame, text="OpenAI (GPT-4)", variable=provider_var, value="openai").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(provider_frame, text="Google (Gemini)", variable=provider_var, value="gemini").pack(side=tk.LEFT, padx=10)

        # OpenAI Frame
        openai_frame = ttk.LabelFrame(dlg, text="OpenAI Configuration", padding=10)
        
        # Gemini Frame
        gemini_frame = ttk.LabelFrame(dlg, text="Gemini Configuration", padding=10)

        def _toggle_provider_frames(*args):
            if provider_var.get() == "openai":
                gemini_frame.pack_forget()
                openai_frame.pack(fill=tk.X, padx=10, pady=5)
            else:
                openai_frame.pack_forget()
                gemini_frame.pack(fill=tk.X, padx=10, pady=5)
        
        provider_var.trace_add("write", _toggle_provider_frames)

        # OpenAI Content
        ttk.Label(openai_frame, text="OpenAI API Key:").pack(anchor=tk.W)
        openai_var = tk.StringVar(value=os.environ.get("OPENAI_API_KEY", "") if self.ai.provider == "openai" else "")
        ttk.Entry(openai_frame, textvariable=openai_var, width=60, show="*").pack(fill=tk.X, pady=2)

        # Gemini Content
        ttk.Label(gemini_frame, text="Gemini API Key:").pack(anchor=tk.W)
        gemini_var = tk.StringVar(value=os.environ.get("GEMINI_API_KEY", "") if self.ai.provider == "gemini" else "")
        ttk.Entry(gemini_frame, textvariable=gemini_var, width=60, show="*").pack(fill=tk.X, pady=2)
        ttk.Label(gemini_frame, text="Get a key at: https://aistudio.google.com/", foreground=COLORS["info"]).pack(anchor=tk.W)

        # Model
        model_frame = ttk.LabelFrame(dlg, text="AI Model", padding=10)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        
        model_var = tk.StringVar(value=self.ai.model)
        model_dropdown = ttk.Combobox(model_frame, textvariable=model_var, width=30, state="readonly")
        model_dropdown.pack(anchor=tk.W)

        def _update_models(*args):
            if provider_var.get() == "openai":
                model_dropdown['values'] = ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
                if model_var.get() not in model_dropdown['values']:
                    model_var.set("gpt-4o")
            else:
                model_dropdown['values'] = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"]
                if model_var.get() not in model_dropdown['values']:
                    model_var.set("gemini-1.5-pro")

        provider_var.trace_add("write", _update_models)
        _toggle_provider_frames()
        _update_models()

        def _save():
            # Update AI
            self.ai.provider = provider_var.get()
            self.ai.model = model_var.get()
            
            if self.ai.provider == "openai":
                self.ai.api_key = openai_var.get().strip()
                if self.ai.api_key:
                    self.ai.session.headers.update({"Authorization": f"Bearer {self.ai.api_key}"})
                    os.environ["OPENAI_API_KEY"] = self.ai.api_key
            else:
                self.ai.api_key = gemini_var.get().strip()
                if self.ai.api_key:
                    os.environ["GEMINI_API_KEY"] = self.ai.api_key
                    if hasattr(self.ai, 'GEMINI_AVAILABLE') and self.ai.GEMINI_AVAILABLE:
                        import google.generativeai as genai
                        genai.configure(api_key=self.ai.api_key)

            self._update_ai_status()
            dlg.destroy()
            messagebox.showinfo("Settings Saved", f"AI configured to use {self.ai.provider.upper()} ({self.ai.model}).")

        ttk.Button(dlg, text="Save Settings", command=_save, style="Success.TButton").pack(pady=10)

    def _ai_question_dialog(self):
        """Open AI question dialog."""
        self.notebook.select(self.ai_tab)
        self.ai_ask_var.set("")
        self.root.focus_set()

    # ══════════════════════════════════════════════════════════════════════════
    # RESEARCH MAP (VERITAS Phase 4)
    # ══════════════════════════════════════════════════════════════════════════

    def _build_research_tab(self, parent):
        header = ttk.Frame(parent)
        header.pack(fill=tk.X, padx=8, pady=(8, 0))
        ttk.Label(header, text="🔬 Research Map", style="Subheader.TLabel").pack(side=tk.LEFT)

        q_frame = ttk.LabelFrame(parent, text="Research Question", padding=8)
        q_frame.pack(fill=tk.X, padx=8, pady=6)

        self.research_q_var = tk.StringVar()
        q_entry = ttk.Entry(q_frame, textvariable=self.research_q_var, font=("Segoe UI", 11))
        q_entry.pack(fill=tk.X, pady=2)
        q_entry.bind("<Return>", lambda e: self._run_research())

        btn_row = ttk.Frame(q_frame)
        btn_row.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(btn_row, text="🔬 Run Research", command=self._run_research,
                   style="Success.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="💾 Save Report",
                   command=self._save_research_report).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="🌐 Open HTML",
                   command=self._open_research_html).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_row, text="Clear",
                   command=self._clear_research).pack(side=tk.RIGHT, padx=2)

        self.research_status_var = tk.StringVar(
            value="Ready — enter a question and press Run Research")
        ttk.Label(parent, textvariable=self.research_status_var,
                  foreground=COLORS["info"], font=("Segoe UI", 9)).pack(
            anchor=tk.W, padx=8, pady=2)

        self.research_progress = ttk.Progressbar(
            parent, orient=tk.HORIZONTAL, mode="determinate", maximum=12)
        self.research_progress.pack(fill=tk.X, padx=8, pady=(0, 4))

        self.research_output = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=("Consolas", 10),
            bg=COLORS["input_bg"], fg=COLORS["text_primary"],
            insertbackground="white", relief=tk.FLAT)
        self.research_output.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

    def _on_pipeline_status(self, step: int, total: int, message: str):
        def _update():
            self.research_status_var.set(message)
            self.research_progress["value"] = step
            self.root.update_idletasks()
        self.root.after(0, _update)

    def _run_research(self):
        question = self.research_q_var.get().strip() if hasattr(self, "research_q_var") else ""
        if not question and self.document_text:
            meta_name = self.document_metadata.get("file_name", "loaded document")
            question = f"Research the content of: {meta_name}"
        if not question:
            messagebox.showwarning("No Input",
                "Enter a research question, or load a document first.")
            return

        self.notebook.select(self.research_tab)
        self.research_output.delete("1.0", tk.END)
        self.research_output.insert(tk.END, "Running research pipeline…\n")
        self.research_progress["value"] = 0
        self.research_status_var.set("Starting pipeline…")
        self.root.update_idletasks()

        def _worker():
            try:
                result = self.pipeline.run(
                    question=question,
                    doc_text=self.document_text or None,
                    doc_metadata=self.document_metadata or None,
                )
                self.research_result = result
                self.root.after(0, self._display_research_result, result)
            except Exception as e:
                self.root.after(0, self._display_research_error, str(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _display_research_result(self, result: dict):
        out = self.research_output
        out.delete("1.0", tk.END)

        out.tag_configure("h1",    font=("Segoe UI", 13, "bold"), foreground="#9ab")
        out.tag_configure("h2",    font=("Segoe UI", 11, "bold"), foreground="#8ab")
        out.tag_configure("label", font=("Segoe UI", 10, "bold"), foreground="#cde")
        out.tag_configure("dim",   foreground=COLORS["text_secondary"])
        out.tag_configure("warn",  foreground=COLORS["warning"])
        out.tag_configure("sep",   foreground=COLORS["accent"])

        def w(text, tag=None):
            out.insert(tk.END, text, tag) if tag else out.insert(tk.END, text)

        SEP = "─" * 70 + "\n"

        w("VERITAS RESEARCH MAP\n", "h1")
        w(f"Question: {result.get('question','')}\n", "dim")
        w(f"Generated: {result.get('timestamp','')}\n\n", "dim")

        if result.get("restatement"):
            w(SEP, "sep"); w("2. Plain-English Restatement\n", "h2")
            w(result["restatement"] + "\n\n")

        defs = result.get("definitions", {})
        if defs:
            w(SEP, "sep"); w("3. Key Terms & Definitions\n", "h2")
            for term, d in defs.items():
                w(f"  {term}\n", "label")
                w(f"    Plain English: {d.get('plain_english') or '—'}\n", "dim")
                w(f"    Doctrinal:     {d.get('doctrinal') or '—'}\n\n", "dim")

        hits = result.get("corpus_hits", [])
        w(SEP, "sep"); w("4. Corpus Findings\n", "h2")
        if hits:
            for i, h in enumerate(hits, 1):
                w(f"  [{i}] {h.get('title','')} ", "label")
                w(f"[{h.get('source_type','')}] {h.get('doc_date','')}\n", "dim")
                snippet = h.get("snippet","").replace("[","«").replace("]","»")
                if snippet: w(f"      {snippet}\n\n")
        else:
            w("  No corpus documents matched.\n  Add documents to corpus/primary/ or corpus/secondary/\n\n", "warn")

        path = result.get("citation_path", [])
        w(SEP, "sep"); w("5. Citation & Doctrine Path\n", "h2")
        if path:
            for i, doc in enumerate(path, 1):
                w(f"  [{i}] {doc.get('title','')} ", "label")
                w(f"({doc.get('source_type','')}, {doc.get('doc_date','')}) {doc.get('self_cite','')}\n", "dim")
        else:
            w("  No citation chain resolved.\n", "dim")
        w("\n")

        drift = result.get("drift_flags", [])
        w(SEP, "sep"); w("6. Semantic Drift Flags\n", "h2")
        if drift:
            for d in drift:
                w(f"  ⚠ {d.get('term','')} in {d.get('doc_title','')} (similarity: {d.get('similarity','')})\n", "warn")
        else:
            w("  No drift detected.\n", "dim")
        w("\n")

        gaps = result.get("gaps", [])
        w(SEP, "sep"); w("7. Missing Information Log\n", "h2")
        if gaps:
            for g in gaps:
                w(f"  [{g.get('gap_type','')}] {g.get('value','')}\n", "warn")
        else:
            w("  No gaps logged.\n", "dim")
        w("\n")

        sources = result.get("source_list", [])
        w(SEP, "sep"); w("8. Source List\n", "h2")
        if sources:
            for s in sources:
                w(f"  {s.get('title','')} ", "label")
                w(f"[{s.get('source_type','')}] {s.get('doc_date','')} — {s.get('self_cite','') or 'no citation'}\n", "dim")
        else:
            w("  No sources in corpus.\n", "dim")

        errs = result.get("errors", [])
        if errs:
            w("\n" + SEP, "sep"); w("Pipeline Notes\n", "h2")
            for e in errs: w(f"  • {e}\n", "dim")

        out.see("1.0")
        self.research_status_var.set(
            f"Complete — {len(hits)} corpus hits · {len(path)} citation entries · {len(gaps)} gaps")
        self.research_progress["value"] = 12
        self.status_var.set("Research pipeline complete.")

    def _display_research_error(self, error: str):
        self.research_output.insert(tk.END, f"\n❌ Pipeline error: {error}\n")
        self.research_status_var.set(f"Error: {error[:80]}")
        self.status_var.set(f"Research pipeline error: {error[:60]}")

    def _save_research_report(self):
        if not self.research_result:
            messagebox.showwarning("No Research", "Run a research query first.")
            return
        try:
            folder = self.pipeline.save_report(self.research_result)
            self._last_report_folder = folder
            messagebox.showinfo("Report Saved", f"Report saved to:\n{folder}")
            self.status_var.set(f"Report saved: {folder}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _open_research_html(self):
        if not self._last_report_folder:
            self._save_research_report()
        if self._last_report_folder:
            html_path = os.path.join(self._last_report_folder, "report.html")
            if os.path.isfile(html_path):
                webbrowser.open(f"file://{html_path}")
            else:
                messagebox.showwarning("No HTML",
                    f"report.html not found in:\n{self._last_report_folder}")

    def _clear_research(self):
        self.research_output.delete("1.0", tk.END)
        self.research_result = {}
        self._last_report_folder = None
        self.research_progress["value"] = 0
        self.research_status_var.set("Ready — enter a question and press Run Research")

    # ══════════════════════════════════════════════════════════════════════════
    # EXPORT
    # ══════════════════════════════════════════════════════════════════════════

    def _export_html(self):
        if not self.analysis_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export HTML Report",
            defaultextension=".html",
            filetypes=[("HTML", "*.html"), ("All", "*.*")],
            initialfile=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        )
        if not path:
            return

        try:
            self.report_generator.generate_html_report(
                self._results_for_display(), self.document_metadata, path
            )
            # Ask to open
            if messagebox.askyesno("Report Saved", f"Report saved to:\n{path}\n\nOpen in browser?"):
                webbrowser.open(f"file://{path}")
            self.status_var.set(f"HTML report exported: {path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def _export_txt(self):
        if not self.analysis_results:
            messagebox.showwarning("No Results", "Run an analysis first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export Text Report",
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")],
            initialfile=f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        )
        if not path:
            return

        try:
            self.report_generator.generate_text_report(
                self._results_for_display(), self.document_metadata, path
            )
            messagebox.showinfo("Report Saved", f"Report saved to:\n{path}")
            self.status_var.set(f"Text report exported: {path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))


# ══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()

    # Set DPI awareness on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = LegalAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
