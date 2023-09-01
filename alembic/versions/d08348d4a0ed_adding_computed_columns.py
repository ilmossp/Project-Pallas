"""adding computed columns

Revision ID: d08348d4a0ed
Revises: cbfc86116172
Create Date: 2023-08-29 17:07:01.166011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = 'd08348d4a0ed'
down_revision: Union[str, None] = 'cbfc86116172'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "flows"
generated_column_name = "ct_state_ttl"

def upgrade() -> None:
    trigger_function = """
    CREATE OR REPLACE FUNCTION update_generated_column()
    RETURNS TRIGGER AS $$
    BEGIN
        DECLARE
            v_state text;
            v_service text;
            v_src text;
            v_dst text;
            v_ct_state_sttl integer;
            v_ct_src_ltm integer;
            v_ct_srv_dst integer;
            v_ct_dst_ltm integer;
        BEGIN
            v_state := NEW.state;
            Select count(*) into v_count from flows where 
            state = v_state and sttl Between 250 and 255 and dttl between 250 and 255 and created_at < NEW.created_at
            Order by created_at desc limit 100;
            NEW.ct_state_ttl = v_ct_state_sttl;
            v_service := NEW.service;
            if v_service = 'http' then
                Select count(*) into v_count from flows where
                service = v_service and created_at < NEW.created_at 
                Order by created_at desc limit 100;
                NEW.ct_flw_http_mthd = v_count;
            end if;
            v_src := NEW.srcip;
            Select count(*) into v_ct_src_ltm from flows where
            srcip = v_src and created_at < NEW.created_at
            Order by created_at desc limit 100;
            NEW.ct_src_ltm = v_ct_src_ltm;
            v_dst := NEW.dstip;
            v_service := NEW.service;
            Select count(*) into v_ct_srv_dst from flows where
            dstip = v_dst and service=v_service and created_at < NEW.created_at
            Order by created_at desc limit 100;
            NEW.ct_srv_dst = v_ct_srv_dst;
            Select count(*) into v_ct_dst_ltm from flows where
            dstip = v_dst and created_at < NEW.created_at
            Order by created_at desc limit 100;
            NEW.ct_dst_ltm = v_ct_dst_ltm;
            RETURN NEW;
        END;
    END;
    $$ LANGUAGE plpgsql;
    """

    op.execute(text(trigger_function))

    trigger = """
    CREATE TRIGGER update_generated_column_trigger
    BEFORE INSERT OR UPDATE ON flows
    FOR EACH ROW
    EXECUTE FUNCTION update_generated_column();
    """
    op.execute(text(trigger))


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS update_generated_column_trigger ON {}".format(table_name))
    op.execute("DROP FUNCTION IF EXISTS update_generated_column()")
