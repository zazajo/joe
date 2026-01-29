from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import resend
import os
import traceback

def home(request):
    return render(request, "pages/home.html", {})

def about(request):
    return render(request, 'pages/about.html')

def projects(request):
    return render(request, 'pages/projects.html')


def contact_view(request):
    """
    Handle contact form submissions and send email via Resend
    """
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'pages/contact.html')
        
        try:
            # Set up Resend API key
            resend.api_key = settings.RESEND_API_KEY
            
            # Prepare email content
            email_subject = f"Portfolio Contact: {subject}" if subject else f"New Contact from {name}"
            
            email_body = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f9f9f9;
                        border-radius: 10px;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 20px;
                        border-radius: 10px 10px 0 0;
                        text-align: center;
                    }}
                    .content {{
                        background: white;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }}
                    .field {{
                        margin-bottom: 20px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #667eea;
                        display: block;
                        margin-bottom: 5px;
                    }}
                    .value {{
                        color: #333;
                        padding: 10px;
                        background-color: #f5f5f5;
                        border-left: 4px solid #667eea;
                        border-radius: 4px;
                    }}
                    .message-box {{
                        background-color: #f5f5f5;
                        padding: 15px;
                        border-left: 4px solid #667eea;
                        border-radius: 4px;
                        margin-top: 10px;
                        white-space: pre-wrap;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        padding-top: 20px;
                        border-top: 2px solid #e0e0e0;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📧 New Contact Form Submission</h2>
                    </div>
                    <div class="content">
                        <div class="field">
                            <span class="label">From:</span>
                            <div class="value">{name}</div>
                        </div>
                        
                        <div class="field">
                            <span class="label">Email:</span>
                            <div class="value">
                                <a href="mailto:{email}" style="color: #667eea; text-decoration: none;">
                                    {email}
                                </a>
                            </div>
                        </div>
                        
                        {f'<div class="field"><span class="label">Subject:</span><div class="value">{subject}</div></div>' if subject else ''}
                        
                        <div class="field">
                            <span class="label">Message:</span>
                            <div class="message-box">{message}</div>
                        </div>
                        
                        <div class="footer">
                            <p>This message was sent from your portfolio contact form</p>
                            <p>Reply directly to <a href="mailto:{email}" style="color: #667eea;">{email}</a></p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Send email via Resend
            params = {
                "from": "Portfolio Contact <onboarding@resend.dev>",  
                "to": [settings.CONTACT_EMAIL],
                "subject": email_subject,
                "html": email_body,
                "reply_to": email,
            }
            
            response = resend.Emails.send(params)
            
            # Success message
            messages.success(
                request, 
                f'Thanks for reaching out, {name}! Your message has been sent successfully. I\'ll get back to you within 24 hours.'
            )
            
            # Redirect to avoid form resubmission on refresh
            return redirect('contact')
            
        except Exception as e:
            # Log the error (you might want to use proper logging in production)
            print(f"Error sending email: {str(e)}")
            
            messages.error(
                request, 
                'Sorry, there was an error sending your message. Please try again or contact me directly via email.'
            )
            return render(request, 'pages/contact.html')
    
    # GET request - just render the form
    return render(request, 'pages/contact.html')