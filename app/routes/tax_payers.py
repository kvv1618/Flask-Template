from flask_restx import Resource, Namespace, marshal
from datetime import datetime, timedelta
from app import bcrypt, db
from uuid import uuid4
from app.models import User
from flask_restx import Resource, Namespace
from app.models.user import TaxPayer
from app.schemas import RoleEnum, tax_payers_schema, tax_payer_schema, taxEnum
from app.utils import tax_payer_access_token_required,admin_or_accountant_token_required,get_tax_status_parser, get_tax_payer_details_parser, get_edited_detais_parser, tax_accountant_access_token_required

api = Namespace('tax_payers', path="/tax_payer", description='Operations on tax_payers')

@api.route("/all_tax_payers")
class AllTaxPayers(Resource):
    @api.doc(security='Access Token')
    @admin_or_accountant_token_required
    def get(self):
        tax_payers = db.session.query(User).filter_by(role=RoleEnum['TAX_PAYER'].value).all()
        return marshal({"tax_payers": tax_payers},tax_payers_schema), 200

@api.route("/edit_tax_payer")
class EditTaxPayer(Resource):
    @api.expect(get_tax_payer_details_parser())
    @api.doc(security='Access Token')
    @admin_or_accountant_token_required
    def post(self):
        payload = get_tax_payer_details_parser().parse_args()
        username,base_value_forGST, profit_forIncomeTax, state = payload['username'],payload['base_value_forGST'],payload['profit_forIncomeTax'],payload['state']
        due_date=datetime.fromisoformat(payload['due_date'])
        tax_payer=db.session.query(User).filter_by(username=username).first()
        if not tax_payer:
            return {"message": "Tax payer not found"}, 404
        tax_payer=db.session.query(TaxPayer).filter_by(username=username).first()
        if not tax_payer:
            total_tax=0
            sgst=cgst=0
            date=datetime.now()
            if(base_value_forGST>0):
                if(state=='INTERSTATE'):
                    cgst=base_value_forGST*0.09
                    sgst=base_value_forGST*0.09
                    total_tax=cgst+sgst
                else:
                    cgst=base_value_forGST*0.18
                    total_tax=cgst
            total_tax+=profit_forIncomeTax*0.05
            if(due_date<date):
                total_tax+=(50*(date-due_date).days)
            tax_payer=db.session.query(User).filter_by(username=username).first()
            new_tax_payer={
                "id": str(uuid4()),
                "user_id": tax_payer.id,
                "username": username,
                "cgst": cgst,
                "sgst": sgst,
                "total_due": total_tax,
                "due_date": due_date,
                "date_modified": datetime.now(),
                "user_date_created": tax_payer.created_at,
            }
            db.session.add(TaxPayer(**new_tax_payer))
            db.session.commit()
            return {"message": "Tax payer updated"}, 200
        tax_payer.due_date=due_date
        if(base_value_forGST>0):
            if(state=='INTERSTATE'):
                tax_payer.cgst+=base_value_forGST*0.09
                tax_payer.sgst+=base_value_forGST*0.09
                tax_payer.total_tax+=cgst+sgst
            else:
                tax_payer.cgst+=base_value_forGST*0.18
                tax_payer.total_due+=tax_payer.cgst
        tax_payer.total_due+=profit_forIncomeTax*0.05
        date=datetime.now()
        if(due_date<date):
            tax_payer.total_due+=(50*(date-due_date).days)
        db.session.commit()
        return {"message": "Tax payer updated"}, 200

@api.route("/edit_tax_due")
class EditTaxDue(Resource):
    @api.expect(get_edited_detais_parser())
    @api.doc(security='Access Token')
    @tax_accountant_access_token_required
    def post(self):
        payload=get_edited_detais_parser().parse_args()
        username, due_amount=payload['username'],payload['due_amount']
        tax_payer=db.session.query(TaxPayer).filter_by(username=username).first()
        if not tax_payer:
            return {"message": "Tax payer not found"}, 404
        if tax_payer.total_due==0 and tax_payer.tax_status==taxEnum['PAID'].value:
            tax_payer.total_due=due_amount
        else:
            return {'message': "Tax is pending to be paid"}, 400
        tax_payer.date_modified=datetime.now()
        db.session.commit()
        return {"message": "Tax payer updated"}, 200

@api.route("/pay_tax")
class PayTax(Resource):
    @api.expect(get_tax_status_parser())
    @api.doc(security='Access Token')
    @tax_payer_access_token_required
    def post(self):
        payload=get_tax_status_parser().parse_args()
        op_status, resp = User.get_loggedin_user()
        username=resp['user']['username']
        tax_payer=db.session.query(TaxPayer).filter_by(username=username).first()
        tax_payer.tax_status=taxEnum[payload['status']].value
        if tax_payer.tax_status==taxEnum['PAID'].value:
            tax_payer.total_due=0
        tax_payer.date_modified=datetime.now()
        db.session.commit()
        return {"message": "Congratulations on paying your tax"}, 200
        