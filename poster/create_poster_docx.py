from __future__ import annotations

import html
import zipfile
from pathlib import Path


OUT = Path(__file__).with_name("harmony_poster_content.docx")

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def p(text: str = "", style: str | None = None, bold: bool = False, italic: bool = False) -> str:
    ppr = f"<w:pPr><w:pStyle w:val=\"{style}\"/></w:pPr>" if style else ""
    rpr = ""
    if bold or italic:
        rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + "</w:rPr>"
    return f"<w:p>{ppr}<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r></w:p>"


def bullet(text: str) -> str:
    return (
        "<w:p><w:pPr><w:pStyle w:val=\"ListParagraph\"/>"
        "<w:numPr><w:ilvl w:val=\"0\"/><w:numId w:val=\"1\"/></w:numPr></w:pPr>"
        f"<w:r><w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r></w:p>"
    )


def caption(text: str) -> str:
    return p(text, "Caption")


def callout(label: str, text: str) -> str:
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"9360\" w:type=\"dxa\"/>"
        "<w:tblInd w:w=\"120\" w:type=\"dxa\"/>"
        "<w:tblBorders><w:top w:val=\"single\" w:sz=\"8\" w:color=\"2E74B5\"/>"
        "<w:left w:val=\"single\" w:sz=\"8\" w:color=\"2E74B5\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"8\" w:color=\"2E74B5\"/>"
        "<w:right w:val=\"single\" w:sz=\"8\" w:color=\"2E74B5\"/>"
        "<w:insideH w:val=\"nil\"/><w:insideV w:val=\"nil\"/></w:tblBorders>"
        "<w:shd w:fill=\"F4F6F9\"/>"
        "<w:tblCellMar><w:top w:w=\"120\" w:type=\"dxa\"/><w:bottom w:w=\"120\" w:type=\"dxa\"/>"
        "<w:start w:w=\"160\" w:type=\"dxa\"/><w:end w:w=\"160\" w:type=\"dxa\"/></w:tblCellMar>"
        "</w:tblPr><w:tblGrid><w:gridCol w:w=\"9360\"/></w:tblGrid><w:tr><w:tc>"
        "<w:tcPr><w:tcW w:w=\"9360\" w:type=\"dxa\"/></w:tcPr>"
        f"{p(label, 'Heading3')}{p(text)}"
        "</w:tc></w:tr></w:tbl>"
    )


def table(headers: list[str], rows: list[list[str]], widths: list[int]) -> str:
    def cell(text: str, width: int, header: bool = False) -> str:
        shade = "<w:shd w:fill=\"F2F4F7\"/>" if header else ""
        style = "TableHeader" if header else "TableText"
        return (
            f"<w:tc><w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/>{shade}</w:tcPr>"
            f"{p(text, style)}"
            "</w:tc>"
        )

    grid = "".join(f"<w:gridCol w:w=\"{w}\"/>" for w in widths)
    border = (
        "<w:tblBorders><w:top w:val=\"single\" w:sz=\"6\" w:color=\"9AA6B2\"/>"
        "<w:left w:val=\"single\" w:sz=\"6\" w:color=\"9AA6B2\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"6\" w:color=\"9AA6B2\"/>"
        "<w:right w:val=\"single\" w:sz=\"6\" w:color=\"9AA6B2\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:color=\"D0D7DE\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:color=\"D0D7DE\"/></w:tblBorders>"
    )
    xml = (
        "<w:tbl><w:tblPr><w:tblW w:w=\"9360\" w:type=\"dxa\"/>"
        "<w:tblInd w:w=\"120\" w:type=\"dxa\"/><w:tblLayout w:type=\"fixed\"/>"
        f"{border}<w:tblCellMar><w:top w:w=\"80\" w:type=\"dxa\"/>"
        "<w:bottom w:w=\"80\" w:type=\"dxa\"/><w:start w:w=\"120\" w:type=\"dxa\"/>"
        "<w:end w:w=\"120\" w:type=\"dxa\"/></w:tblCellMar></w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
    )
    xml += "<w:tr>" + "".join(cell(h, w, True) for h, w in zip(headers, widths)) + "</w:tr>"
    for row in rows:
        xml += "<w:tr>" + "".join(cell(c, w) for c, w in zip(row, widths)) + "</w:tr>"
    return xml + "</w:tbl>"


def document_xml() -> str:
    body: list[str] = []

    body.append(p("An Automatic Four-Part Harmony Grading System", "Title"))
    body.append(p("Integrating Deep Learning-Based Optical Music Recognition and Rule-Based Analysis", "Subtitle"))
    body.append(p("MA, SIAO-SHIH", "Meta"))
    body.append(p("Advisor: Ming-Hsueh Lin", "Meta"))
    body.append(p("Arete Honors Program", "Meta"))
    body.append(p("National Yang Ming Chiao Tung University", "Meta"))

    body.append(p("01 Background and Problem", "Heading1"))
    body.append(p("Four-part harmony is a fundamental component of music theory education. Students must simultaneously consider voice leading, chord spacing, doubling, leading-tone resolution, and cadence structure. Traditional grading depends heavily on expert teachers and often requires substantial time for manual correction."))
    body.append(p("Although Optical Music Recognition (OMR) systems can recognize notation from score images, most existing systems focus on symbol detection or transcription rather than harmony-specific analysis and explainable learning feedback."))
    body.append(callout("Key Question", "How can a system convert a score image into localized and explainable four-part harmony feedback for student learning?"))

    body.append(p("02 Objectives and Contributions", "Heading1"))
    body.append(p("This study aims to design an automatic four-part harmony grading system that integrates deep learning-based Optical Music Recognition with rule-based harmony analysis."))
    body.append(p("Objectives", "Heading2"))
    for item in [
        "Detect music notation symbols from score images using a YOLO-based OMR model.",
        "Convert detected symbols into structured four-part harmony snapshots.",
        "Analyze common harmony errors through a rule-based engine.",
        "Present localized errors with rule explanations and correction suggestions.",
    ]:
        body.append(bullet(item))
    body.append(p("Contributions", "Heading2"))
    for item in [
        "A system architecture connecting score recognition and harmony rule analysis.",
        "A structured representation for four-part harmony snapshots.",
        "A rule-based engine for representative voice-leading and chord-configuration errors.",
        "A web-based prototype demonstrating the grading workflow.",
    ]:
        body.append(bullet(item))

    body.append(p("03 System Method", "Heading1"))
    body.append(table(
        ["Layer", "Process"],
        [
            ["Input", "Score Image"],
            ["Deep Learning-Based OMR", "Image Preprocessing -> YOLO Symbol Detection -> Symbol-to-Voice Assembly"],
            ["Rule-Based Analysis", "ChordSnapshot Representation -> Harmony Rule Engine -> Localized Feedback"],
        ],
        [2600, 6760],
    ))
    body.append(caption("Figure 1: Overall workflow of the proposed four-part harmony grading system."))
    body.append(p("The proposed system consists of five major stages: score image input, OMR symbol detection, symbol-to-voice assembly, rule-based harmony analysis, and feedback visualization. The architecture separates visual recognition from musical reasoning, allowing the OMR model and the harmony rule engine to be improved independently."))

    body.append(p("04 OMR Model Performance", "Heading1"))
    body.append(p("The current best OMR model is based on YOLO12s Ultimate v5 Stable and is evaluated on a cleaned validation set."))
    body.append(table(
        ["Metric", "Result"],
        [["mAP50", "0.7763"], ["mAP50-95", "0.7320"], ["Precision", "0.957"], ["Recall", "0.576"]],
        [4680, 4680],
    ))
    body.append(caption("Table 1: OMR detection performance under the deployment protocol."))
    body.append(p("Observation: High precision indicates reliable detections, while recall improvement remains the main training target, especially for small or rare notation symbols."))

    body.append(p("05 Rule-Based Harmony Analysis", "Heading1"))
    body.append(p("The rule engine receives a sequence of chord snapshots. Each snapshot contains the pitch, measure, beat, and voice assignment of Soprano, Alto, Tenor, and Bass parts."))
    body.append(table(
        ["ID", "Rule Type", "Description"],
        [
            ["M1", "Melodic leap", "Detects excessive or unstable melodic intervals."],
            ["V1", "Voice crossing / overlap", "Checks invalid voice order between adjacent parts."],
            ["P1", "Parallel fifths / octaves", "Detects parallel perfect intervals between voices."],
            ["P2", "Hidden fifths / octaves", "Checks direct motion into perfect intervals."],
            ["D1", "Doubling / omission", "Verifies triad members and leading-tone treatment."],
            ["L1", "Leading-tone resolution", "Checks resolution from leading tone to tonic."],
        ],
        [900, 2700, 5760],
    ))
    body.append(caption("Table 2: Representative harmony rules implemented in the rule engine."))
    body.append(p("Each detected issue is mapped to a rule identifier, a severity level, involved voices, score location, explanation, and correction suggestion."))

    body.append(p("06 Prototype Demonstration", "Heading1"))
    body.append(p("Main prototype screen: OMR recognition result with localized harmony errors."))
    body.append(p("Supporting screens: score image input and rule explanation detail."))
    body.append(p("The web-based prototype demonstrates the complete user-facing workflow: score input, recognition progress, error localization, rule explanation, and correction guidance."))

    body.append(p("07 Discussion and Limitations", "Heading1"))
    body.append(p("Current strengths", "Heading2"))
    for item in [
        "The OMR model achieves promising detection precision for music symbols.",
        "The rule engine provides explainable analysis rather than only binary grading.",
        "The prototype interface makes error locations and rule explanations visible to learners.",
        "The modular design allows the OMR model and rule engine to be improved independently.",
    ]:
        body.append(bullet(item))
    body.append(p("Current limitations", "Heading2"))
    for item in [
        "Recall remains the main bottleneck of the OMR model.",
        "Symbol-to-voice assembly requires further improvement for arbitrary handwritten scores.",
        "The current rule set focuses on representative four-part harmony errors.",
        "More advanced harmony phenomena require future rule expansion.",
    ]:
        body.append(bullet(item))

    body.append(p("08 Conclusion and Future Work", "Heading1"))
    body.append(p("This study presents an automatic four-part harmony grading system that integrates deep learning-based OMR and rule-based harmony analysis. The system detects music symbols from score images, converts them into structured harmony representations, and provides localized, explainable feedback for common four-part harmony errors."))
    body.append(p("Future work", "Heading2"))
    for item in [
        "Improve recall for small and rare notation symbols.",
        "Strengthen the conversion from OMR detections to four-voice structure.",
        "Expand the rule set to include non-chord tones and cadence-specific cases.",
        "Deploy the system to a mobile application for real-time classroom use.",
    ]:
        body.append(bullet(item))
    body.append(callout("Key Takeaway", "The system does not search for a single correct answer; it detects violations of harmony rules and provides explainable learning feedback."))

    body.append(p("References", "Heading1"))
    for item in [
        "YOLO / object detection reference.",
        "Optical Music Recognition survey.",
        "Four-part harmony or music theory reference.",
        "Rule-based analysis or explainable feedback reference.",
    ]:
        body.append(bullet(item))

    sect = (
        "<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/>"
        "<w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" "
        "w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr>"
    )
    return (
        f"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        f"<w:document xmlns:w=\"{W_NS}\" xmlns:r=\"{R_NS}\"><w:body>"
        + "".join(body)
        + sect
        + "</w:body></w:document>"
    )


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>
"""

STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W_NS}">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="80"/></w:pPr><w:rPr><w:b/><w:sz w:val="36"/><w:color w:val="0B2545"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="120"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="1F4D78"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Meta"><w:name w:val="Meta"/><w:pPr><w:jc w:val="center"/><w:spacing w:after="30"/></w:pPr><w:rPr><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="320" w:after="160"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/><w:color w:val="2E74B5"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/><w:color w:val="2E74B5"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/><w:color w:val="1F4D78"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="Caption"/><w:pPr><w:spacing w:before="80" w:after="80"/></w:pPr><w:rPr><w:i/><w:sz w:val="20"/><w:color w:val="555555"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="160" w:line="280" w:lineRule="auto"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="0" w:line="264" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableHeader"><w:name w:val="Table Header"/><w:basedOn w:val="TableText"/><w:rPr><w:b/><w:sz w:val="20"/></w:rPr></w:style>
</w:styles>
"""

NUMBERING = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{W_NS}">
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="•"/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
</w:numbering>
"""

CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Harmony Poster Content</dc:title>
  <dc:creator>Codex</dc:creator>
</cp:coreProperties>
"""

APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>
"""


def main() -> None:
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("word/document.xml", document_xml())
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", NUMBERING)
        z.writestr("docProps/core.xml", CORE)
        z.writestr("docProps/app.xml", APP)
    print(OUT)


if __name__ == "__main__":
    main()
