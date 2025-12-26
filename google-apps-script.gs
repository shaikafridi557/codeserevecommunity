/**
 * @OnlyCurrentDoc
 */

// Required OAuth Scopes
// This tells Google Apps Script what permissions we need
const REQUIRED_SCOPES = [
  'https://www.googleapis.com/auth/script.send_mail',
  'https://www.googleapis.com/auth/spreadsheets'
];

// Google Apps Script for Code.Serve Pricing Demo Management
// This script manages customer data and auto-generates demo links

// TO FIND YOUR SHEET ID:
// 1. Open your Google Sheet
// 2. Look at the URL: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
// 3. Copy the SHEET_ID_HERE part and paste it below

const SHEET_ID = '1Qr4_s4_TD75j7-2BmQdTndvDS9df1fwy76qwH0JGGzs'; // Your actual Sheet ID
const SHEET_NAME = 'DemoCustomers'; // Name of your sheet
const SETTINGS_SHEET_NAME = 'Settings'; // Settings sheet to track demo counter

// Get the spreadsheet
function getSheet() {
  try {
    // For container-bound scripts, use getActiveSpreadsheet
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    return ss.getSheetByName(SHEET_NAME);
  } catch (error) {
    Logger.log('Error getting sheet: ' + error.toString());
    
    // Fallback to openById for standalone scripts
    try {
      const ss = SpreadsheetApp.openById(SHEET_ID);
      return ss.getSheetByName(SHEET_NAME);
    } catch (fallbackError) {
      Logger.log('Fallback also failed: ' + fallbackError.toString());
      return null;
    }
  }
}

// Get the next demo number (finds the lowest available number)
function getNextDemoNumber() {
  const sheet = getSheet();
  if (!sheet) return 0; // Start from 0 (which becomes "demo")
  
  const data = sheet.getDataRange().getValues();
  const usedNumbers = new Set();
  
  // Skip header row and collect all used demo numbers
  // DemoLink is in column B (index 1)
  for (let i = 1; i < data.length; i++) {
    const demoLink = data[i][1]; // DemoLink is in column B (index 1)
    if (demoLink && typeof demoLink === 'string') {
      // Handle format: https://demo.netlify.com (number = 0) or https://demo1.netlify.com (number = 1), https://demo2.netlify.com (number = 2), etc.
      if (demoLink === 'https://demo.netlify.com') {
        usedNumbers.add(0);
      } else {
        // Match demo followed by optional digits
        const match = demoLink.match(/demo(\d*)\.netlify\.com/);
        if (match) {
          const numStr = match[1];
          const num = numStr === '' ? 0 : parseInt(numStr);
          usedNumbers.add(num);
        }
      }
    }
  }
  
  // Find the lowest available number
  let nextNumber = 0;
  while (usedNumbers.has(nextNumber)) {
    nextNumber++;
  }
  
  Logger.log('Used demo numbers:', Array.from(usedNumbers));
  Logger.log('Next demo number:', nextNumber);
  
  return nextNumber;
}

// Generate demo link with sequential number
function generateDemoLink() {
  const demoNumber = getNextDemoNumber();
  
  // Format: https://demo.netlify.com (first = 0), https://demo1.netlify.com (second = 1), https://demo2.netlify.com (third = 2), etc.
  if (demoNumber === 0) {
    return 'https://demo.netlify.com';
  } else {
    return `https://demo${demoNumber}.netlify.com`;
  }
}

// Save customer record
function saveCustomer(email, businessName, phone, demoRequirements, address) {
  Logger.log('=== SAVE CUSTOMER CALLED ===');
  Logger.log('Received email:', email);
  Logger.log('Received businessName:', businessName);
  Logger.log('Received phone:', phone);
  Logger.log('Received demoRequirements:', demoRequirements);
  Logger.log('Received address:', address);
  
  try {
    const sheet = getSheet();
    if (!sheet) {
      return {
        success: false,
        message: 'Could not access spreadsheet'
      };
    }
    
    // Check if customer already exists
    const data = sheet.getDataRange().getValues();
    const normalizedEmail = email.toLowerCase().trim();
    for (let i = 1; i < data.length; i++) {
      const sheetEmail = data[i][0] ? data[i][0].toLowerCase().trim() : '';
      if (sheetEmail === normalizedEmail) { // Email is in column A (index 0)
        return {
          success: false,
          message: 'Customer already exists',
          exists: true
        };
      }
    }
    
    // Generate demo link and get the number
    const demoNumber = getNextDemoNumber();
    const demoLink = generateDemoLink();
    
    Logger.log('Generated demo link:', demoLink, 'for demo number:', demoNumber);
    
    // Add new row - matching your sheet columns: Email, DemoLink, DemoStatus, Timestamp, BusinessName, Phone, DemoRequirements, Address
    const newRow = [
      email,
      demoLink,
      'pending', // DemoStatus
      new Date(), // Timestamp
      businessName,
      phone,
      demoRequirements,
      address || ''
    ];
    
    sheet.appendRow(newRow);
    
    // Send admin notification
    sendAdminNotification(email, businessName, phone, demoRequirements, demoLink);
    
    return {
      success: true,
      message: 'Customer saved successfully',
      demoNumber: demoNumber,
      placeholder: demoNumber === 0 ? 'demo' : `demo${demoNumber}`
    };
    
  } catch (error) {
    Logger.log('Error saving customer:', error);
    return {
      success: false,
      message: 'Error saving customer: ' + error.toString()
    };
  }
}

// Check customer status - verify both email and phone
function checkCustomer(email, phone) {
  try {
    const sheet = getSheet();
    if (!sheet) {
      return {
        success: false,
        message: 'Could not access spreadsheet'
      };
    }
    
    const data = sheet.getDataRange().getValues();
    const normalizedEmail = email.toLowerCase().trim();
    const normalizedPhone = phone ? phone.toString().replace(/\D/g, '') : '';
    
    Logger.log('Login attempt - Email: ' + normalizedEmail + ', Phone: ' + normalizedPhone);
    
    for (let i = 1; i < data.length; i++) {
      const sheetEmail = data[i][0] ? data[i][0].toString().toLowerCase().trim() : '';
      const sheetPhoneRaw = data[i][5]; // Phone is in column F (index 5)
      const sheetPhone = sheetPhoneRaw ? sheetPhoneRaw.toString().replace(/\D/g, '') : '';
      
      Logger.log('Row ' + i + ' - Sheet Email: ' + sheetEmail + ', Sheet Phone: ' + sheetPhone + ', Raw: ' + sheetPhoneRaw);
      
      // Match both email and phone
      if (sheetEmail === normalizedEmail) {
        Logger.log('Email matched! Checking phone...');
        Logger.log('Comparing phones - Provided: ' + normalizedPhone + ', Sheet: ' + sheetPhone);
        
        // If phone is provided, verify it matches (check last 10 digits in case of country code)
        if (normalizedPhone) {
          // Check if the provided phone matches the sheet phone
          // Also check if sheet phone ends with provided phone (in case of country code)
          const phoneMatches = (sheetPhone === normalizedPhone) || (sheetPhone.endsWith(normalizedPhone));
          
          if (!phoneMatches) {
            Logger.log('Phone mismatch! Expected: ' + normalizedPhone + ', Got: ' + sheetPhone);
            return {
              success: true,
              exists: false,
              message: 'Email found but phone number does not match'
            };
          }
        }
        
        Logger.log('Phone matched! Returning customer data.');
        return {
          success: true,
          exists: true,
          data: {
            customer: {
              Email: data[i][0],
              DemoLink: data[i][1],
              DemoStatus: data[i][2],
              Timestamp: data[i][3],
              BusinessName: data[i][4],
              Phone: data[i][5],
              DemoRequirements: data[i][6],
              Address: data[i][7]
            }
          }
        };
      }
    }
    
    Logger.log('No matching email found in sheet');
    
    return {
      success: true,
      exists: false,
      message: 'Customer not found'
    };
    
  } catch (error) {
    Logger.log('Error checking customer:', error);
    return {
      success: false,
      message: 'Error checking customer: ' + error.toString()
    };
  }
}

// Verify that demo link belongs to the customer
function verifyDemoLink(email, demoLink) {
  try {
    const sheet = getSheet();
    if (!sheet) {
      return {
        success: false,
        isValid: false,
        message: 'Could not access spreadsheet'
      };
    }
    
    const data = sheet.getDataRange().getValues();
    const normalizedEmail = email.toLowerCase().trim();
    
    for (let i = 1; i < data.length; i++) {
      const sheetEmail = data[i][0] ? data[i][0].toLowerCase().trim() : '';
      if (sheetEmail === normalizedEmail) { // Email is in column A (index 0)
        const storedDemoLink = data[i][1]; // DemoLink is in column B (index 1)
        
        // Check if the provided demo link matches the one stored for this customer
        if (storedDemoLink === demoLink) {
          return {
            success: true,
            isValid: true,
            message: 'Demo link verified for this customer'
          };
        } else {
          return {
            success: true,
            isValid: false,
            message: 'Demo link does not match customer record',
            storedLink: storedDemoLink,
            providedLink: demoLink
          };
        }
      }
    }
    
    return {
      success: true,
      isValid: false,
      message: 'Customer not found'
    };
    
  } catch (error) {
    Logger.log('Error verifying demo link:', error);
    return {
      success: false,
      isValid: false,
      message: 'Error verifying demo link: ' + error.toString()
    };
  }
}

// Update customer record
function updateCustomer(email, demoLink, demoStatus) {
  try {
    const sheet = getSheet();
    if (!sheet) {
      return {
        success: false,
        message: 'Could not access spreadsheet'
      };
    }
    
    const data = sheet.getDataRange().getValues();
    const normalizedEmail = email.toLowerCase().trim();
    
    for (let i = 1; i < data.length; i++) {
      const sheetEmail = data[i][0] ? data[i][0].toLowerCase().trim() : '';
      if (sheetEmail === normalizedEmail) { // Email is in column A (index 0)
        sheet.getRange(i + 1, 2).setValue(demoLink); // Update DemoLink (column B)
        sheet.getRange(i + 1, 3).setValue(demoStatus); // Update DemoStatus (column C)
        
        return {
          success: true,
          message: 'Customer updated successfully'
        };
      }
    }
    
    return {
      success: false,
      message: 'Customer not found'
    };
    
  } catch (error) {
    Logger.log('Error updating customer:', error);
    return {
      success: false,
      message: 'Error updating customer: ' + error.toString()
    };
  }
}

// Test admin notification
function testAdminNotification() {
  console.log('=== EMAIL SERVICE TEST ===');
  
  try {
    // Check email quota
    const quota = MailApp.getRemainingDailyQuota();
    console.log('Remaining email quota: ' + quota);
    
    if (quota === 0) {
      console.log('ERROR: Email quota exhausted!');
      return { success: false, message: 'Email quota exhausted' };
    }
    
    const testEmail = 'codeserve.contact@gmail.com';
    const subject = 'Test Admin Notification - Code.Serve';
    const body = 'Test Email - Time: ' + new Date().toLocaleString();
    
    console.log('Sending to: ' + testEmail);
    console.log('Subject: ' + subject);
    
    // Send email
    MailApp.sendEmail(testEmail, subject, body);
    
    console.log('SUCCESS: Email sent!');
    return { success: true, message: 'Test email sent' };
    
  } catch (error) {
    console.log('ERROR occurred: ' + String(error));
    console.log('Error message: ' + (error.message || 'unknown'));
    return { success: false, message: String(error) };
  }
}

// Simple test - this will trigger authorization
function simpleEmailTest() {
  MailApp.sendEmail('codeserve.contact@gmail.com', 'Test', 'This is a test email');
  console.log('Email sent!');
}

// Health check
function healthCheck() {
  return {
    success: true,
    message: 'Google Apps Script is running',
    timestamp: new Date().toISOString()
  };
}

// Debug function to list all sheet names
function listSheets() {
  try {
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const sheets = ss.getSheets();
    const sheetNames = sheets.map(sheet => sheet.getName());
    
    return {
      success: true,
      sheetNames: sheetNames,
      message: 'Available sheets: ' + sheetNames.join(', ')
    };
  } catch (error) {
    return {
      success: false,
      message: 'Error listing sheets: ' + error.toString()
    };
  }
}

// Get the last demo number (for reference before clearing)
function getLastDemoNumber() {
  try {
    const sheet = getSheet();
    if (!sheet) {
      return {
        success: false,
        message: 'Could not access spreadsheet'
      };
    }
    
    const data = sheet.getDataRange().getValues();
    let maxNumber = 0;
    
    // Find the highest demo number
    for (let i = 1; i < data.length; i++) {
      const demoLink = data[i][1];
      if (demoLink && typeof demoLink === 'string') {
        if (demoLink === 'https://demo.netlify.com') {
          maxNumber = Math.max(maxNumber, 0);
        } else {
          const match = demoLink.match(/demo(\d*)\.netlify\.com/);
          if (match) {
            const numStr = match[1];
            const num = numStr === '' ? 0 : parseInt(numStr);
            maxNumber = Math.max(maxNumber, num);
          }
        }
      }
    }
    
    return {
      success: true,
      lastDemoNumber: maxNumber,
      nextDemoNumber: maxNumber + 1,
      lastDemoLink: maxNumber === 0 ? 'https://demo.netlify.com' : `https://demo${maxNumber}.netlify.com`,
      nextDemoLink: maxNumber === 0 ? 'https://demo1.netlify.com' : `https://demo${maxNumber + 1}.netlify.com`,
      totalRecords: data.length - 1,
      message: `Last demo: ${maxNumber === 0 ? 'https://demo.netlify.com' : `https://demo${maxNumber}.netlify.com`} | Next will be: ${maxNumber === 0 ? 'https://demo1.netlify.com' : `https://demo${maxNumber + 1}.netlify.com`}`
    };
  } catch (error) {
    return {
      success: false,
      message: 'Error getting last demo number: ' + error.toString()
    };
  }
}

// ===== EMAIL FUNCTIONS (Google Apps Script Backend) =====

// Send admin notification when demo is booked
function sendAdminNotification(email, businessName, phone, demoRequirements, demoLink) {
  Logger.log('=== ADMIN NOTIFICATION STARTED ===');
  Logger.log('Email:', email);
  Logger.log('Business:', businessName);
  Logger.log('Phone:', phone);
  Logger.log('Demo Link:', demoLink);
  
  try {
    // Multiple admin emails
    const adminEmails = [
      'codeserve.contact@gmail.com',
      'shaikafridi557@gmail.com',
      'srinivasvenkatasai23@gmail.com'
    ];
    
    Logger.log('Admin emails:', adminEmails);
    
    const subject = 'New Demo Booking - ' + businessName;
    
    const htmlBody = `
      <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            
            <div style="background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;">
              <h2 style="margin: 0; font-size: 24px;">🎉 New Demo Booking!</h2>
              <p style="margin: 10px 0 0 0; opacity: 0.9;">A customer has requested a demo</p>
            </div>
            
            <div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
              <h3 style="margin: 0 0 15px 0; color: #1f2937;">Customer Details:</h3>
              
              <table style="width: 100%; border-collapse: collapse;">
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #374151; width: 120px;">Business:</td>
                  <td style="padding: 8px 0; color: #6b7280;">${businessName}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #374151;">Email:</td>
                  <td style="padding: 8px 0; color: #6b7280;"><a href="mailto:${email}" style="color: #2563eb; text-decoration: none;">${email}</a></td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #374151;">Phone:</td>
                  <td style="padding: 8px 0; color: #6b7280;"><a href="tel:${phone}" style="color: #2563eb; text-decoration: none;">${phone}</a></td>
                </tr>
                <tr>
                  <td style="padding: 8px 0; font-weight: bold; color: #374151;">Demo Link:</td>
                  <td style="padding: 8px 0; color: #6b7280; word-break: break-all;">${demoLink}</td>
                </tr>
              </table>
            </div>
            
            <div style="background-color: #f0fdf4; border-left: 4px solid #10b981; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
              <h3 style="margin: 0 0 15px 0; color: #1f2937;">Demo Requirements:</h3>
              <p style="margin: 0; color: #374151; white-space: pre-wrap; background-color: white; padding: 15px; border-radius: 4px; border: 1px solid #e5e7eb;">${demoRequirements}</p>
            </div>
            
            <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
              <h3 style="margin: 0 0 10px 0; color: #92400e;">⏱ Next Steps:</h3>
              <ol style="margin: 0; padding-left: 20px; color: #92400e;">
                <li>Build the demo (1-2 pages)</li>
                <li>Update the Google Sheet status to "done"</li>
                <li>Customer will receive demo link automatically</li>
              </ol>
            </div>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="text-align: center; color: #6b7280; font-size: 12px;">
              This is an automated notification from Code.Serve Demo System
            </p>
            
          </div>
        </body>
      </html>
    `;
    
    // Send to all admin emails
    Logger.log('Starting to send emails to admins...');
    adminEmails.forEach(adminEmail => {
      try {
        Logger.log('Sending email to:', adminEmail);
        const plainText = 'New Demo Booking\n\nBusiness: ' + businessName + '\nEmail: ' + email + '\nPhone: ' + phone + '\nDemo Link: ' + demoLink + '\n\nRequirements:\n' + demoRequirements;
        
        // Use MailApp for better compatibility
        MailApp.sendEmail({
          to: adminEmail,
          subject: subject,
          body: plainText,
          htmlBody: htmlBody,
          name: 'Code.Serve Demo System'
        });
        
        Logger.log('✅ Admin notification sent to:', adminEmail);
      } catch (emailError) {
        Logger.log('❌ Failed to send to ' + adminEmail + ':', emailError.toString());
      }
    });
    Logger.log('All emails processed');
    
    return { success: true, message: 'All admins notified' };
    
  } catch (error) {
    Logger.log('Error sending admin notification:', error.toString());
    Logger.log('Error name:', error.name);
    Logger.log('Error message:', error.message);
    Logger.log('Full error:', JSON.stringify(error));
    return { success: false, message: 'Failed to notify admin: ' + error.toString() };
  }
}

// Send demo request confirmation email via Google Apps Script
function sendDemoRequestEmailBackend(email, businessName, phone, demoRequirements) {
  try {
    const subject = 'Demo Request Received - Code.Serve';
    const htmlBody = `
      <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2563eb;">Thank You for Your Demo Request!</h2>
            
            <p>Hello <strong>${businessName}</strong>,</p>
            
            <p>We've received your demo request and we're excited to work with you!</p>
            
            <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="margin-top: 0; color: #1f2937;">Your Request Details:</h3>
              <p><strong>Email:</strong> ${email}</p>
              <p><strong>Phone:</strong> ${phone}</p>
              <p><strong>Requirements:</strong></p>
              <p style="white-space: pre-wrap; background-color: white; padding: 10px; border-radius: 4px;">${demoRequirements}</p>
            </div>
            
            <p><strong>What's Next?</strong></p>
            <p>Our team will prepare your personalized demo within <strong>2 business days</strong>. We'll send you a private demo link via email once it's ready.</p>
            
            <p>In the meantime, if you have any questions or need to make changes to your request, feel free to reach out.</p>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #6b7280; font-size: 0.9em;">
              Best regards,<br>
              <strong>Code.Serve Team</strong><br>
              <a href="https://codeserve.com" style="color: #2563eb;">Visit our website</a>
            </p>
          </div>
        </body>
      </html>
    `;
    
    const plainText = `Thank You for Your Demo Request!

Hello ${businessName},

We've received your demo request and we're excited to work with you!

Your Request Details:
- Email: ${email}
- Phone: ${phone}
- Requirements: ${demoRequirements}

What's Next?
Our team will prepare your personalized demo within 2 business days. We'll send you a private demo link via email once it's ready.

In the meantime, if you have any questions or need to make changes to your request, feel free to reach out.

Best regards,
Code.Serve Team
Visit our website: https://codeservecommunity.netlify.app`;
    
    GmailApp.sendEmail(email, subject, plainText, {
      htmlBody: htmlBody,
      name: 'Code.Serve'
    });
    
    Logger.log('Demo request email sent to:', email);
    return {
      success: true,
      message: 'Demo request confirmation email sent'
    };
  } catch (error) {
    Logger.log('Error sending demo request email:', error);
    return {
      success: false,
      message: 'Failed to send email: ' + error.toString()
    };
  }
}

// Send demo ready notification email via Google Apps Script
function sendDemoReadyEmailBackend(email, demoLink) {
  try {
    console.log('=== SENDING DEMO READY EMAIL ===');
    console.log('To email: ' + email);
    console.log('Demo link: ' + demoLink);
    
    if (!email || !demoLink) {
      console.log('❌ Missing email or demo link!');
      return { success: false, message: 'Missing email or demo link' };
    }
    
    const subject = 'Your Demo is Ready - Code.Serve';
    const htmlBody = `
      <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #10b981;">🎉 Your Demo is Ready!</h2>
            
            <p>Great news! Your personalized demo has been prepared and is ready for review.</p>
            
            <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10b981;">
              <p style="margin: 0;"><strong>Access your demo here:</strong></p>
              <p style="margin: 10px 0 0 0;">
                <a href="${demoLink}" style="display: inline-block; background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">
                  View Your Demo
                </a>
              </p>
              <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #6b7280;">
                Or copy this link: <code style="background-color: white; padding: 2px 6px; border-radius: 3px;">${demoLink}</code>
              </p>
            </div>
            
            <p><strong>Next Steps:</strong></p>
            <ol>
              <li>Review the demo and explore all the features</li>
              <li>If you're satisfied, return to our pricing page and paste the demo link to unlock our full pricing plans</li>
              <li>Choose the package that best fits your needs</li>
            </ol>
            
            <p>If you have any questions, feedback, or need modifications to the demo, please don't hesitate to reach out. We're here to help!</p>
            
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
            
            <p style="color: #6b7280; font-size: 0.9em;">
              Best regards,<br>
              <strong>Code.Serve Team</strong><br>
              <a href="https://codeservecommunity.netlify.app" style="color: #2563eb;">Visit our website</a>
            </p>
          </div>
        </body>
      </html>
    `;
    
    const plainText = 'Your Demo is Ready!\n\nGreat news! Your personalized demo has been prepared and is ready for review.\n\nAccess your demo here: ' + demoLink + '\n\nNext Steps:\n1. Review the demo and explore all the features\n2. If you are satisfied, return to our pricing page and paste the demo link to unlock our full pricing plans\n3. Choose the package that best fits your needs\n\nIf you have any questions, feedback, or need modifications to the demo, please do not hesitate to reach out. We are here to help!\n\nBest regards,\nCode.Serve Team\nVisit our website: https://codeservecommunity.netlify.app';
    
    console.log('Calling MailApp.sendEmail...');
    console.log('Subject: ' + subject);
    
    MailApp.sendEmail({
      to: email,
      subject: subject,
      body: plainText,
      htmlBody: htmlBody,
      name: 'Code.Serve'
    });
    
    console.log('✅ Demo ready email sent to: ' + email);
    return {
      success: true,
      message: 'Demo ready notification email sent'
    };
  } catch (error) {
    console.log('❌ Error sending demo ready email: ' + error.toString());
    return {
      success: false,
      message: 'Failed to send email: ' + error.toString()
    };
  }
}

// Trigger function - runs when sheet is edited
function onEdit(e) {
  try {
    console.log('=== SHEET EDIT DETECTED ===');
    
    // Check if event object exists
    if (!e || !e.range) {
      console.log('No event object, manual trigger');
      return;
    }
    
    const sheet = e.source.getActiveSheet();
    const range = e.range;
    
    // Check if this is the DemoCustomers sheet
    if (sheet.getName() !== SHEET_NAME) {
      console.log('Edit was not in DemoCustomers sheet, ignoring');
      return;
    }
    
    // Check if the edited column is DemoStatus (column C, index 3)
    const editedColumn = range.getColumn();
    if (editedColumn !== 3) {
      console.log('Edit was not in DemoStatus column, ignoring');
      return;
    }
    
    // Get the new value
    const newValue = range.getValue();
    console.log('DemoStatus changed to:', newValue);
    
    // Check if status changed to "done"
    if (newValue && newValue.toString().toLowerCase() === 'done') {
      const editedRow = range.getRow();
      console.log('Status changed to DONE in row:', editedRow);
      
      // Get customer data from the row
      const rowData = sheet.getRange(editedRow, 1, 1, 8).getValues()[0];
      const email = rowData[0]; // Column A
      const demoLink = rowData[1]; // Column B
      const businessName = rowData[4]; // Column E
      
      console.log('Customer email:', email);
      console.log('Demo link:', demoLink);
      console.log('Business name:', businessName);
      
      // Send demo ready email
      if (email && demoLink) {
        console.log('Sending demo ready email...');
        const result = sendDemoReadyEmailBackend(email, demoLink);
        
        if (result.success) {
          console.log('✅ Demo ready email sent successfully!');
        } else {
          console.log('❌ Failed to send demo ready email:', result.message);
        }
      } else {
        console.log('❌ Missing email or demo link, cannot send email');
      }
    }
    
  } catch (error) {
    console.log('❌ Error in onEdit trigger:', error.toString());
  }
}

// Manual function to send demo ready email (for testing)
function sendDemoReadyManual() {
  // Test with a specific row
  const sheet = getSheet();
  if (!sheet) {
    console.log('Could not access sheet');
    return;
  }
  
  // Get the last row (most recent customer)
  const lastRow = sheet.getLastRow();
  const rowData = sheet.getRange(lastRow, 1, 1, 8).getValues()[0];
  
  const email = rowData[0];
  const demoLink = rowData[1];
  const status = rowData[2];
  
  console.log('Testing with row:', lastRow);
  console.log('Email:', email);
  console.log('Demo link:', demoLink);
  console.log('Status:', status);
  
  if (status && status.toString().toLowerCase() === 'done') {
    const result = sendDemoReadyEmailBackend(email, demoLink);
    console.log('Result:', result);
  } else {
    console.log('Status is not "done", change it to "done" first');
  }
}

// Check email quota
function checkEmailQuota() {
  const quota = MailApp.getRemainingDailyQuota();
  console.log('Remaining email quota today: ' + quota);
  console.log('You can send ' + quota + ' more emails today');
  return quota;
}

// Test sheet access
function testSheetAccess() {
  console.log('=== TESTING SHEET ACCESS ===');
  console.log('Sheet ID: ' + SHEET_ID);
  console.log('Sheet Name: ' + SHEET_NAME);
  
  const sheet = getSheet();
  
  if (!sheet) {
    console.log('❌ Could not access sheet!');
    console.log('Make sure:');
    console.log('1. Sheet ID is correct: ' + SHEET_ID);
    console.log('2. Sheet name exists: ' + SHEET_NAME);
    return false;
  }
  
  console.log('✅ Sheet accessed successfully!');
  console.log('Sheet name: ' + sheet.getName());
  console.log('Last row: ' + sheet.getLastRow());
  console.log('Last column: ' + sheet.getLastColumn());
  
  // Try to read first row (headers)
  const headers = sheet.getRange(1, 1, 1, 8).getValues()[0];
  console.log('Headers: ' + headers.join(', '));
  
  return true;
}

// Test saving a customer
function testSaveCustomer() {
  console.log('=== TESTING SAVE CUSTOMER ===');
  
  const testData = {
    email: 'test@example.com',
    businessName: 'Test Business',
    phone: '1234567890',
    demoRequirements: 'Test requirements',
    address: 'Test address'
  };
  
  console.log('Saving test customer:', testData);
  
  const result = saveCustomer(
    testData.email,
    testData.businessName,
    testData.phone,
    testData.demoRequirements,
    testData.address
  );
  
  console.log('Save result:', JSON.stringify(result, null, 2));
  
  if (result.success) {
    console.log('✅ Customer saved successfully!');
    console.log('Demo number:', result.demoNumber);
    console.log('Check your Google Sheet - new row should be added');
  } else {
    console.log('❌ Failed to save customer:', result.message);
  }
  
  return result;
}

// Test email to specific address
function testEmailToAddress() {
  const testEmail = 'codeserve.contact@gmail.com'; // Change this to test different email
  const testLink = 'https://demo.netlify.com';
  
  console.log('Sending test email to: ' + testEmail);
  const result = sendDemoReadyEmailBackend(testEmail, testLink);
  console.log('Result:', result);
  
  if (result.success) {
    console.log('✅ Check ' + testEmail + ' inbox and spam folder');
  }
}

// Main doGet function to handle requests
function doGet(e) {
  Logger.log('=== DOGET CALLED ===');
  Logger.log('Event object exists: ' + (e !== null && e !== undefined));
  Logger.log('Parameter object exists: ' + (e && e.parameter !== null && e.parameter !== undefined));
  Logger.log('All parameters: ' + JSON.stringify(e ? e.parameter : 'NO EVENT'));
  Logger.log('Action: ' + (e && e.parameter ? e.parameter.action : 'NO ACTION'));
  Logger.log('Email: ' + (e && e.parameter ? e.parameter.email : 'NO EMAIL'));
  Logger.log('BusinessName: ' + (e && e.parameter ? e.parameter.businessName : 'NO BUSINESS'));
  
  try {
    if (!e || !e.parameter) {
      return ContentService
        .createTextOutput(JSON.stringify({
          success: false,
          message: 'No parameters received'
        }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    
    const action = e.parameter.action;
    
    let response;
    
    switch (action) {
      case 'healthCheck':
        response = healthCheck();
        break;
        
      case 'listSheets':
        response = listSheets();
        break;
        
      case 'getLastDemoNumber':
        response = getLastDemoNumber();
        break;
        
      case 'verifyDemoLink':
        response = verifyDemoLink(
          e.parameter.email,
          e.parameter.demoLink
        );
        break;
        
      case 'saveCustomer':
        response = saveCustomer(
          e.parameter.email,
          e.parameter.businessName,
          e.parameter.phone,
          e.parameter.demoRequirements,
          e.parameter.address
        );
        break;
        
      case 'checkCustomer':
        response = checkCustomer(e.parameter.email, e.parameter.phone);
        break;
        
      case 'updateCustomer':
        response = updateCustomer(
          e.parameter.email,
          e.parameter.demoLink,
          e.parameter.demoStatus
        );
        break;
        
      case 'sendDemoRequestEmail':
        response = sendDemoRequestEmailBackend(
          e.parameter.email,
          e.parameter.businessName,
          e.parameter.phone,
          e.parameter.demoRequirements
        );
        break;
        
      case 'sendDemoReadyEmail':
        response = sendDemoReadyEmailBackend(
          e.parameter.email,
          e.parameter.demoLink
        );
        break;
        
      default:
        response = {
          success: false,
          message: 'Unknown action: ' + action
        };
    }
    
    // Return as JSON with CORS headers
    return ContentService
      .createTextOutput(JSON.stringify(response))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    Logger.log('Error in doGet:', error);
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        message: 'Server error: ' + error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
