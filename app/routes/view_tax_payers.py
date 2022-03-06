from app.utils import access_token_required, get_filter_parser, admin_or_accountant_token_required
from app.models import TaxPayer, User
from app import bcrypt, db
from flask_restx import Resource, Namespace, marshal
from app.schemas import date_created_payers_schema,state_of_tax_payers_schema,date_modified_payers_schema
from app.schemas import RoleEnum, self_tax_payers_schema

api = Namespace('view_tax', path="/view_tax", description='Filters for viewing tax')


@api.route('/view_tax_payers')
class ViewTaxPayers(Resource):
    @api.expect(get_filter_parser())
    @api.doc(security='Access Token')
    @access_token_required
    def post(self):
        payload=get_filter_parser().parse_args()
        op_status, resp = User.get_loggedin_user()
        current_user=db.session.query(TaxPayer).filter_by(username=resp['user']['username']).first()  
        print(current_user.username)
        date_created, date_modified, state_of_tax=payload['date_created'], payload['date_modified'], payload['state_of_tax']
        if not current_user:
            if date_modified:
                tax_payers_due=db.session.query(TaxPayer).order_by(TaxPayer.date_modified).all()
                return marshal({"tax_payers": tax_payers_due},date_modified_payers_schema), 200
            if date_created:
                tax_payers_due=db.session.query(TaxPayer).order_by(TaxPayer.user_date_created).all()
                return marshal({"tax_payers": tax_payers_due},date_created_payers_schema), 200
            if state_of_tax=='NEW':
                tax_payers_due=db.session.query(TaxPayer).filter_by(tax_status=1).order_by(TaxPayer.date_modified).all()
                return marshal({"tax_payers": tax_payers_due},state_of_tax_payers_schema), 200
            if state_of_tax=='PAID':
                tax_payers_due=db.session.query(TaxPayer).filter_by(tax_status=0).order_by(TaxPayer.date_modified).all()
                return marshal({"tax_payers": tax_payers_due},state_of_tax_payers_schema), 200
            if state_of_tax=='DELAYED':
                tax_payers_due=db.session.query(TaxPayer).filter_by(tax_status=2).order_by(TaxPayer.date_modified).all()
                return marshal({"tax_payers": tax_payers_due},state_of_tax_payers_schema), 200
        else:
            current_user=db.session.query(TaxPayer).filter_by(username=resp['user']['username']).first()
            return marshal({"tax_payers": current_user},self_tax_payers_schema), 200