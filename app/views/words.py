from sqlalchemy.sql.expression import func
from flask import Blueprint, render_template, request, jsonify, escape
from flask_user import login_required, roles_required, current_user

from app import app, db
from app.models.practice import Definition, WordRole, HrWord, EnWord, format_glossary, PRONOUNS, VERB_TENSES
from app.models.users import WordBank
from app.utils.verbs import Conjugation

