import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="cpfvalidator")
def cpfvalidator(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            cpf = req_body.get('cpf')

    if cpf and is_valid_cpf(cpf):
        return func.HttpResponse(f"The CPF {cpf} is valid.")
    else:
        return func.HttpResponse(
             "Invalid CPF. Please provide a valid CPF in the query string or in the request body.",
             status_code=400
        )

def is_valid_cpf(cpf: str) -> bool:
    # Remove any non-numeric characters
    cpf = ''.join(filter(str.isdigit, cpf))

    # CPF must be 11 digits long
    if len(cpf) != 11:
        return False

    # Check for CPF with all digits the same (e.g., 111.111.111-11)
    if cpf == cpf[0] * len(cpf):
        return False

    # Calculate the first check digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    check_digit1 = (sum1 * 10 % 11) % 10

    # Calculate the second check digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    check_digit2 = (sum2 * 10 % 11) % 10

    # Check if the calculated check digits match the input
    return check_digit1 == int(cpf[9]) and check_digit2 == int(cpf[10])