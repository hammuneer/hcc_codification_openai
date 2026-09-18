from hcc_codifier.prompts import SYSTEM_PROMPT


def test_requests_icd10_table_columns():
    assert "ICD-10 Code" in SYSTEM_PROMPT
    assert "ICD-10 Description" in SYSTEM_PROMPT
    assert "Reasoning" in SYSTEM_PROMPT


def test_instructs_not_to_reveal_hcc_codes():
    assert "do not show HCC code" in SYSTEM_PROMPT
