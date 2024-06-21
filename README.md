# OPG Šincek Web App Server (AWS Lambda Functions) 🚀

## Overview

This repository contains AWS Lambda functions used as a server for the OPG Šincek web application. These functions handle various backend tasks such as sending emails, managing images on the website, and handling admin login functionality.

### Key Features:

- **Email Sending**: Provides functionality to email PDF receipts.
  
- **Image Management**: Allows adding and removing images from the website dynamically.
  
- **Admin Login**: Implements secure login functionality for administrators to manage website content.

## Technologies Used:

- AWS Lambda
- Python
- MongoDB
- AWS SDK (for interacting with other AWS services like SES, S3, etc.)

## Functions Overview:

1. **Email Function**:
   - Sends emails using AWS SES (Simple Email Service) for various purposes such as user registrations, password resets, and notifications.

2. **Image Management Function**:
   - Allows administrators to upload, delete, and manage images stored in AWS S3 buckets for the website.

3. **Admin Login Function**:
   - Implements authentication and authorization mechanisms using AWS Cognito or custom authentication logic to secure admin access to backend resources.
