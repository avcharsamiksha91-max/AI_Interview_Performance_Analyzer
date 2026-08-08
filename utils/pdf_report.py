from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
import os


# =====================================================
# FINAL REPORT FUNCTION
# =====================================================

def generate_final_report(
    filename,
    candidate_name,
    final_score,

    # Voice
    voice_score,
    confidence,
    fluency,
    voice_clarity,
    speaking_speed,
    wpm,
    filler_words,

    # Video
    video_score,
    face_presence,
    face_position,
    eye_contact,
    expression,

    # Text
    transcript,
    ai_feedback,
    recommendations,
):

    # =================================================
    # CREATE REPORT FOLDER
    # =================================================

    folder = os.path.dirname(filename)

    if folder:
        os.makedirs(folder, exist_ok=True)

    # =================================================
    # CREATE PDF
    # =================================================

    pdf = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    # =================================================
    # TITLE
    # =================================================

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story.append(
        Paragraph(
            "AI Interview Performance Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    # =================================================
    # CANDIDATE
    # =================================================

    story.append(
        Paragraph(
            f"<b>Candidate:</b> {candidate_name}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 10))

    # =================================================
    # FINAL SCORE
    # =================================================

    story.append(
        Paragraph(
            "<b>FINAL INTERVIEW SCORE</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"<font size='20'><b>{final_score}/100</b></font>",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # =================================================
    # VOICE ANALYSIS
    # =================================================

    story.append(
        Paragraph(
            "Voice Analysis",
            styles["Heading2"]
        )
    )

    voice_data = [
        ["Metric", "Score"],

        ["Voice Score", f"{voice_score}/100"],

        ["Confidence", f"{confidence}%"],

        ["Fluency", f"{fluency}%"],

        ["Voice Clarity", f"{voice_clarity}%"],

        ["Speaking Speed", f"{speaking_speed}%"],

        ["Words Per Minute", str(wpm)],

        ["Filler Words", str(filler_words)],
    ]

    voice_table = Table(
        voice_data,
        colWidths=[250, 150]
    )

    voice_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),
        ])
    )

    story.append(voice_table)

    story.append(Spacer(1, 20))

    # =================================================
    # VIDEO ANALYSIS
    # =================================================

    story.append(
        Paragraph(
            "Video Analysis",
            styles["Heading2"]
        )
    )

    video_data = [
        ["Metric", "Score"],

        ["Video Score", f"{video_score}/100"],

        ["Face Presence", f"{face_presence}%"],

        ["Face Position", f"{face_position}%"],

        ["Eye Contact", f"{eye_contact}%"],

        ["Facial Expression", f"{expression}%"],
    ]

    video_table = Table(
        video_data,
        colWidths=[250, 150]
    )

    video_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),
        ])
    )

    story.append(video_table)

    story.append(Spacer(1, 20))

    # =================================================
    # TRANSCRIPT
    # =================================================

    story.append(
        Paragraph(
            "Interview Transcript",
            styles["Heading2"]
        )
    )

    safe_transcript = (
        str(transcript)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            safe_transcript,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # =================================================
    # AI FEEDBACK
    # =================================================

    story.append(
        Paragraph(
            "AI Feedback",
            styles["Heading2"]
        )
    )

    safe_feedback = (
        str(ai_feedback)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            safe_feedback,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # =================================================
    # RECOMMENDATIONS
    # =================================================

    story.append(
        Paragraph(
            "Recommendations",
            styles["Heading2"]
        )
    )

    for item in recommendations:

        safe_item = (
            str(item)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        story.append(
            Paragraph(
                f"• {safe_item}",
                styles["Normal"]
            )
        )

        story.append(Spacer(1, 5))

    # =================================================
    # FOOTER
    # =================================================

    story.append(Spacer(1, 30))

    story.append(
        Paragraph(
            "AI Interview Performance Analyzer",
            styles["Normal"]
        )
    )

    # =================================================
    # BUILD PDF
    # =================================================

    pdf.build(story)


# =====================================================
# OLD REPORT FUNCTION
# =====================================================
# This keeps 5_voice_analysis.py working.
# =====================================================

def generate_report(
    filename,
    candidate_name,
    transcript,
    score,
    strengths,
    weaknesses,
    suggestions,
):

    score_value = str(score)

    if "/" in score_value:

        score_value = score_value.split("/")[0]

    try:
        score_value = int(score_value)

    except:
        score_value = 0

    generate_final_report(

        filename=filename,

        candidate_name=candidate_name,

        final_score=score_value,

        # Voice
        voice_score=score_value,
        confidence=0,
        fluency=0,
        voice_clarity=0,
        speaking_speed=0,
        wpm=0,
        filler_words=0,

        # Video
        video_score=0,
        face_presence=0,
        face_position=0,
        eye_contact=0,
        expression=0,

        # Text
        transcript=transcript,

        ai_feedback=str(strengths),

        recommendations=[
            str(weaknesses),
            str(suggestions),
        ],
    )