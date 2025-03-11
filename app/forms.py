from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, SelectField, DecimalField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class AddressForm(FlaskForm):
    address_type = SelectField('Address Type', choices=[('Shipping', 'Shipping'), ('Billing', 'Billing')], validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State')
    postal_code = StringField('Postal Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    addresses = FieldList(FormField(AddressForm), min_entries=1)  # Adjust `min_entries` as needed
    submit = SubmitField('Save Changes')

class RegistrationForm(FlaskForm):
    title = SelectField('Title', choices=[('', 'Select your title'), ('Ms/Mrs', 'Ms/Mrs'), ('Mr', 'Mr')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    email_confirmation = StringField('Confirm Email', validators=[DataRequired(), Email(), EqualTo('email', message="Emails must match")])

    # Separate day, month, year fields
    day = IntegerField('Day', validators=[DataRequired(), NumberRange(min=1, max=31, message="Invalid day")])
    month = SelectField('Month', choices=[
        ('', 'Month'), ('1', 'January'), ('2', 'February'), ('3', 'March'), 
        ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), 
        ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
    ], validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1900, max=2023, message="Invalid year")])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match")])


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    SKU = StringField('SKU', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Save Product')

class AddressForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State')
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Save Address')

class DiscountForm(FlaskForm):
    code = StringField('Discount Code', validators=[DataRequired()])
    discount_type = SelectField('Discount Type', choices=[('Percentage', 'Percentage'), ('Flat', 'Flat Amount')], validators=[DataRequired()])
    percentage = DecimalField('Percentage', places=2, validators=[NumberRange(min=0, max=100)])
    flat_amount = DecimalField('Flat Amount', places=2, validators=[NumberRange(min=0)])
    submit = SubmitField('Apply Discount')

#SubscriptionForm
class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')