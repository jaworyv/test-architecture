from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_credit_transaction_by_id(db: Session, creditId: int) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=creditId).first()

    @staticmethod
    def get_transaction_by_accounts(db: Session, from_account_id: int, to_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id, to_account_id=to_account_id).first()

    @staticmethod
    def get_transaction_by_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id).first()