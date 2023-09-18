"""creating Flows Table

Revision ID: cbfc86116172
Revises: 
Create Date: 2023-08-24 21:41:33.309723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbfc86116172'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'flows',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('flow_id', sa.String(255), nullable=False),
        sa.Column('srcip', sa.String(255), nullable=False),
        sa.Column('sport', sa.Integer, nullable=False),
        sa.Column('dstip', sa.String(255), nullable=False),
        sa.Column('dsport', sa.Integer, nullable=False),
        sa.Column('proto', sa.String(255), nullable=False),
        sa.Column('state', sa.String(255), nullable=False),
        sa.Column('dur', sa.Float, nullable=False),
        sa.Column('sbytes', sa.Integer, nullable=False),
        sa.Column('dbytes', sa.Integer, nullable=False),
        sa.Column('sttl', sa.Integer, nullable=False),
        sa.Column('dttl', sa.Integer, nullable=False),
        sa.Column('sloss', sa.Integer, nullable=False),
        sa.Column('dloss', sa.Integer, nullable=False),
        sa.Column('service', sa.String(255), nullable=False),
        sa.Column('sload', sa.Float, nullable=False),
        sa.Column('dload', sa.Float, nullable=False),
        sa.Column('Spkts', sa.Integer, nullable=False),
        sa.Column('Dpkts', sa.Integer, nullable=False),
        sa.Column('stcpb', sa.Integer, nullable=False),
        sa.Column('dtcpb', sa.Integer, nullable=False),
        sa.Column('smean', sa.Integer, nullable=False),
        sa.Column('dmean', sa.Integer, nullable=False),
        sa.Column('trans_depth', sa.Integer, nullable=False),
        sa.Column('sjit', sa.Float, nullable=False),
        sa.Column('djit', sa.Float, nullable=False),
        sa.Column('Stime', sa.Float, nullable=False),
        sa.Column('Ltime', sa.Float, nullable=False),
        sa.Column('Sintpkt', sa.Float, nullable=False),
        sa.Column('Dintpkt', sa.Float, nullable=False),
        sa.Column('tcprtt', sa.Float, nullable=False),
        sa.Column('synack', sa.Float, nullable=False),
        sa.Column('ackdat', sa.Float, nullable=False),
        sa.Column('ct_state_ttl', sa.Integer, nullable=False),
        sa.Column('ct_flw_http_mthd', sa.Integer, nullable=False),
        sa.Column('ct_src_ltm', sa.Integer, nullable=False),
        sa.Column('ct_srv_dst', sa.Integer, nullable=False),
        sa.Column('ct_dst_ltm', sa.Integer, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('flows')


