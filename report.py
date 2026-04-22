from datetime import datetime

def generate_report(defects, image_path, output_path):
    """Generate a structured defect inspection report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    high = [d for d in defects if d["severity"] == "HIGH"]
    medium = [d for d in defects if d["severity"] == "MEDIUM"]
    low = [d for d in defects if d["severity"] == "LOW"]

    defect_types = {}
    for d in defects:
        defect_types[d["type"]] = defect_types.get(d["type"], 0) + 1

    status = "FAIL" if high else "PASS" if not defects else "REVIEW"

    report = f"""
╔══════════════════════════════════════════════════════╗
║         INDUSTRIAL DEFECT INSPECTION REPORT          ║
╚══════════════════════════════════════════════════════╝

  Timestamp   : {timestamp}
  Image       : {image_path}
  Output      : {output_path}
  Status      : {status}

──────────────────────────────────────────────────────
  SUMMARY
──────────────────────────────────────────────────────
  Total defects found : {len(defects)}
  HIGH severity       : {len(high)}
  MEDIUM severity     : {len(medium)}
  LOW severity        : {len(low)}

──────────────────────────────────────────────────────
  DEFECT BREAKDOWN
──────────────────────────────────────────────────────"""

    for defect_type, count in defect_types.items():
        report += f"\n  {defect_type:<20} : {count} instance(s)"

    if defects:
        report += f"""

──────────────────────────────────────────────────────
  DETAILED FINDINGS
──────────────────────────────────────────────────────"""
        for i, d in enumerate(defects, 1):
            report += f"""
  [{i}] Type       : {d['type']}
      Confidence : {d['confidence']:.1%}
      Severity   : {d['severity']}
      Area       : {d['area_px']} px²
      Location   : {d['bbox']}"""

    report += f"""

──────────────────────────────────────────────────────
  RECOMMENDATION
──────────────────────────────────────────────────────
  {'⛔ REJECT — High severity defects detected. Do not ship.' if status == 'FAIL'
    else '✅ PASS — No significant defects detected.' if status == 'PASS'
    else '⚠️  REVIEW — Minor defects present. Manual inspection advised.'}

╚══════════════════════════════════════════════════════╝
"""
    print(report)
    return report, status