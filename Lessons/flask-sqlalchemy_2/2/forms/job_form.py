from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class JobForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Duration', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Finished')
    submit = SubmitField('Submit')
