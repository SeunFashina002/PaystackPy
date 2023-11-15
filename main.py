from paystackpyAPI.transaction import Transaction
from os import getenv
api_key = getenv("PAYSTACK_KEY")

transaction = Transaction(api_key)

# Example: Initialize a transaction
email = 'customer@example.com'
amount = 5000  # Replace with your desired amount

optional_params = {'callback_url': 'https://example.com/callback'}

# authorization_code='AUTH_72btv547'
currency = 'NGN'
try:
    initialization_response = transaction.initialize_transaction(email, amount, **optional_params)
    print("Initialization Response:", initialization_response)

    # Extract the reference from the initialization response
    reference_to_verify = initialization_response["response_from_api"]['data']['reference']

    try:
        auth_code = initialization_response["response_from_api"]['data']['authorization_url']
        auth_code = auth_code.split('/')[-1]
        print(auth_code)
        auth_transaction = transaction.charge_authorization(email, amount, auth_code, **optional_params)
        print("Authorization Response:", auth_transaction)
    except Exception as e:
        print("Error authorizing transaction:", str(e))
    # Example: Verify the transaction using the obtained reference
    try:
        verification_response = transaction.verify_transaction(reference_to_verify)
        print("Verification Response:", verification_response)
    except Exception as e:
        print("Error verifying transaction:", str(e))
    try:
        transactions = transaction.list_transactions()
        print("Transactions:", transactions)
    except Exception as e:
        print("Error listing transactions:", str(e))
    try:
        transaction_id = verification_response["response_from_api"]['data']['id']
        fetch_transaction = transaction.fetch_transaction(transaction_id)
        print("Transaction:", fetch_transaction)
    except Exception as e:
        print("Error fetching transaction:", str(e))
    try:
        total_transactions = transaction.get_transaction_totals()
        print("Total Transactions:", total_transactions)
    except Exception as e:
        print("Error getting total transactions:", str(e))
        
    try:
        export = transaction.export_transactions()
        print("export result :", export)
    except Exception as e:
        print("Error Exporting transactions:", str(e))

    #TODO: partial debit
    try:
        authorization_code = initialization_response["response_from_api"]['data']['authorization_url']
        authorization_code = authorization_code.split('/')[-1]
        partial_debit_response = transaction.partial_debit(authorization_code, email, currency, amount, **optional_params)
        print("Partial Debit:", partial_debit_response)
    except Exception as e:
        print("an error occured in partial debit:", str(e))

except Exception as e:
    print("Error initializing transaction:", str(e))
