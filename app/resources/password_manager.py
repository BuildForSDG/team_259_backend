import base64
import smtplib
from datetime import timedelta, datetime
from email.mime.text import MIMEText

import uuid
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from flask import request, abort, render_template
from flask_mail import Mail, Message

from models.user_model import User, UserSchema
from models.change_password_model import ChangePasswordToken, ChangePasswordTokenSchema
from models.user_role_model import UserRole, UserRoleSchema
from models.sessions_model import Session
from user_functions.token_generator import TokenGenerator
from user_functions.user_role_manager import UserPrivilege
from user_functions.platform_fetcher import compute_platform_version


mail = Mail()

api = Namespace('password', description='Change User Password')

password_token_schema = ChangePasswordTokenSchema()
password_tokens_schema = ChangePasswordTokenSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_role_schema = UserRoleSchema()

reset_token_model = api.model('PasswordResetToken', {
    'email': fields.String(required=True, description='Email registered under one of the accounts')
})

change_password_model = api.model('ChangePassword', {
    'password': fields.String(required=True, description='New Password')
})


@api.route('/forgot')
class SendResetLink(Resource):
    @api.doc('create_reset_link')
    @api.expect(reset_token_model)
    def post(self):
        '''Send email with password reset link'''
        data = api.payload

        if not data:
            abort(400, 'No input data detected')

        email = data['email'].lower()
        db_user = User.query.filter_by(email=email).first()
        user_to_check = user_schema.dump(db_user)
        if len( user_to_check) == 0:
            abort(400, 'Failed! Please use the email used to register your account')

        password_reset = TokenGenerator()
        reset_code =password_reset.token_code
        reset_token = password_reset.url_token

        user_id = db_user.id
        password_reset_record = ChangePasswordToken(user_id=user_id, email=email, reset_code=reset_code)
        password_reset_record.insert_record()
        print(reset_token)

        # Add a html to send along with the email containing a button that redirects to the password reset page
        template = render_template('password_reset.html', reset_token=reset_token)
        subject = "Password Reset"
        msg = Message('Hello', recipients=[email])#, sender = 'keithgatana@gmail.com')
        msg.body = 'We have noticed you have requested for a password change. Please click on the link belowZipFile The class for reading and writing ZIP files.  See section '
        msg.html = template

        try:
            mail.send(msg)
            return {'message':'Success', 'reset_token':reset_token}, 200
        except Exception as e:
            print('description: ', e)
            return {'message': 'Couldn\'t send mail'}, 400

@api.route('/token/validity/<string:reset_token>')
class CheckTokenValidity(Resource):
    @api.doc('check_reset_password_token_validity')
    def get(self, reset_token):
        '''Verify Password Reset Token'''
        received_reset_token = reset_token
        TokenGenerator.decode_token(received_reset_token)
        token = TokenGenerator.token

        # Check for an existing reset_token with is_expired status as False
        reset_code_record = ChangePasswordToken.fetch_by_reset_code(reset_code=token)
        if not reset_code_record:
            abort(400, 'Rejected! This reset token does not exist')

        set_to_expire = reset_code_record.created + timedelta(minutes=30)
        current_time = datetime.utcnow()
        if set_to_expire <= current_time:
            user_id = reset_code_record.user_id
            is_expired = True
            user_records = ChangePasswordToken.fetch_all_by_user_id(user_id)
            record_ids = []
            for record in user_records:
                record_ids.append(record.id)
            for record_id in record_ids:
                ChangePasswordToken.expire_token(id=record_id, is_expired=is_expired)
            abort(400, 'Rejected! Password reset token is expired. Please request a new password reset.')

        if reset_code_record.is_expired == True:
            user_id = reset_code_record.user_id
            is_expired = True
            user_records = ChangePasswordToken.fetch_all_by_user_id(user_id)
            record_ids = []
            for record in user_records:
                record_ids.append(record.id)
            for record_id in record_ids:
                ChangePasswordToken.expire_token(id=record_id, is_expired=is_expired)
            abort(400, 'Rejected! Password reset token has already been used. Please request a new password reset.')
        return {'message': 'Password reset token is active. You may type in your new password.'}, 200

@api.route('/reset/<string:reset_token>')
class ResetPassword(Resource):
    @api.doc('reset_password')
    @api.expect(change_password_model)
    def put(self, reset_token):
        '''Reset User Password'''
        # Get User-agent and ip address, then compute operating system
        my_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
        if my_ip is None:
            ip = my_ip
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
        user_agent = str(request.user_agent)
        user_agent_platform = request.user_agent.platform
        device_os = compute_platform_version(user_agent, user_agent_platform)
        if device_os is None or ip is None:
            abort(400, 'This request has been rejected. Please use a recognised device')

        received_reset_token = reset_token
        TokenGenerator.decode_token(received_reset_token)
        token = TokenGenerator.token

        # Check for an existing reset_token with is_expired status as False
        reset_code_record = ChangePasswordToken.fetch_by_reset_code(reset_code=token)
        if not reset_code_record:
            abort(400, 'This reset token does not exist')
        
        if reset_code_record.is_expired == True:
            user_id = reset_code_record.user_id
            is_expired = True
            user_records = ChangePasswordToken.fetch_all_by_user_id(user_id)
            record_ids = []
            for record in record_ids:
                record_ids.append(record.id)
            for record_id in record_ids:
                ChangePasswordToken.expire_token(id=record_id, is_expired=is_expired)
            abort(400, 'Password reset token has already been used. Please request a new password reset.')

        user_id = reset_code_record.user_id
        is_expired = True
        user_records = ChangePasswordToken.fetch_all_by_user_id(user_id)
        record_ids = []
        for record in user_records:
            record_ids.append(record.id)
        for record_id in record_ids:
            ChangePasswordToken.expire_token(id=record_id, is_expired=is_expired)

        data = api.payload

        if not data:
            abort(400, 'No input data detected')

        password = data['password']
        hashed_password = generate_password_hash(data['password'], method='sha256')
        User.update_password(id=user_id, password=hashed_password)
        this_user = User.fetch_by_id(id=user_id)
        user = user_schema.dump(this_user)

        user_id = this_user.id

        user_role = UserRole.fetch_by_user_id(user_id)
        privileges = user_role.role.role
        # Create access token
        expiry_time = timedelta(minutes=30)
        my_identity = {'id':this_user.id, 'privileges':privileges}
        access_token = create_access_token(identity=my_identity, expires_delta=expiry_time)
        refresh_token = create_refresh_token(my_identity)
        # Save session info to db
        new_session_record = Session(user_ip_address=ip, device_operating_system=device_os, user_id=user_id, token=access_token)    
        new_session_record.insert_record()
        status = {'message': 'Successfully changed Password', 'access token': access_token, 'refresh token': refresh_token, 'user': user}
        return status, 200
