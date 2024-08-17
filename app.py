from flask import Flask, jsonify, request
import os, requests

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')
BASE_URL = 'https://marketplace.api.healthcare.gov/api/v1'
    
@app.route('/plans', methods=['POST'])
def list_plans():
    args = request.get_json()
    if args is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    if args.get('place') is None or args.get('market') is None or args.get('market') == '':
        return jsonify({"error": "Missing required fields"}), 400
    
    if args['place'].get('countyfips') is None or args['place'].get('countyfips') == '':
        fips = get_fips(args['place']['zipcode'])
        if fips is None:
            return jsonify({"error": "Error fetching fips"}), 400
        args['place']['countyfips'] = fips

    response = requests.post(f"{BASE_URL}/plans/search?apikey={API_KEY}", json=args, headers={'Content-Type': 'application/json'})
    output = ''

    if response.status_code == 200:

        response_data = response.json()
        plans_data = response_data.get('plans', [])
        plans = []

        for plan in plans_data:
            copay = []
            for benefit_item in plan['benefits']:
                if benefit_item['name'] == 'Specialist Visit':
                    cost = []
                    for cost_sharing in benefit_item['cost_sharings']:
                        cost.append({
                            'copay_amount': cost_sharing['copay_amount'],
                            'coinsurance_rate': cost_sharing['coinsurance_rate'],
                            'network_tier': cost_sharing['network_tier'],
                        })
                    copay.append(cost)
            
            deductibles = []
            for deductible_item in plan['deductibles']:
                deductibles.append({
                    'type': deductible_item['type'],
                    'amount': deductible_item['amount'],
                    'network_tier': deductible_item['network_tier'],
                    'csr': deductible_item['csr'],
                    'family': deductible_item['family'],
                    'individual': deductible_item['individual'],
                    'family_cost': deductible_item['family_cost'],
                })
                
            tiered_deductibles = []
            for tier_deductible_item in plan['tiered_deductibles']:
                tiered_deductibles.append({
                    'type': tier_deductible_item['type'],
                    'amount': tier_deductible_item['amount'],
                    'network_tier': tier_deductible_item['network_tier'],
                    'csr': tier_deductible_item['csr'],
                    'family': tier_deductible_item['family'],
                    'individual': tier_deductible_item['individual'],
                    'family_cost': tier_deductible_item['family_cost'],
                })

            moops = []
            for moops_item in plan['moops']:
                moops.append({
                    'type': moops_item['type'],
                    'amount': moops_item['amount'],
                    'network_tier': moops_item['network_tier'],
                    'csr': moops_item['csr'],
                    'family': moops_item['family'],
                    'individual': moops_item['individual'],
                    'family_cost': moops_item['family_cost'],
                })
                
            tiered_moops = []
            for tier_moops_item in plan['tiered_moops']:
                tiered_moops.append({
                    'type': tier_moops_item['type'],
                    'amount': tier_moops_item['amount'],
                    'network_tier': tier_moops_item['network_tier'],
                    'csr': tier_moops_item['csr'],
                    'family': tier_moops_item['family'],
                    'individual': tier_moops_item['individual'],
                    'family_cost': tier_moops_item['family_cost'],
                })

            issuer = plan.get('issuer', '')

            plan_info = {
                "name": plan.get('name', ''),
                "id": plan.get('id', ''),
                "issuer": {
                    "name": issuer.get('name', ''),
                    "id": issuer.get('id', ''),
                    "shop_url": issuer.get('shop_url', ''),
                    "individual_url": issuer.get('individual_url', ''),
                    "state": issuer.get('state', ''),
                    "toll_free": issuer.get('toll_free', ''),
                    "tty": issuer.get('tty', ''),
                },
                "sharings_specialist_visit": copay,
                "deductibles": deductibles,
                "tiered_deductibles": tiered_deductibles,
                "moops": moops,
                "tiered_moops": tiered_moops,
                "benefits_url": plan.get('benefits_url', ''),
                "brochure_url": plan.get('brochure_url', ''),
                "formulary_url": plan.get('formulary_url', ''),
                "network_url": plan.get('network_url', ''),
            }
            plans.append(plan_info)

        output = {
            "plans": plans,
            "ranges": response_data.get('ranges', {}),
            "total": response_data.get('total', 0),
        }
        return jsonify(output)
    else:
        return response.json()
    
@app.route('/plan')
def get_plan():
    args = request.args

    plan_id = args.get('plan_id')
    year = args.get('year')
    response = None
    if year:
        response = requests.get(f"{BASE_URL}/plans/{plan_id}?apikey={API_KEY}&plan_id={plan_id}&year={year}")
    else:
        response = requests.get(f"{BASE_URL}/plans/{plan_id}?apikey={API_KEY}&plan_id={plan_id}")
    return response.json()

@app.route('/issuers')
def get_issuers():
    args = request.args
    
    params = f"apikey={API_KEY}"
    year, state, limit, offset = args.get('year'), args.get('state'), args.get('limit'), args.get('offset')
    if year:
        params += f"&year={year}"
    if state:
        params += f"&state={state}"
    if limit:
        params += f"&limit={limit}"
    if offset:
        params += f"&offset={offset}"

    response = requests.get(f"{BASE_URL}/issuers?{params}")
    return response.json()

def get_fips(zipcode):
    response = requests.get(f"{BASE_URL}/counties/by/zip/{zipcode}?apikey={API_KEY}")
    if response.status_code == 200:
        try:
            return response.json()['counties'][0]['fips']
        except:
            return None
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')