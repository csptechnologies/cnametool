# Author: Ryan Kim
# API Provider: Ryan Kim
import re
import requests 
from flask import Flask, request, render_template
app = Flask(__name__, template_folder='.', static_folder='.')
def e164_sanatize(phone_number: str) -> str:
    digits_clean = re.sub(r'\D', '', phone_number)
    if digits_clean:
        return f"+{digits_clean}"
    return None

@app.route('/', methods=['GET', 'POST'])
def lookup():
    rawinput = None
    sanitized_number = None
    upstreamdata = None
    error = None

    if request.method == 'POST':
        rawinput = request.form.get('phone_number')
        
        if rawinput:
            sanitized_number = e164_sanatize(rawinput)
            if sanitized_number:
                csp_api = f"https://api.csptech.org/cnam/lookup.php?number={sanitized_number}"
                
                try:
                    response = requests.get(csp_api, timeout=10)
                    upstreamdata = response.text

                except requests.RequestException as e:
                    error = f"Failed to fetch data from CSP API: {str(e)}"
            else:
                error = "Invalid phone number format."
        else:
            error = "No phone number provided."

    return render_template(
        'index.html', 
        rawinput=rawinput, 
        sanitized_num=sanitized_number, 
        csp_response=upstreamdata,
        error=error
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)