5. The app will open in your browser.

## Important Notes:
- This is a **local prototype** using mock data only (via Faker). No real web scraping or LinkedIn integration.
- For sending real emails with Gmail: Enable 2-Step Verification in your Google Account, then generate a 16-character **App Password** (not your regular password). Use that in the SMTP settings.
- Always comply with CAN-SPAM, GDPR, and anti-spam laws. Only email people who have given you permission.
- Emails are sent directly via SMTP — test with "Test Email" first.
- Campaign logs are saved to `sent_campaigns.csv` in the app folder.

Enjoy responsible outreach! 🚀
"""

import streamlit as st
import pandas as pd
from faker import Faker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json
import os
from datetime import datetime
import random

# Initialize session state
if "leads" not in st.session_state:
 st.session_state.leads = pd.DataFrame()
if "selected_leads" not in st.session_state:
 st.session_state.selected_leads = pd.DataFrame()
if "campaign_log" not in st.session_state:
 st.session_state.campaign_log = pd.DataFrame(columns=["timestamp", "email", "status", "message"])

fake = Faker()

# Page config
st.set_page_config(
 page_title="LeadScope AI",
 page_icon="🔍",
 layout="wide",
 initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
 st.title("🔍 LeadScope AI")
 st.caption("Local Leadscope Clone")
 
 st.markdown("### Quick Start")
 st.markdown("""
 1. **Generate Leads** tab → Set criteria  
 2. Review & select leads  
 3. Craft personalized message  
 4. Configure SMTP & send  
 """)
 
 # Dark/Light mode (Streamlit handles this automatically in recent versions)
 st.markdown("---")
 
 # Save/Load Campaign
 if st.button("💾 Save Campaign", use_container_width=True):
     if not st.session_state.leads.empty:
         campaign_data = {
             "leads": st.session_state.leads.to_dict(orient="records"),
             "subject": st.session_state.get("email_subject", ""),
             "body": st.session_state.get("email_body", ""),
             "timestamp": datetime.now().isoformat()
         }
         with open("leadscope_campaign.json", "w") as f:
             json.dump(campaign_data, f, indent=2)
         st.success("Campaign saved to leadscope_campaign.json")
     else:
         st.warning("No leads to save yet.")
 
 if st.button("📂 Load Campaign", use_container_width=True):
     if os.path.exists("leadscope_campaign.json"):
         try:
             with open("leadscope_campaign.json", "r") as f:
                 data = json.load(f)
             st.session_state.leads = pd.DataFrame(data["leads"])
             st.success("Campaign loaded successfully!")
             st.rerun()
         except Exception as e:
             st.error(f"Failed to load: {e}")
     else:
         st.warning("No saved campaign found.")
 
 st.markdown("---")
 st.markdown("### About")
 [st.info](http://st.info)("""
 **Local prototype only**  
 Mock data generated with Faker.  
 No real data scraping.  
 For educational & responsible use.
 """)

# Main app title
st.title("🔍 LeadScope AI")
st.subheader("All-in-One B2B Lead Generation & Email Outreach")
st.markdown("---")

# Use tabs for unified interface
tab1, tab2, tab3, tab4 = st.tabs([
 "📊 Lead Generation",
 "📋 Leads List",
 "✉️ Message & Personalization",
 "🚀 Email Campaign"
])

# Tab 1: Lead Generation
with tab1:
 st.header("Generate Leads")
 
 col1, col2 = st.columns([2, 1])
 
 with col1:
     industries = ["SaaS", "E-commerce", "Manufacturing", "Healthcare", "Finance", "Real Estate", 
                  "Education", "Marketing", "Consulting", "Technology"]
     selected_industries = st.multiselect(
         "Company Industries",
         options=industries,
         default=["SaaS", "Technology"],
         help="Select one or more industries. You can type custom ones too."
     )
     
     location_col1, location_col2, location_col3 = st.columns(3)
     with location_col1:
         country = st.text_input("Country", value="United States")
     with location_col2:
         state = st.text_input("State/Province", value="California")
     with location_col3:
         city = st.text_input("City", value="San Francisco")
 
 with col2:
     company_size = st.selectbox(
         "Company Size (Employees)",
         options=["1-10", "11-50", "51-200", "201-1000", "1000+"],
         index=2
     )
     
     revenue = st.text_input("Annual Revenue Range (optional)", placeholder="e.g. $1M - $10M")
     
     num_leads = st.slider("Number of Leads to Generate", min_value=10, max_value=500, value=50, step=10)
 
 job_titles_input = st.text_input(
     "Target Job Titles / Keywords (comma-separated)",
     value="CEO, Founder, Head of Sales, VP Marketing",
     help="e.g. CEO, Founder, Head of Sales"
 )
 target_job_titles = [t.strip() for t in job_titles_input.split(",") if t.strip()]
 
 if st.button("🚀 Generate Leads", type="primary", use_container_width=True):
     with st.spinner("Generating realistic mock leads..."):
         leads_list = []
         for _ in range(num_leads):
             first_name = fake.first_name()
             last_name = fake.last_name()
             job_title = random.choice(target_job_titles) if target_job_titles else fake.job()
             
             company_name = fake.company()
             # Make email based on company
             domain = company_name.lower().replace(" ", "").replace(",", "").replace(".", "")[:15] + ".com"
             email = f"{first_name.lower()}.{last_name.lower()}@{domain}"
             
             linkedin = f"[https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}-{fake.random_int(100,999](https://linkedin.com/in/%7Bfirst_name.lower()%7D-%7Blast_name.lower()%7D-%7Bfake.random_int(100,999))}"
             
             industry = random.choice(selected_industries) if selected_industries else "Technology"
             
             leads_list.append({
                 "first_name": first_name,
                 "last_name": last_name,
                 "job_title": job_title,
                 "company_name": company_name,
                 "industry": industry,
                 "city": city or fake.city(),
                 "state": state or fake.state(),
                 "country": country or "United States",
                 "email": email,
                 "linkedin_url": linkedin,
                 "company_size": company_size
             })
         
         st.session_state.leads = pd.DataFrame(leads_list)
         st.success(f"✅ Generated {len(leads_list)} realistic leads!")
         st.rerun()

# Tab 2: Leads List
with tab2:
 st.header("Leads List")
 
 if st.session_state.leads.empty:
     [st.info](http://st.info)("No leads generated yet. Go to the **Lead Generation** tab to create some.")
 else:
     # Add selection column for data_editor (workaround for older Streamlit versions)
     df_display = st.session_state.leads.copy()
     if "Select" not in df_display.columns:
         df_display.insert(0, "Select", False)
     
     st.subheader("Editable Leads Table")
     edited_df = st.data_editor(
         df_display,
         hide_index=True,
         use_container_width=True,
         column_config={
             "Select": st.column_config.CheckboxColumn(
                 "Select",
                 help="Check to include in campaign",
                 default=False,
             ),
             "email": st.column_config.TextColumn("Email", disabled=False),
             "linkedin_url": st.column_config.LinkColumn("LinkedIn", disabled=True),
         },
         num_rows="dynamic"
     )
     
     # Update session leads from edited
     if not edited_df.equals(df_display):
         # Remove select column and update main df
         updated_leads = edited_df.drop(columns=["Select"], errors="ignore")
         st.session_state.leads = updated_leads
     
     # Get selected leads
     selected_mask = edited_df["Select"] == True if "Select" in edited_df.columns else pd.Series(False, index=edited_df.index)
     st.session_state.selected_leads = edited_df[selected_mask].drop(columns=["Select"], errors="ignore")
     
     col_a, col_b, col_c = st.columns(3)
     with col_a:
         if st.button("Select All", use_container_width=True):
             # This is a simple way; full select all needs more session handling
             st.warning("For full 'Select All', check boxes manually or use the next button to export selected.")
     
     with col_b:
         if st.button("Export Selected to CSV", use_container_width=True):
             if not st.session_state.selected_leads.empty:
                 csv = st.session_state.selected_leads.to_csv(index=False)
                 st.download_button(
                     "📥 Download Selected Leads CSV",
                     csv,
                     file_name=f"leads_{datetime.now().strftime('%Y%m%d')}.csv",
                     mime="text/csv"
                 )
             else:
                 st.warning("No leads selected.")
     
     with col_c:
         uploaded_file = st.file_uploader("Upload your own leads CSV", type=["csv"])
         if uploaded_file:
             try:
                 uploaded_df = pd.read_csv(uploaded_file)
                 # Basic column mapping
                 required_cols = ["first_name", "last_name", "email", "company_name"]
                 if all(col in uploaded_df.columns for col in required_cols):
                     st.session_state.leads = pd.concat([st.session_state.leads, uploaded_df], ignore_index=True).drop_duplicates(subset=["email"])
                     st.success(f"Loaded {len(uploaded_df)} leads from CSV!")
                     st.rerun()
                 else:
                     st.error(f"CSV must contain at least: {required_cols}")
             except Exception as e:
                 st.error(f"Error reading CSV: {e}")
     
     st.caption(f"Total Leads: {len(st.session_state.leads)} | Selected: {len(st.session_state.selected_leads)}")

# Tab 3: Message & Personalization
with tab3:
 st.header("Message & Personalization")
 
 if st.session_state.leads.empty:
     st.warning("Generate some leads first!")
 else:
     st.subheader("Email Template")
     
     email_subject = st.text_input(
         "Email Subject",
         value="Quick question about {{company_name}} growth",
         key="email_subject"
     )
     
     email_body = st.text_area(
         "Email Body (Markdown supported)",
         value="""Hi {{first_name}},

I noticed {{company_name}} is doing great work in {{industry}}.

Would you be open to a quick 10-minute call next week to discuss how we help similar companies?

Best regards,
Your Name
Your Company""",
         height=300,
         key="email_body"
     )
     
     st.markdown("**Supported Personalization Variables:**")
     vars_list = ["{{first_name}}", "{{last_name}}", "{{job_title}}", "{{company_name}}", "{{industry}}", "{{city}}"]
     st.code(" ".join(vars_list))
     
     # Live Preview
     st.subheader("Live Preview")
     preview_leads = st.session_state.selected_leads if not st.session_state.selected_leads.empty else st.session_state.leads.head(3)
     
     if not preview_leads.empty:
         for idx, row in preview_leads.iterrows():
             with st.expander(f"Preview for {row.get('first_name', '')} at {row.get('company_name', '')}", expanded=idx==0):
                 subject_preview = email_subject
                 body_preview = email_body
                 
                 for var, col in [
                     ("{{first_name}}", "first_name"),
                     ("{{last_name}}", "last_name"),
                     ("{{job_title}}", "job_title"),
                     ("{{company_name}}", "company_name"),
                     ("{{industry}}", "industry"),
                     ("{{city}}", "city")
                 ]:
                     if var in subject_preview or var in body_preview:
                         value = str(row.get(col, ""))
                         subject_preview = subject_preview.replace(var, value)
                         body_preview = body_preview.replace(var, value)
                 
                 st.markdown(f"**Subject:** {subject_preview}")
                 st.markdown("**Body:**")
                 st.markdown(body_preview)
     else:
         [st.info](http://st.info)("Select leads in the Leads List tab to see personalized previews.")

# Tab 4: Email Campaign
with tab4:
 st.header("Email Campaign")
 
 if st.session_state.selected_leads.empty and not st.session_state.leads.empty:
     st.warning("No leads selected yet. Go to **Leads List** and check some rows.")
 
 num_to_send = len(st.session_state.selected_leads) if not st.session_state.selected_leads.empty else 0
 st.metric("Ready to Send", f"{num_to_send} leads")
 
 with st.expander("📧 SMTP Settings", expanded=True):
     smtp_provider = st.selectbox("Provider", ["Gmail", "Outlook", "Custom SMTP"])
     
     if smtp_provider == "Gmail":
         smtp_host = "[smtp.gmail.com](http://smtp.gmail.com)"
         smtp_port = 587
         use_tls = True
     elif smtp_provider == "Outlook":
         smtp_host = "[smtp.office365.com](http://smtp.office365.com)"
         smtp_port = 587
         use_tls = True
     else:
         smtp_host = st.text_input("SMTP Host", "[smtp.example.com](http://smtp.example.com)")
         smtp_port = st.number_input("SMTP Port", value=587)
         use_tls = st.toggle("Use TLS", value=True)
     
     sender_email = st.text_input("Sender Email", placeholder="[yourname@gmail.com](mailto:yourname@gmail.com)")
     sender_name = st.text_input("Sender Name", "Your Name")
     reply_to = st.text_input("Reply-To (optional)", value=sender_email)
     
     smtp_password = st.text_input("SMTP Password / App Password", type="password", help="For Gmail use App Password, not regular password.")
 
 delay_seconds = st.slider("Delay between emails (seconds)", min_value=1, max_value=30, value=5)
 
 # Test Email
 if st.button("📨 Send Test Email", use_container_width=True):
     if not sender_email or not smtp_password:
         st.error("Please fill in SMTP credentials.")
     elif st.session_state.leads.empty:
         st.error("No leads available.")
     else:
         test_lead = st.session_state.leads.iloc[0]
         try:
             # Personalize
             subject = st.session_state.get("email_subject", "Test Email")
             body = st.session_state.get("email_body", "This is a test.")
             
             for var, col in [
                 ("{{first_name}}", "first_name"), ("{{last_name}}", "last_name"),
                 ("{{job_title}}", "job_title"), ("{{company_name}}", "company_name"),
                 ("{{industry}}", "industry"), ("{{city}}", "city")
             ]:
                 subject = subject.replace(var, str(test_lead.get(col, "")))
                 body = body.replace(var, str(test_lead.get(col, "")))
             
             msg = MIMEMultipart()
             msg['From'] = f"{sender_name} <{sender_email}>"
             msg['To'] = test_lead["email"]
             msg['Subject'] = subject
             if reply_to:
                 msg['Reply-To'] = reply_to
             msg.attach(MIMEText(body, 'plain'))
             
             with smtplib.SMTP(smtp_host, smtp_port) as server:
                 if use_tls:
                     server.starttls()
                 server.login(sender_email, smtp_password)
                 server.sendmail(sender_email, test_lead["email"], msg.as_string())
             
             st.success(f"✅ Test email sent to {test_lead['email']}")
         except Exception as e:
             st.error(f"❌ Test failed: {str(e)}")
 
 # Safety Warning & Send All
 if num_to_send > 0 and st.button("🚀 Send to All Selected Leads", type="primary", use_container_width=True):
     if not sender_email or not smtp_password:
         st.error("SMTP credentials required.")
     else:
         st.warning("""
         **⚠️ Legal & Safety Warning**  
         This tool is for legitimate outreach only.  
         You must comply with CAN-SPAM, GDPR, and all applicable laws.  
         Only email prospects you have permission to contact.  
         """)
         
         if st.checkbox("I understand and take full responsibility", value=False):
             with st.spinner("Sending campaign..."):
                 progress_bar = st.progress(0)
                 log_entries = []
                 
                 selected = st.session_state.selected_leads.copy()
                 
                 for i, (_, row) in enumerate(selected.iterrows()):
                     try:
                         # Personalize
                         subject = st.session_state.get("email_subject", "")
                         body = st.session_state.get("email_body", "")
                         
                         for var, col in [
                             ("{{first_name}}", "first_name"), ("{{last_name}}", "last_name"),
                             ("{{job_title}}", "job_title"), ("{{company_name}}", "company_name"),
                             ("{{industry}}", "industry"), ("{{city}}", "city")
                         ]:
                             if var in subject or var in body:
                                 value = str(row.get(col, ""))
                                 subject = subject.replace(var, value)
                                 body = body.replace(var, value)
                         
                         msg = MIMEMultipart()
                         msg['From'] = f"{sender_name} <{sender_email}>"
                         msg['To'] = row["email"]
                         msg['Subject'] = subject
                         if reply_to:
                             msg['Reply-To'] = reply_to
                         msg.attach(MIMEText(body, 'plain'))
                         
                         with smtplib.SMTP(smtp_host, smtp_port) as server:
                             if use_tls:
                                 server.starttls()
                             server.login(sender_email, smtp_password)
                             server.sendmail(sender_email, row["email"], msg.as_string())
                         
                         status = "Success"
                         log_entries.append({
                             "timestamp": datetime.now().isoformat(),
                             "email": row["email"],
                             "status": status,
                             "message": "Sent successfully"
                         })
                         
                     except Exception as e:
                         status = "Failed"
                         log_entries.append({
                             "timestamp": datetime.now().isoformat(),
                             "email": row["email"],
                             "status": status,
                             "message": str(e)
                         })
                     
                     # Update progress
                     progress_bar.progress((i + 1) / len(selected))
                     
                     # Delay
                     if i < len(selected) - 1:
                         time.sleep(delay_seconds)
                 
                 # Save log
                 new_log = pd.DataFrame(log_entries)
                 st.session_state.campaign_log = pd.concat([st.session_state.campaign_log, new_log], ignore_index=True)
                 st.session_state.campaign_log.to_csv("sent_campaigns.csv", index=False)
                 
                 st.success(f"✅ Campaign completed! {len([l for l in log_entries if l['status']=='Success'])} successful sends.")
                 st.dataframe(st.session_state.campaign_log.tail(10), use_container_width=True)
         else:
             [st.info](http://st.info)("Please acknowledge the safety warning to proceed.")

# Footer
st.markdown("---")
st.caption("LeadScope AI • Local Prototype • Built for responsible B2B outreach")
