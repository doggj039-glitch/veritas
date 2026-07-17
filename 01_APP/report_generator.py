# Copyright (c) contributors. Licensed under the Apache License, Version 2.0.
"""
Report Generator Module
Generates analysis reports in various formats (HTML, PDF, TXT).
"""

import os
from datetime import datetime
from privacy_scrubber import scrub_party_identifiers


class ReportGenerator:
    """Generate formatted analysis reports."""

    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_html_report(self, analysis_results, document_metadata, output_path):
        """Generate a detailed HTML report."""
        analysis_results = scrub_party_identifiers(analysis_results)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VERITAS Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
            color: white;
            padding: 30px 40px;
        }}
        .header h1 {{
            font-size: 28px;
            margin-bottom: 5px;
        }}
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .content {{
            padding: 30px 40px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #1a237e;
            border-bottom: 2px solid #e8eaf6;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .section h3 {{
            color: #283593;
            margin: 15px 0 10px;
        }}
        .alert {{
            padding: 15px 20px;
            border-radius: 6px;
            margin: 15px 0;
        }}
        .alert-high {{
            background: #ffebee;
            border-left: 4px solid #c62828;
            color: #b71c1c;
        }}
        .alert-medium {{
            background: #fff3e0;
            border-left: 4px solid #e65100;
            color: #bf360c;
        }}
        .alert-low {{
            background: #e8f5e9;
            border-left: 4px solid #2e7d32;
            color: #1b5e20;
        }}
        .alert-info {{
            background: #e3f2fd;
            border-left: 4px solid #1565c0;
            color: #0d47a1;
        }}
        .breach-card {{
            background: #fafafa;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 20px;
            margin: 15px 0;
        }}
        .breach-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-high {{ background: #ffcdd2; color: #c62828; }}
        .badge-medium {{ background: #ffe0b2; color: #e65100; }}
        .badge-low {{ background: #c8e6c9; color: #2e7d32; }}
        .confidence-bar {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .confidence-fill {{
            height: 100%;
            border-radius: 10px;
        }}
        .confidence-fill.high {{ background: #c62828; }}
        .confidence-fill.medium {{ background: #e65100; }}
        .confidence-fill.low {{ background: #2e7d32; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            padding: 10px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #e8eaf6;
            color: #283593;
            font-weight: 600;
        }}
        .keyword-tag {{
            display: inline-block;
            background: #e8eaf6;
            color: #283593;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin: 2px;
        }}
        .test-item {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 10px 15px;
            margin: 8px 0;
        }}
        .test-issue {{
            border-left: 3px solid #c62828;
        }}
        .test-ok {{
            border-left: 3px solid #2e7d32;
        }}
        .recommendation {{
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 4px;
            background: #fff9c4;
            border-left: 3px solid #f9a825;
        }}
        .recommendation.priority {{
            border-left-color: #c62828;
            background: #ffebee;
        }}
        .url-link {{
            color: #1565c0;
            text-decoration: none;
            word-break: break-all;
        }}
        .url-link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background: #f5f5f5;
            padding: 20px 40px;
            text-align: center;
            font-size: 12px;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        .meta-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }}
        .meta-item {{
            background: #f5f5f5;
            padding: 10px 15px;
            border-radius: 4px;
        }}
        .meta-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .meta-value {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }}
        .remedy-card {{
            background: #e8f5e9;
            border: 1px solid #a5d6a7;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
        }}
        .disclaimer {{
            background: #fff3e0;
            border: 1px solid #ffe0b2;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            font-size: 13px;
            color: #e65100;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>VERITAS Analysis Report</h1>
            <p>Constitutional analysis report</p>
            <p>Generated: {self.timestamp}</p>
        </div>
        <div class="content">
"""

        # Document Metadata
        meta = document_metadata
        html += f"""
            <div class="section">
                <h2>📋 Document Information</h2>
                <div class="meta-grid">
                    <div class="meta-item">
                        <div class="meta-label">File Name</div>
                        <div class="meta-value">{meta.get('file_name', 'N/A')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Format</div>
                        <div class="meta-value">{meta.get('format', 'N/A')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Words</div>
                        <div class="meta-value">{meta.get('word_count', 'N/A'):,}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Paragraphs</div>
                        <div class="meta-value">{meta.get('paragraph_count', 'N/A')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Characters</div>
                        <div class="meta-value">{meta.get('char_count', 'N/A'):,}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Sentences</div>
                        <div class="meta-value">{meta.get('sentence_count', 'N/A')}</div>
                    </div>
                </div>
            </div>
"""

        # Disclaimer
        html += """
            <div class="disclaimer">
                <strong>⚠️ DISCLAIMER:</strong> This analysis is generated by an automated tool and does not constitute legal advice.
                All findings should be reviewed by a qualified legal professional. Keyword and pattern matching
                cannot replace the exercise of legal judgment.
            </div>
"""

        terminology_issues = analysis_results.get("terminology_issues", [])
        deflection_issues = analysis_results.get("deflection_issues", [])

        # Overall Assessment
        html += f"""
            <div class="section">
                <h2>📊 Overall Assessment</h2>
                <p><strong>Terminology issues identified:</strong> {len(terminology_issues)}</p>
                <p><strong>Deflection / ambiguity patterns identified:</strong> {len(deflection_issues)}</p>
            </div>
"""

        # Terminology Findings
        html += """
            <div class="section">
                <h2>📖 Terminology Findings</h2>
"""
        if terminology_issues:
            for issue in terminology_issues:
                html += f"""
                <div class="breach-card">
                    <h3>{issue.get('term', '')}</h3>
                    <p><em>{issue.get('issue', '')}</em></p>
                    <p><strong>Preferred form:</strong> {issue.get('correct_form', '')}</p>
                    <p><strong>Occurrences:</strong> {issue.get('count', 0)}</p>
                    <p><strong>Source:</strong> {issue.get('source', '')}</p>
"""
                if issue.get("matches"):
                    html += "                    <p><strong>Example matches:</strong></p><ul>"
                    for m in issue["matches"]:
                        html += f"<li>{m}</li>"
                    html += "</ul>"
                html += "                </div>\n"
        else:
            html += '            <div class="alert alert-low">No terminology issues identified in this document.</div>\n'
        html += "            </div>\n"

        # Deflection / Ambiguity Findings
        html += """
            <div class="section">
                <h2>🚫 Deflection / Ambiguity Findings</h2>
"""
        if deflection_issues:
            for issue in deflection_issues:
                sev = (issue.get("severity") or "low").lower()
                html += f"""
                <div class="breach-card">
                    <div class="breach-header">
                        <h3>{issue.get('pattern_type', '')}</h3>
                        <span class="badge badge-{sev}">{(issue.get('severity') or '').upper()}</span>
                    </div>
                    <p><em>{issue.get('description', '')}</em></p>
                    <p><strong>Occurrences:</strong> {issue.get('count', 0)}</p>
                    <p><strong>Suggestion:</strong> {issue.get('suggestion', '')}</p>
"""
                if issue.get("matches"):
                    html += "                    <p><strong>Example matches:</strong></p><ul>"
                    for m in issue["matches"]:
                        html += f"<li>{m}</li>"
                    html += "</ul>"
                html += "                </div>\n"
        else:
            html += '            <div class="alert alert-low">No deflection or ambiguity patterns identified in this document.</div>\n'
        html += "            </div>\n"

        # Footer
        html += f"""
            <div class="footer">
                <p>Generated by VERITAS v{os.environ.get("APP_VERSION", "1.0")} — {self.timestamp}</p>
                <p>This report does not constitute legal advice. Consult a qualified legal professional.</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

        # Write report
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def generate_text_report(self, analysis_results, document_metadata, output_path):
        """Generate a plain text report."""
        analysis_results = scrub_party_identifiers(analysis_results)
        lines = ["=" * 80, "VERITAS ANALYSIS REPORT",
                 "Constitutional analysis report",
                 f"Generated: {self.timestamp}", "=" * 80]

        # Document Info
        meta = document_metadata
        lines.append(f"\nDOCUMENT INFORMATION")
        lines.append("-" * 40)
        lines.append(f"  File:     {meta.get('file_name', 'N/A')}")
        lines.append(f"  Format:   {meta.get('format', 'N/A')}")
        lines.append(f"  Words:    {meta.get('word_count', 'N/A'):,}")
        lines.append(f"  Paragraphs: {meta.get('paragraph_count', 'N/A')}")

        # Disclaimer
        lines.append(f"\nDISCLAIMER: This analysis does not constitute legal advice.")

        terminology_issues = analysis_results.get("terminology_issues", [])
        deflection_issues = analysis_results.get("deflection_issues", [])

        # Overall Assessment
        lines.append(f"\nOVERALL ASSESSMENT")
        lines.append("-" * 40)
        lines.append(f"  Terminology issues identified: {len(terminology_issues)}")
        lines.append(f"  Deflection / ambiguity patterns identified: {len(deflection_issues)}")

        # Terminology Findings
        lines.append(f"\nTERMINOLOGY FINDINGS ({len(terminology_issues)} found)")
        lines.append("=" * 60)
        for issue in terminology_issues:
            lines.append(f"\n  {issue.get('term', '')}")
            lines.append(f"  Issue: {issue.get('issue', '')}")
            lines.append(f"  Preferred form: {issue.get('correct_form', '')}")
            lines.append(f"  Occurrences: {issue.get('count', 0)}")
            lines.append(f"  Source: {issue.get('source', '')}")
            if issue.get("matches"):
                lines.append(f"  Example matches: {', '.join(issue['matches'])}")

        # Deflection / Ambiguity Findings
        lines.append(f"\nDEFLECTION / AMBIGUITY FINDINGS ({len(deflection_issues)} found)")
        lines.append("=" * 60)
        for issue in deflection_issues:
            lines.append(f"\n  {issue.get('pattern_type', '')} ({(issue.get('severity') or '').upper()})")
            lines.append(f"  {issue.get('description', '')}")
            lines.append(f"  Occurrences: {issue.get('count', 0)}")
            lines.append(f"  Suggestion: {issue.get('suggestion', '')}")
            if issue.get("matches"):
                lines.append(f"  Example matches: {', '.join(issue['matches'])}")

        lines.append(f"\n{'=' * 80}")
        lines.append(f"End of Report — {self.timestamp}")
        lines.append("=" * 80)

        report_text = "\n".join(lines)
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        return output_path

    # ──────────────────────────────────────────────────────────────────────────
    # VERITAS Research Map Reports (Phase 5)
    # ──────────────────────────────────────────────────────────────────────────

    def generate_research_html(self, research_result: dict, output_path: str) -> str:
        """
        Generate a full HTML research-map report from a pipeline result dict.

        Parameters
        ----------
        research_result : dict as returned by PipelineRunner.run()
        output_path     : Destination .html file path

        Returns
        -------
        str — output_path
        """
        def esc(s):
            return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        q         = esc(research_result.get("question", ""))
        ts        = esc(research_result.get("timestamp", self.timestamp))
        version   = esc(research_result.get("pipeline_version", "4.0"))
        restate   = esc(research_result.get("restatement", ""))
        defs      = research_result.get("definitions", {})
        hits      = research_result.get("corpus_hits", [])
        path      = research_result.get("citation_path", [])
        drift     = research_result.get("drift_flags", [])
        gaps      = research_result.get("gaps", [])
        sources   = research_result.get("source_list", [])
        errors    = research_result.get("errors", [])

        # ── CSS ──────────────────────────────────────────────────────────────
        css = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f5; color: #222; line-height: 1.6; padding: 20px;
        }
        .container {
            max-width: 1100px; margin: 0 auto; background: white;
            border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #0d2b4e 0%, #1a3f6e 50%, #1e5288 100%);
            color: white; padding: 30px 40px;
        }
        .header h1 { font-size: 26px; margin-bottom: 4px; }
        .header .sub { opacity: 0.85; font-size: 13px; margin-top: 4px; }
        .content { padding: 30px 40px; }
        .section { margin-bottom: 32px; }
        .section h2 {
            color: #0d2b4e; border-bottom: 2px solid #dde3ea;
            padding-bottom: 8px; margin-bottom: 14px; font-size: 18px;
        }
        .section-num {
            display: inline-block; background: #0d2b4e; color: white;
            border-radius: 50%; width: 26px; height: 26px; text-align: center;
            line-height: 26px; font-size: 12px; font-weight: bold;
            margin-right: 8px;
        }
        table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
        th { background: #dde3ea; color: #0d2b4e; padding: 9px 12px;
             text-align: left; font-weight: 600; }
        td { padding: 8px 12px; border-bottom: 1px solid #eee; vertical-align: top; }
        tr:hover td { background: #f7f9fc; }
        .tag {
            display: inline-block; padding: 2px 8px; border-radius: 10px;
            font-size: 11px; font-weight: 600; text-transform: uppercase;
        }
        .tag-primary { background: #dbeafe; color: #1e40af; }
        .tag-secondary { background: #f3f4f6; color: #374151; }
        .tag-gap { background: #fef3c7; color: #92400e; }
        .tag-drift { background: #fee2e2; color: #991b1b; }
        .empty { color: #888; font-style: italic; padding: 10px 0; }
        .disclaimer {
            background: #fff7ed; border: 1px solid #fed7aa;
            border-radius: 6px; padding: 12px 16px;
            font-size: 12px; color: #9a3412; margin-bottom: 24px;
        }
        .footer {
            background: #f5f7fa; padding: 18px 40px; text-align: center;
            font-size: 12px; color: #666; border-top: 1px solid #e0e0e0;
        }
        .restate-box {
            background: #f0f7ff; border-left: 4px solid #1e5288;
            padding: 14px 18px; border-radius: 4px; color: #1a2a3a;
        }
        .gap-row td:first-child { font-weight: 600; color: #92400e; }
        .drift-row td:first-child { font-weight: 600; color: #991b1b; }
        code { background: #f3f4f6; padding: 1px 5px; border-radius: 3px;
               font-size: 12px; font-family: monospace; }
        """

        # ── Sections ─────────────────────────────────────────────────────────

        # 1 — Header / Query
        sec1 = f"""
        <div class="section">
            <h2><span class="section-num">1</span>Research Query</h2>
            <table>
                <tr><td><strong>Question</strong></td><td>{q}</td></tr>
                <tr><td><strong>Generated</strong></td><td>{ts}</td></tr>
                <tr><td><strong>Pipeline</strong></td><td>VERITAS v{version}</td></tr>
            </table>
        </div>"""

        # 2 — Restatement
        sec2 = f"""
        <div class="section">
            <h2><span class="section-num">2</span>Plain-English Restatement</h2>
            {"<div class='restate-box'>" + restate + "</div>" if restate else "<p class='empty'>No restatement available (AI not configured).</p>"}
        </div>"""

        # 3 — Terms & Definitions
        if defs:
            rows = ""
            for term, d in defs.items():
                plain = esc(d.get("plain_english") or "—")
                doc   = esc(d.get("doctrinal") or "—")
                hist  = esc(d.get("historical_context") or "—")
                rows += f"<tr><td><strong>{esc(term)}</strong></td><td>{plain}</td><td>{doc}</td><td>{hist}</td></tr>"
            sec3 = f"""
        <div class="section">
            <h2><span class="section-num">3</span>Key Terms &amp; Definitions</h2>
            <table>
                <thead><tr><th>Term</th><th>Plain English</th><th>Doctrinal</th><th>Historical Context</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
        else:
            sec3 = """
        <div class="section">
            <h2><span class="section-num">3</span>Key Terms &amp; Definitions</h2>
            <p class="empty">No terms identified.</p>
        </div>"""

        # 4 — Corpus Findings
        if hits:
            rows = ""
            for h in hits:
                stype = h.get("source_type", "")
                tag   = "tag-primary" if stype == "primary" else "tag-secondary"
                snip  = esc(h.get("snippet", "")).replace("[", "<mark>").replace("]", "</mark>")
                rows += (
                    f"<tr><td><strong>{esc(h.get('title',''))}</strong></td>"
                    f"<td><span class='tag {tag}'>{esc(stype)}</span></td>"
                    f"<td>{esc(h.get('doc_date','') or '—')}</td>"
                    f"<td>{snip}</td></tr>"
                )
            sec4 = f"""
        <div class="section">
            <h2><span class="section-num">4</span>Corpus Findings</h2>
            <table>
                <thead><tr><th>Title</th><th>Type</th><th>Date</th><th>Excerpt</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
        else:
            sec4 = """
        <div class="section">
            <h2><span class="section-num">4</span>Corpus Findings</h2>
            <p class="empty">No corpus documents matched. Add documents to
            <code>corpus/primary/</code> or <code>corpus/secondary/</code> and re-run.</p>
        </div>"""

        # 5 — Citation & Doctrine Path
        if path:
            items = ""
            for i, doc in enumerate(path, 1):
                stype = doc.get("source_type", "")
                tag   = "tag-primary" if stype == "primary" else "tag-secondary"
                cite  = esc(doc.get("self_cite", "") or "")
                items += (
                    f"<tr><td>{i}</td>"
                    f"<td><strong>{esc(doc.get('title',''))}</strong></td>"
                    f"<td><span class='tag {tag}'>{esc(stype)}</span></td>"
                    f"<td>{esc(doc.get('doc_date','') or '—')}</td>"
                    f"<td><code>{cite}</code></td></tr>"
                )
            sec5 = f"""
        <div class="section">
            <h2><span class="section-num">5</span>Citation &amp; Doctrine Path</h2>
            <table>
                <thead><tr><th>#</th><th>Title</th><th>Type</th><th>Date</th><th>Citation</th></tr></thead>
                <tbody>{items}</tbody>
            </table>
        </div>"""
        else:
            sec5 = """
        <div class="section">
            <h2><span class="section-num">5</span>Citation &amp; Doctrine Path</h2>
            <p class="empty">No citation chain resolved.</p>
        </div>"""

        # 6 — Semantic Drift Flags
        if drift:
            rows = ""
            for d in drift:
                rows += (
                    f"<tr class='drift-row'>"
                    f"<td>{esc(d.get('term',''))}</td>"
                    f"<td>{esc(d.get('doc_title',''))}</td>"
                    f"<td>{esc(str(d.get('similarity','')))}</td>"
                    f"<td>{esc(d.get('usage_sample','')[:150])}</td></tr>"
                )
            sec6 = f"""
        <div class="section">
            <h2><span class="section-num">6</span>Semantic Drift Flags</h2>
            <table>
                <thead><tr><th>Term</th><th>Document</th><th>Similarity</th><th>Usage Sample</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
        else:
            sec6 = """
        <div class="section">
            <h2><span class="section-num">6</span>Semantic Drift Flags</h2>
            <p class="empty">No semantic drift detected.</p>
        </div>"""

        # 7 — Missing Information Log
        if gaps:
            rows = ""
            for g in gaps:
                rows += (
                    f"<tr class='gap-row'>"
                    f"<td><span class='tag tag-gap'>{esc(g.get('gap_type',''))}</span></td>"
                    f"<td>{esc(g.get('value',''))}</td>"
                    f"<td>{esc(g.get('source_doc_id','') or '—')}</td>"
                    f"<td>{esc(g.get('best_link','') or '—')}</td></tr>"
                )
            sec7 = f"""
        <div class="section">
            <h2><span class="section-num">7</span>Missing Information Log</h2>
            <table>
                <thead><tr><th>Type</th><th>Value</th><th>Source Doc</th><th>Reference</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
        else:
            sec7 = """
        <div class="section">
            <h2><span class="section-num">7</span>Missing Information Log</h2>
            <p class="empty">No gaps logged.</p>
        </div>"""

        # 8 — Source List
        if sources:
            rows = ""
            for s in sources:
                stype = s.get("source_type", "")
                tag   = "tag-primary" if stype == "primary" else "tag-secondary"
                rows += (
                    f"<tr><td><strong>{esc(s.get('title',''))}</strong></td>"
                    f"<td><span class='tag {tag}'>{esc(stype)}</span></td>"
                    f"<td>{esc(s.get('doc_date','') or '—')}</td>"
                    f"<td><code>{esc(s.get('self_cite','') or '—')}</code></td></tr>"
                )
            sec8 = f"""
        <div class="section">
            <h2><span class="section-num">8</span>Source List</h2>
            <table>
                <thead><tr><th>Title</th><th>Type</th><th>Date</th><th>Citation</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
        </div>"""
        else:
            sec8 = """
        <div class="section">
            <h2><span class="section-num">8</span>Source List</h2>
            <p class="empty">No sources used.</p>
        </div>"""

        # Pipeline errors (footer note, not a main section)
        err_html = ""
        if errors:
            items = "".join(f"<li>{esc(e)}</li>" for e in errors)
            err_html = f"""
        <div class="section">
            <h2>Pipeline Notes</h2>
            <ul style="font-size:13px;color:#666;padding-left:20px">{items}</ul>
        </div>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VERITAS Research Map — {q[:60]}</title>
<style>{css}</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🔬 VERITAS Research Map</h1>
    <div class="sub">Constitutional Research Engine — Pipeline v{version}</div>
    <div class="sub">Generated: {ts}</div>
  </div>
  <div class="content">
    <div class="disclaimer">
      ⚠️ <strong>RESEARCH AND STATISTICS TOOL ONLY — NOT LEGAL ADVICE — VERIFY ALL RESULTS.</strong>
      This report is produced by an automated pipeline. All findings must be independently verified.
    </div>
    {sec1}{sec2}{sec3}{sec4}{sec5}{sec6}{sec7}{sec8}{err_html}
  </div>
  <div class="footer">
    <p>VERITAS Research Map · Pipeline v{version} · {ts}</p>
    <p>This report does not constitute legal advice. Consult a qualified legal professional.</p>
  </div>
</div>
</body>
</html>"""

        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        return output_path

    def generate_research_text(self, research_result: dict, output_path: str) -> str:
        """
        Generate a plain-text research-map report from a pipeline result dict.

        Parameters
        ----------
        research_result : dict as returned by PipelineRunner.run()
        output_path     : Destination .txt file path

        Returns
        -------
        str — output_path
        """
        q       = research_result.get("question", "")
        ts      = research_result.get("timestamp", self.timestamp)
        version = research_result.get("pipeline_version", "4.0")
        W = 80

        lines = [
            "=" * W,
            "VERITAS RESEARCH MAP",
            "Constitutional Research Engine",
            f"Pipeline v{version}",
            f"Generated: {ts}",
            "=" * W,
            "",
            "RESEARCH AND STATISTICS TOOL ONLY — NOT LEGAL ADVICE — VERIFY ALL RESULTS",
            "",
        ]

        # 1 — Query
        lines += ["─" * W, "1. RESEARCH QUERY", "─" * W, f"  {q}", ""]

        # 2 — Restatement
        restate = research_result.get("restatement", "")
        lines += ["─" * W, "2. PLAIN-ENGLISH RESTATEMENT", "─" * W]
        lines.append(f"  {restate}" if restate else "  (No restatement — AI not configured.)")
        lines.append("")

        # 3 — Terms & Definitions
        defs = research_result.get("definitions", {})
        lines += ["─" * W, f"3. KEY TERMS & DEFINITIONS ({len(defs)} terms)", "─" * W]
        if defs:
            for term, d in defs.items():
                lines.append(f"  {term}")
                lines.append(f"    Plain English:      {d.get('plain_english') or '—'}")
                lines.append(f"    Doctrinal:          {d.get('doctrinal') or '—'}")
                lines.append(f"    Historical Context: {d.get('historical_context') or '—'}")
                lines.append("")
        else:
            lines += ["  No terms identified.", ""]

        # 4 — Corpus Findings
        hits = research_result.get("corpus_hits", [])
        lines += ["─" * W, f"4. CORPUS FINDINGS ({len(hits)} results)", "─" * W]
        if hits:
            for i, h in enumerate(hits, 1):
                lines.append(
                    f"  [{i}] {h.get('title','')} "
                    f"[{h.get('source_type','')}] {h.get('doc_date','') or ''}"
                )
                snip = h.get("snippet", "").replace("[", "«").replace("]", "»")
                if snip:
                    lines.append(f"      {snip}")
                lines.append("")
        else:
            lines += ["  No corpus documents matched.", ""]

        # 5 — Citation & Doctrine Path
        path = research_result.get("citation_path", [])
        lines += ["─" * W, f"5. CITATION & DOCTRINE PATH ({len(path)} entries)", "─" * W]
        if path:
            for i, doc in enumerate(path, 1):
                lines.append(
                    f"  [{i}] {doc.get('title','')} "
                    f"({doc.get('source_type','')}, {doc.get('doc_date','') or ''})"
                    f" — {doc.get('self_cite','') or 'no citation'}"
                )
            lines.append("")
        else:
            lines += ["  No citation chain resolved.", ""]

        # 6 — Drift Flags
        drift = research_result.get("drift_flags", [])
        lines += ["─" * W, f"6. SEMANTIC DRIFT FLAGS ({len(drift)} flags)", "─" * W]
        if drift:
            for d in drift:
                lines.append(
                    f"  ⚠ {d.get('term','')} in \"{d.get('doc_title','')}\" "
                    f"(similarity: {d.get('similarity','')})"
                )
            lines.append("")
        else:
            lines += ["  No drift detected.", ""]

        # 7 — Gaps
        gaps = research_result.get("gaps", [])
        lines += ["─" * W, f"7. MISSING INFORMATION LOG ({len(gaps)} entries)", "─" * W]
        if gaps:
            for g in gaps:
                lines.append(f"  [{g.get('gap_type','')}] {g.get('value','')}")
            lines.append("")
        else:
            lines += ["  No gaps logged.", ""]

        # 8 — Source List
        sources = research_result.get("source_list", [])
        lines += ["─" * W, f"8. SOURCE LIST ({len(sources)} sources)", "─" * W]
        if sources:
            for s in sources:
                lines.append(
                    f"  {s.get('title','')} [{s.get('source_type','')}] "
                    f"{s.get('doc_date','') or ''} — "
                    f"{s.get('self_cite','') or 'no citation'}"
                )
            lines.append("")
        else:
            lines += ["  No sources used.", ""]

        # Pipeline errors
        errors = research_result.get("errors", [])
        if errors:
            lines += ["─" * W, "PIPELINE NOTES", "─" * W]
            for e in errors:
                lines.append(f"  • {e}")
            lines.append("")

        lines += ["=" * W, f"End of VERITAS Research Map — {ts}", "=" * W]

        report_text = "\n".join(lines)
        os.makedirs(
            os.path.dirname(output_path) if os.path.dirname(output_path) else ".",
            exist_ok=True
        )
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        return output_path
