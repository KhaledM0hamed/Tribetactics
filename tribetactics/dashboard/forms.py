from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from tribetactics.models import Restaurant

class RestaurantForm(FlaskForm):
    name = StringField('name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Create Restaurant')

    def validate_name(self, name):
        restaurant = Restaurant.query.filter_by(name=name.data).first()
        if restaurant:
            raise ValidationError('That name is taken. Please choose another one')


class ItemForm(FlaskForm):
    name = StringField('name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    price = IntegerField('price',
                        validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        restaurant = Restaurant.query.filter_by(name=name.data).first()
        if restaurant:
            raise ValidationError('That name is taken. Please choose another one')

