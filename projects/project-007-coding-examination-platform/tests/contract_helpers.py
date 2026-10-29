"""Shared test fixture: a valid ECC v1.0 capability set (spec §8 example)."""
LAB_CAPABILITIES = {
    "compiler": "ALLOW", "debugger": "ALLOW", "visible_tests": "ALLOW",
    "terminal": {"value": "LIMITED", "allowlist": ["python", "pytest"]},
    "documentation": {"value": "ALLOWLIST", "sources": ["python-stdlib-docs"]},
    "internet": "DENY", "clipboard": "INTERNAL_ONLY",
    "ai_assistance": "DENY", "external_ide": "DENY",
}


def save_lab_contract(database, examination_id: str, owner_user_id: str):
    """Live tests: store a draft ECC so DRAFT -> SCHEDULED can bind it (spec §5.2)."""
    from app.persistence.mysql_contract_repository import MySQLContractRepository
    from app.persistence.mysql_examination_repository import MySQLExaminationRepository
    from app.services.contract_service import ContractDeclaration, ContractService

    service = ContractService(MySQLContractRepository(database), MySQLExaminationRepository(database), None)
    return service.save_draft(examination_id, owner_user_id, ContractDeclaration(dict(LAB_CAPABILITIES)))
