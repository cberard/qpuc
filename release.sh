#!/bin/bash
cd qpuc_app/ \
&& export PYTHONPATH=../ \
&& alembic revision --autogenerate \
&& alembic upgrade head  
