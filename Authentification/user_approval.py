import os
import time
from extract_signature import extracted_signature

def approve_signature(signature):
    with open('user_approval.txt', 'a') as file:
        file.write(signature + '\n')
    # Set a timer to delete the file after 30 minutes
    time.sleep(1800)
    os.remove('user_approval.txt')

approval = input("Do you approve this signature: {}? (Yes/No): ".format(extracted_signature)).lower()

if approval == 'yes':
    approve_signature(extracted_signature)
    print("Signature approved and stored in user_approval.txt for 30 minutes.")
else:
    print("Signature not approved.")
