from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("plan", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey(
            "accounts.id"), nullable=False),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "vendors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey(
            "accounts.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("tax_id", sa.String(), nullable=True),
        sa.Column("address_jsonb", postgresql.JSONB(), nullable=True),
    )

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey(
            "accounts.id"), nullable=False),
        sa.Column("vendor_id", sa.Integer(), sa.ForeignKey(
            "vendors.id"), nullable=True),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("confidence", sa.Numeric(), nullable=True),
        sa.Column("totals_jsonb", postgresql.JSONB(), nullable=True),
        sa.Column("extracted_jsonb", postgresql.JSONB(), nullable=True),
        sa.Column("original_file_url", sa.Text(), nullable=False),
        sa.Column("reviewer_id", sa.Integer(),
                  sa.ForeignKey("users.id"), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("exported_system", sa.String(), nullable=True),
        sa.Column("exported_id", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "invoice_line_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("invoice_id", sa.Integer(), sa.ForeignKey(
            "invoices.id"), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("quantity", sa.Numeric(), nullable=True),
        sa.Column("unit_price", sa.Numeric(), nullable=True),
        sa.Column("line_total", sa.Numeric(), nullable=True),
        sa.Column("meta_jsonb", postgresql.JSONB(), nullable=True),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("account_id", sa.Integer(), sa.ForeignKey(
            "accounts.id"), nullable=False),
        sa.Column("actor_id", sa.Integer(),
                  sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("delta_jsonb", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("invoice_line_items")
    op.drop_table("invoices")
    op.drop_table("vendors")
    op.drop_table("users")
    op.drop_table("accounts")

