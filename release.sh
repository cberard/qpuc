#!/bin/bash
cd qpuc_app/ \
&& alembic revision --autogenerate \
&& alembic upgrade head  
