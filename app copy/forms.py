from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, SelectField, DecimalField, TextAreaField, NumberRange
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Register')

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
