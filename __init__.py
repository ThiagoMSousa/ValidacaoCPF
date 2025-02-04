import json
import re
import azure.functions as func

def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({'message': 'Invalid JSON'}),
            status_code=400,
            mimetype="application/json"
        )

    cpf = req_body.get('cpf', '')

    if not cpf:
        return func.HttpResponse(
            json.dumps({'message': 'CPF is required'}),
            status_code=400,
            mimetype="application/json"
        )

    is_valid = validate_cpf(cpf)
    return func.HttpResponse(
        json.dumps({'cpf': cpf, 'is_valid': is_valid}),
        status_code=200,
        mimetype="application/json"
    )