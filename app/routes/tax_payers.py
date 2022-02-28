from flask_restx import Resource, Namespace, marshal
from datetime import datetime, timedelta
from app import bcrypt, db
from uuid import uuid4
from app.models import User
from flask_restx import Resource, Namespace
from app.models.user import TaxPayer
from app.schemas import RoleEnum, tax_payers_schema, tax_payer_schema, taxEnum
from app.utils import adim_or_accountant_token_required, get_tax_payer_details_parser

api = Namespace('tax_payers', path="/tax_payer", description='Operations on tax_payers')

@api.route("/all_tax_payers")
class AllTaxPayers(Resource):
    @api.doc(security='Access Token')
    @adim_or_accountant_token_required
    def get(self):
        tax_payers = db.session.query(User).filter_by(role=RoleEnum['TAX_PAYER'].value).all()
        return marshal({"tax_payers": tax_payers},tax_payers_schema), 200

@api.route("/edit_tax_payer")
class EditTaxPayer(Resource):
    @api.expect(get_tax_payer_details_parser())
    @api.doc(security='Access Token')
    @adim_or_accountant_token_required
    def post(self):
        payload = get_tax_payer_details_parser().parse_args()
        username,base_value_forGST, profit_forIncomeTax, state = payload['username'],payload['base_value_forGST'],payload['profit_forIncomeTax'],payload['state']
        due_date, status=datetime.fromisoformat(payload['due_date']), payload["status"]
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
            if(due_date<date and status!="PAID"):
                total_tax+=(50*(date-due_date).days)
            tax_payer=db.session.query(User).filter_by(username=username).first()
            new_tax_payer={
                "id": str(uuid4()),
                "user_id": tax_payer.id,
                "username": username,
                "tax_status":taxEnum[status].value,
                "cgst": cgst,
                "sgst": sgst,
                "total_due": total_tax,
                "due_date": due_date,
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
                tax_payer.total_tax+=cgst
        tax_payer.total_tax+=profit_forIncomeTax*0.05
        date=datetime.now()
        if(due_date<date and status!="PAID"):
            tax_payer.total_tax+=(50*(date-due_date).days)
        tax_payer.tax_status=taxEnum[status].value
        db.session.commit()
        return {"message": "Tax payer updated"}, 200