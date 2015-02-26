"""empty message

Revision ID: 4540de37bc03
Revises: None
Create Date: 2014-12-14 15:22:54.618535

"""

# revision identifiers, used by Alembic.
revision = '4540de37bc03'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.String(length=128), server_default='3fd854071e8e', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('key', sa.String(length=128), nullable=True),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_category_created_time'), ['created_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_category_key'), ['key'], unique=False)

    op.create_table('worker',
    sa.Column('id', sa.String(length=128), autoincrement=False, nullable=False),
    sa.Column('uid', sa.String(length=128), nullable=False),
    sa.Column('user_name', sa.String(length=128), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=True),
    sa.Column('profile_picture', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=True, server_default='prepare'),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_worker_created_time'), ['created_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_updated_time'), ['updated_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_user_name'), ['user_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_status'), ['status'], unique=False)
        batch_op.create_index(batch_op.f('ix_worker_uid'), ['uid'], unique=False)

    op.create_table('worker_category',
    sa.Column('worker_id', sa.String(length=128), nullable=False),
    sa.Column('category_id', sa.String(length=128), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('worker_id', 'category_id')
    )
    with op.batch_alter_table('worker_category', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_worker_category_created_time'), ['created_time'], unique=False)

    op.create_table('media',
    sa.Column('id', sa.String(length=128), autoincrement=False, nullable=False),
    sa.Column('worker_id', sa.String(length=128), nullable=False),
    sa.Column('low_resolution', sa.String(length=256), nullable=False),
    sa.Column('thumbnail', sa.String(length=256), nullable=False),
    sa.Column('standard_resolution', sa.String(length=256), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_media_created_time'), ['created_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_media_worker_id'), ['worker_id'], unique=False)

    op.create_table('admin',
    sa.Column('id', sa.String(length=128), server_default='3fd854071e8e', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('mobile', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_admin_created_time'), ['created_time'], unique=False)
        batch_op.create_index('ix_admin_email_password', ['email', 'password'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.String(length=128), server_default='3fd854071e8e', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('avatar', sa.String(length=255), nullable=False),
    sa.Column('access_token', sa.String(length=255), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_created_time'), ['created_time'], unique=False)

    op.create_table('site_setting',
    sa.Column('id', sa.String(length=128), server_default='3fd854071e8e', autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('slogan', sa.String(length=255), nullable=False),
    sa.Column('keyword', sa.String(length=255), nullable=False),
    sa.Column('created_time', sa.DateTime(timezone=True), server_default=sa.text(u'CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('site_setting', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_site_setting_created_time'), ['created_time'], unique=False)

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('site_setting', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_site_setting_created_time'))

    op.drop_table('site_setting')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_created_time'))

    op.drop_table('user')
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.drop_index('ix_admin_email_password')
        batch_op.drop_index(batch_op.f('ix_admin_created_time'))

    op.drop_table('admin')
    with op.batch_alter_table('media', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_media_worker_id'))
        batch_op.drop_index(batch_op.f('ix_media_created_time'))

    op.drop_table('media')
    with op.batch_alter_table('worker_category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_worker_category_created_time'))

    op.drop_table('worker_category')
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_worker_uid'))
        batch_op.drop_index(batch_op.f('ix_worker_status'))
        batch_op.drop_index(batch_op.f('ix_worker_user_name'))
        batch_op.drop_index(batch_op.f('ix_worker_updated_time'))
        batch_op.drop_index(batch_op.f('ix_worker_created_time'))

    op.drop_table('worker')
    with op.batch_alter_table('category', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_category_key'))
        batch_op.drop_index(batch_op.f('ix_category_created_time'))

    op.drop_table('category')
    ### end Alembic commands ###
