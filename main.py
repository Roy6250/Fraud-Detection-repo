from fastapi import FastAPI, File, UploadFile, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from typing import List
from PIL import Image
import io
import google.generativeai as genai
import urllib.request 
from io import BytesIO
app = FastAPI()
from typing import Optional

from pydantic import BaseModel

class questions(BaseModel):
    conversation: str

prompt='''
Instructions :
Cyber criminals use a variety of attack vectors and strategies to commit internet fraud. This includes malicious software, email and instant messaging services to spread malware, spoofed websites that steal user data, and elaborate, wide-reaching phishing scams.

Internet fraud can be broken down into several key types of attacks, including:

Phishing and spoofing: The use of email and online messaging services to dupe victims into sharing personal data, login credentials, and financial details.
Data breach: Stealing confidential, protected, or sensitive data from a secure location and moving it into an untrusted environment. This includes data being stolen from users and organizations.
Denial of service (DoS): Interrupting access of traffic to an online service, system, or network to cause malicious intent.
Malware: The use of malicious software to damage or disable users’ devices or steal personal and sensitive data.
Ransomware: A type of malware that prevents users from accessing critical data then demanding payment in the promise of restoring access. Ransomware is typically delivered via phishing attacks.
Business email compromise (BEC): A sophisticated form of attack targeting businesses that frequently make wire payments. It compromises legitimate email accounts through social engineering techniques to submit unauthorized payments.
To avoid hackers’ internet fraud attempts, users need to understand common examples of internet fraud and tactics.

Email phishing scams
Email-based phishing scams are among the most prevalent types of internet fraud, which continues to pose a serious threat to internet users and businesses. 

Statistics from Security Boulevard show that in 2020, 22% of all data breaches involved a phishing attack, and 95% of all attacks that targeted business networks were caused by spear phishing. Furthermore, 97% of users could not spot a sophisticated phishing email, 1.5 million new phishing sites were created every month, and 78% of users understand the risk of hyperlinks in emails but click them anyway.

Email-based phishing scams are constantly evolving and range from simple attacks to more sneaky and complex threats that target specific individuals.

Email phishing scams see cyber criminals masquerade as an individual that their victim either knows or would consider reputable. The attack aims to encourage people to click on a link that leads to a malicious or spoofed website designed to look like a legitimate website, or open an attachment that contains malicious content.

The hacker first compromises a legitimate website or creates a fake website. They then acquire a list of email addresses to target and distribute an email message that aims to dupe people into clicking on a link to that website. When a victim clicks the link, they are taken to the spoofed website, which will either request a username and password or automatically download malware onto their device, which will steal data and login credential information. The hacker can use this data to access the user’s online accounts, steal more data like credit card details, access corporate networks attached to the device, or commit wider identity fraud.

Email phishing scam attackers will often express the need for urgency from their victims. This includes telling them that their online account or credit card is at risk, and they need to log in immediately to rectify the issue.

Greeting card scams
Many internet fraud attacks focus on popular events to scam the people that celebrate them. This includes birthdays, Christmas, and Easter, which are commonly marked by sharing greeting cards with friends and family members via email. Hackers typically exploit this by installing malicious software within an email greeting card, which downloads and installs onto the recipient’s device when they open the greeting card.

The consequences can be devastating. The malware could result in annoying pop-up ads that can affect application performance and slow down the device. A more worrying result would be the victim’s personal and financial data being stolen and their computer being used as a bot within a vast network of compromised computers, also known as a botnet.

Credit card scams
Credit card fraud typically occurs when hackers fraudulently acquire people's credit or debit card details in an attempt to steal money or make purchases. 

To obtain these details, internet fraudsters often use too-good-to-be-true credit card or bank loan deals to lure victims. For example, a victim might receive a message from their bank telling them they are eligible for a special loan deal or a vast amount of money has been made available to them as a loan. These scams continue to trick people despite widespread awareness that such offers are too good to be true for a reason.

Online dating scams
Another typical example of internet fraud targets the plethora of online dating applications and websites. Hackers focus on these apps to lure victims into sending money and sharing personal data with new love interests. Scammers typically create fake profiles to interact with users, develop a relationship, slowly build their trust, create a phony story, and ask the user for financial help.

Lottery fee fraud
Another common form of internet fraud is email scams that tell victims they have won the lottery. These scams will inform recipients that they can only claim their prize after they have paid a small fee.

Lottery fee fraudsters typically craft emails to look and sound believable, which still results in many people falling for the scam. The scam targets people's dreams of winning massive amounts of money, even though they may have never purchased a lottery ticket. Furthermore, no legitimate lottery scheme will ask winners to pay to claim their prize. 

The Nigerian prince
A classic internet fraud tactic, the Nigerian Prince scam approach remains common and thriving despite widespread awareness.

The scam uses the premise of a wealthy Nigerian family or individual who wants to share their wealth in return for assistance in accessing their inheritance. It uses phishing tactics to send emails that outline an emotional backstory, then lures victims into a promise of significant financial reward. The scam typically begins by asking for a small fee to help with legal processes and paperwork with the promise of a large sum of money further down the line. 

The scammer will inevitably ask for more extensive fees to cover further administration tasks and transaction costs supported by legitimate-looking confirmation documents. However, the promised return on investment never arrives.

Prompt: Analyze the contents the image and detect whether's it a fraud, spam or any other scam or not.
'''

ques_prompt='''
Instructions :
Cyber criminals use a variety of attack vectors and strategies to commit internet fraud. This includes malicious software, email and instant messaging services to spread malware, spoofed websites that steal user data, and elaborate, wide-reaching phishing scams.

Internet fraud can be broken down into several key types of attacks, including:

Phishing and spoofing: The use of email and online messaging services to dupe victims into sharing personal data, login credentials, and financial details.
Data breach: Stealing confidential, protected, or sensitive data from a secure location and moving it into an untrusted environment. This includes data being stolen from users and organizations.
Denial of service (DoS): Interrupting access of traffic to an online service, system, or network to cause malicious intent.
Malware: The use of malicious software to damage or disable users’ devices or steal personal and sensitive data.
Ransomware: A type of malware that prevents users from accessing critical data then demanding payment in the promise of restoring access. Ransomware is typically delivered via phishing attacks.
Business email compromise (BEC): A sophisticated form of attack targeting businesses that frequently make wire payments. It compromises legitimate email accounts through social engineering techniques to submit unauthorized payments.
To avoid hackers’ internet fraud attempts, users need to understand common examples of internet fraud and tactics.

Email phishing scams
Email-based phishing scams are among the most prevalent types of internet fraud, which continues to pose a serious threat to internet users and businesses. 

Statistics from Security Boulevard show that in 2020, 22% of all data breaches involved a phishing attack, and 95% of all attacks that targeted business networks were caused by spear phishing. Furthermore, 97% of users could not spot a sophisticated phishing email, 1.5 million new phishing sites were created every month, and 78% of users understand the risk of hyperlinks in emails but click them anyway.

Email-based phishing scams are constantly evolving and range from simple attacks to more sneaky and complex threats that target specific individuals.

Email phishing scams see cyber criminals masquerade as an individual that their victim either knows or would consider reputable. The attack aims to encourage people to click on a link that leads to a malicious or spoofed website designed to look like a legitimate website, or open an attachment that contains malicious content.

The hacker first compromises a legitimate website or creates a fake website. They then acquire a list of email addresses to target and distribute an email message that aims to dupe people into clicking on a link to that website. When a victim clicks the link, they are taken to the spoofed website, which will either request a username and password or automatically download malware onto their device, which will steal data and login credential information. The hacker can use this data to access the user’s online accounts, steal more data like credit card details, access corporate networks attached to the device, or commit wider identity fraud.

Email phishing scam attackers will often express the need for urgency from their victims. This includes telling them that their online account or credit card is at risk, and they need to log in immediately to rectify the issue.

Greeting card scams
Many internet fraud attacks focus on popular events to scam the people that celebrate them. This includes birthdays, Christmas, and Easter, which are commonly marked by sharing greeting cards with friends and family members via email. Hackers typically exploit this by installing malicious software within an email greeting card, which downloads and installs onto the recipient’s device when they open the greeting card.

The consequences can be devastating. The malware could result in annoying pop-up ads that can affect application performance and slow down the device. A more worrying result would be the victim’s personal and financial data being stolen and their computer being used as a bot within a vast network of compromised computers, also known as a botnet.

Credit card scams
Credit card fraud typically occurs when hackers fraudulently acquire people's credit or debit card details in an attempt to steal money or make purchases. 

To obtain these details, internet fraudsters often use too-good-to-be-true credit card or bank loan deals to lure victims. For example, a victim might receive a message from their bank telling them they are eligible for a special loan deal or a vast amount of money has been made available to them as a loan. These scams continue to trick people despite widespread awareness that such offers are too good to be true for a reason.

Online dating scams
Another typical example of internet fraud targets the plethora of online dating applications and websites. Hackers focus on these apps to lure victims into sending money and sharing personal data with new love interests. Scammers typically create fake profiles to interact with users, develop a relationship, slowly build their trust, create a phony story, and ask the user for financial help.

Lottery fee fraud
Another common form of internet fraud is email scams that tell victims they have won the lottery. These scams will inform recipients that they can only claim their prize after they have paid a small fee.

Lottery fee fraudsters typically craft emails to look and sound believable, which still results in many people falling for the scam. The scam targets people's dreams of winning massive amounts of money, even though they may have never purchased a lottery ticket. Furthermore, no legitimate lottery scheme will ask winners to pay to claim their prize. 

The Nigerian prince
A classic internet fraud tactic, the Nigerian Prince scam approach remains common and thriving despite widespread awareness.

The scam uses the premise of a wealthy Nigerian family or individual who wants to share their wealth in return for assistance in accessing their inheritance. It uses phishing tactics to send emails that outline an emotional backstory, then lures victims into a promise of significant financial reward. The scam typically begins by asking for a small fee to help with legal processes and paperwork with the promise of a large sum of money further down the line. 

The scammer will inevitably ask for more extensive fees to cover further administration tasks and transaction costs supported by legitimate-looking confirmation documents. However, the promised return on investment never arrives.

Prompt: Analyze the text and detect whether's it a fraud, spam or any other scam or not.
'''
genai.configure(api_key='AIzaSyCVSPwfCwvG7U-oMzWg8glv0oZt5-A1mjY')

# Initialize the model
# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/fraud-detection-image/")
async def detect_fraud_endpoint(file: UploadFile = File(...)):
    global prompt
    try:
        # Read the image file
        image = Image.open(io.BytesIO(await file.read()))

        # Detect fraud using the Gemini model
        response = model.generate_content([prompt,image])
        print(response.text)
        # Return the result
        return JSONResponse(content={"message":list({response.text})})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")



@app.post("/fraud-detection-text/")
async def detect_fraud_endpoint(quest:questions):

    global prompt
    try:
        # Read the image file
        print(quest)

        text = quest.conversation

        prompt= ques_prompt+text
        # Detect fraud using the Gemini model
        response = model.generate_content(prompt)
        print(response.text)
        # Return the result
        return JSONResponse(content={"message":list({response.text})})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

