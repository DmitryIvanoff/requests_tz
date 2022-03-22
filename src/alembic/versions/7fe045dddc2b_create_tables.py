"""create_tables

Revision ID: 7fe045dddc2b
Revises: 
Create Date: 2022-03-20 15:55:17.184368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7fe045dddc2b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "requests",
        sa.Column("key", sa.Text(), nullable=False),
        sa.Column("body", sa.JSON(), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("key"),
    )
    op.create_index(op.f("ix_requests_key"), "requests", ["key"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_requests_key"), table_name="requests")
    op.drop_table("requests")
    # ### end Alembic commands ###
