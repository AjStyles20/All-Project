import io
import zipfile

import pytest
from fastapi.testclient import TestClient

from p011.analysis import analyse
from p011.app import create_app
from p011.evaluation import DEV, report
from p011.feedback import evaluate
from p011.ingest import IngestError, extract, sentences
from p011.reviewers import ROLES, plan

REPORT = """Our attendance app is the first system of its kind for teachers.

In testing, accuracy was 91%. We used a dataset of 400 photos from two schools.

The final accuracy was 85% on the same data. However, it was only tested with 8 teachers.

The app must work offline. Student data and passwords are stored on the server."""


def docx(paragraphs, extra=b""):
    body = "".join(f'<w:p><w:r><w:t>{p}</w:t></w:r></w:p>' for p in paragraphs)
    xml = ('<?xml version="1.0"?>' + extra.decode() +
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           + body + '</w:body></w:document>').encode()
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        z.writestr("word/document.xml", xml)
    return out.getvalue()


def pptx(slides):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for i, text in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml",
                       '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                       f'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>{text}</a:t></p:sld>')
    return out.getvalue()


# ---------- ingestion ----------

def test_text_docx_pptx_keep_their_location():
    assert extract("r.md", REPORT.encode())[1].locator == "paragraph 2"
    pieces = extract("r.docx", docx(["Intro.", "We used a survey."]))
    assert [p.locator for p in pieces] == ["paragraph 1", "paragraph 2"]
    slides = extract("s.pptx", pptx(["Title", "Results: 91%", "Thanks"]))
    assert slides[1].locator == "slide 2" and "91%" in slides[1].text


def test_hostile_files_are_refused():
    with pytest.raises(IngestError):
        extract("x.exe", b"MZ")
    with pytest.raises(IngestError):
        extract("big.txt", b"x" * (10 * 1024 * 1024 + 1))
    with pytest.raises(IngestError):
        extract("bad.docx", b"not a zip")
    with pytest.raises(IngestError, match="document type"):
        extract("xxe.docx", docx(["hi"], b'<!DOCTYPE d [<!ENTITY x SYSTEM "file:///etc/passwd">]>'))
    bomb = io.BytesIO()
    with zipfile.ZipFile(bomb, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("word/document.xml", b"0" * (60 * 1024 * 1024))
    with pytest.raises(IngestError, match="expands"):
        extract("bomb.docx", bomb.getvalue())


def test_pdf_is_read_with_page_numbers():
    pypdf = pytest.importorskip("pypdf")
    writer = pypdf.PdfWriter()
    writer.add_blank_page(100, 100)
    out = io.BytesIO()
    writer.write(out)
    assert extract("blank.pdf", out.getvalue()) == []      # no text, no crash
    with pytest.raises(IngestError):
        extract("broken.pdf", b"%PDF-1.4 garbage")


def test_sentence_split():
    assert sentences("It works. It is fast! Is it? 3 users agreed.") == ["It works.", "It is fast!", "Is it?", "3 users agreed."]


# ---------- analysis and questions ----------

def chunks():
    return [(f"c{i}", p.text) for i, p in enumerate(extract("r.md", REPORT.encode()))]


def test_findings_point_at_real_sentences():
    found = analyse(chunks())
    kinds = {f.kind for f in found}
    assert {"UNSUPPORTED_CLAIM", "CONTRADICTION", "LIMITATION", "REQUIREMENT", "METHOD", "SECURITY"} <= kinds
    texts = dict(chunks())
    assert all(f.sentence in texts[f.chunk_id] for f in found)
    contradiction = next(f for f in found if f.kind == "CONTRADICTION")
    assert "91" in contradiction.detail and "85" in contradiction.detail and contradiction.other_chunk_id


def test_claims_with_evidence_are_not_called_unsupported():
    found = analyse([("c1", "Our method outperforms the baseline (Table 2), with p < 0.05.")])
    assert [f.kind for f in found if "CLAIM" in f.kind] == ["QUANTIFIED_CLAIM"]


def test_questions_are_grounded_and_roles_differ():
    qs = plan(list(ROLES), analyse(chunks()), per_role=2)
    texts = dict(chunks())
    for q in qs:
        if q.grounded:
            assert q.quote in q.text and any(q.quote in texts[c] for c in q.chunk_ids)
    # Nothing is asked twice: a later reviewer moves on to what earlier ones did not cover.
    assert len({(q.quote, q.category) for q in qs if q.grounded}) == sum(q.grounded for q in qs)
    alone = {r: plan([r], analyse(chunks()), per_role=1)[0].category for r in ROLES}
    assert alone == {"technical": "REQUIREMENT", "methodology": "METHOD", "skeptic": "UNSUPPORTED_CLAIM",
                     "security": "SECURITY"}


def test_general_questions_are_marked_not_grounded():
    qs = plan(["technical"], [], per_role=3)
    assert qs and all(not q.grounded and q.category == "GENERAL" for q in qs)


def test_evaluation_reports_are_reproducible():
    assert report(5, DEV) == report(5, DEV)


# ---------- feedback ----------

def test_feedback_has_criteria_and_basis_but_no_score():
    q = next(q for q in plan(["skeptic"], analyse(chunks())) if q.category == "CONTRADICTION")
    sources = [dict(chunks())[c] for c in q.chunk_ids]
    items = evaluate("It is always 99% accurate.", q, sources)
    by = {i.criterion: i for i in items}
    assert by["consistency"].basis == "source" and "99" in by["consistency"].observation
    assert "unsupported statements" in by and "uncertainty" in by
    assert not any("score" in i.criterion for i in items)
    good = evaluate("The 91% was on the first test set; the final 85% used all data, so 85% is the figure we stand by, "
                    "and we only tested with 8 teachers.", q, sources)
    assert not any(i.criterion == "consistency" for i in good)


# ---------- app ----------

def client(tmp_path):
    return TestClient(create_app(tmp_path / "d.sqlite3", "tok"), base_url="http://127.0.0.1"), {"X-Token": "tok"}


def test_app_requires_token_and_local_host(tmp_path):
    c, h = client(tmp_path)
    assert c.get("/api/documents").status_code == 401
    other = TestClient(create_app(tmp_path / "e.sqlite3", "tok"), base_url="http://evil.example")
    assert other.get("/api/documents", headers=h).status_code == 403


def test_full_flow(tmp_path):
    c, h = client(tmp_path)
    up = c.post("/api/documents", params={"name": "report.docx"}, headers=h,
                content=docx(REPORT.split("\n\n")))
    assert up.status_code == 201 and up.json()["chunks"] == 4
    findings = c.get("/api/findings", headers=h).json()
    assert any(f["kind"] == "CONTRADICTION" and "report.docx" in f["where"] for f in findings)
    assert c.get("/api/search", params={"q": "accuracy"}, headers=h).json()[0]["document"] == "report.docx"
    sid = c.post("/api/sessions", headers=h, json={"roles": ["skeptic", "security"]}).json()["id"]
    session = c.get(f"/api/sessions/{sid}", headers=h).json()
    q = session["questions"][0]
    assert q["grounded"] and q["evidence"][0]["text"]
    fb = c.post(f"/api/questions/{q['id']}/answer", headers=h, json={"text": "Our tests show it."}).json()["feedback"]
    assert fb and all({"criterion", "observation", "basis"} <= set(i) for i in fb)
    again = c.get(f"/api/sessions/{sid}", headers=h).json()["questions"][0]
    assert again["answer"] == "Our tests show it."


def test_upload_validation_and_delete(tmp_path):
    c, h = client(tmp_path)
    assert c.post("/api/documents", params={"name": "x.exe"}, headers=h, content=b"MZ").status_code == 400
    assert c.post("/api/documents", params={"name": "empty.txt"}, headers=h, content=b"   ").status_code == 400
    doc = c.post("/api/documents", params={"name": "r.txt"}, headers=h, content=REPORT.encode()).json()["id"]
    assert c.delete(f"/api/documents/{doc}", headers=h).status_code == 200
    assert c.get("/api/search", params={"q": "accuracy"}, headers=h).json() == []
    assert c.post("/api/sessions", headers=h, json={"roles": ["nobody"]}).status_code == 400
