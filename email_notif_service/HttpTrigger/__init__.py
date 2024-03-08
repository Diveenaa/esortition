import azure.functions as func
from azure.communication.email import EmailClient
import json
import time
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Parse request body
        req_body = req.get_json()
        recipient_address = req_body.get('recipient_address')
        subject = req_body.get('subject')
        plain_text_body = req_body.get('plain_text_body')
        html_body = req_body.get('html_body')

        # Call send_email function (assume it's defined elsewhere in the same file or imported)
        send_email_result = send_email(recipient_address, subject, plain_text_body, html_body)

        return func.HttpResponse(
            body=json.dumps({"message": "Email sent successfully", "details": send_email_result}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

# Function to send email
def send_email(recipient_address, subject, plain_text_body, html_body):
    connection_string = "endpoint=https://esortition-communication-services.uk.communication.azure.com/;accesskey=3JZRo1+vkmZb9GooIN/tuNuhmVHN+Oua7IZHDbOpTsNRKt/pIZhfnA8MejcILhAuK8w4aYbD3G0EvLKG+Jjc2w=="
    sender_address = "DoNotReply@29fbe95b-57aa-4326-8975-a78ba89ee5e8.azurecomm.net"
    
    POLLER_WAIT_TIME = 10

    message = {
        "senderAddress": sender_address,
        "recipients":  {
            "to": [{"address": recipient_address}],
        },
        "content": {
            "subject": subject,
            "plainText": plain_text_body,
            "html": html_body,
        }
    }

    try:
        client = EmailClient.from_connection_string(connection_string)

        poller = client.begin_send(message)

        time_elapsed = 0
        while not poller.done():
            print("Email send poller status: " + poller.status())
            time.sleep(POLLER_WAIT_TIME)  # Use time.sleep instead of poller.wait for waiting
            time_elapsed += POLLER_WAIT_TIME

            if time_elapsed > 18 * POLLER_WAIT_TIME:
                raise RuntimeError("Polling timed out.")

        if poller.result()["status"] == "Succeeded":
            print(f"Successfully sent the email to {recipient_address} (operation id: {poller.result()['id']})")
        else:
            raise RuntimeError(str(poller.result()["error"]))

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()