Overview
---------
The Odoo `Complaint Management` Module is a custom module for the Odoo website platform that allows customers to submit complaints through the website.

Features
---------
* Website Form: Customers can submit the complaint through website.
* Email Notifications: Email notifications will send when submitting the complaints and closing the complaints.
* Work Order Report: System users can download complaint work order report(DIN5008)

Installation
-------------
Follow these steps to install the Odoo `Complaint Management` Module:

* Download the module ZIP file from the provided source.
* Extract the ZIP file to your Odoo custom addons directory and restart the Odoo service.
* Log in to your Odoo system as an administrator.
* Go to the `Apps` module.
* Click on the `Update Apps List` menu.  
* In the search bar, type `Complaint Management` and press Enter.
* Click on the `Install` button next to the module to install it.

Configuration
-------------
Once the module is installed, you can configure it to website complaint form:

Configure Default Responsible User
* Go to the `Website` module in Odoo.
* Click on the Configurations and Setting.
* Select a `Responsible Default User` in `Complaints Info` section.

Configure Complaint Types
* Go to the `Website` module in Odoo.
* Click on the Complaint menu item and sect the Complaint Type sub menu item.
* Click on the new button and create the complaint type.

Configure DIN5008 report layout
* Go to the `Setting` and click on the General Setting
* Click on the configure document layout button under Document Layout.
* Select the `DIN 5008` as the Layout.
* Select the `European A4 for DIN5008 Type A` as the paper format

Usage
-----
With the Odoo `Complaint Management` Module installed and configured, customers can submit complaints through the website:

Frontend Workflow
* Visit your website.
* Click on the `Complaint` menu and it will open the website form.
* These fields are mandatory, `Your Name`, `Your Email`, `Type`, `Description`.
* User can fill the address details if required.
* If there's any document or images related to the complaint, user can attach those documents in `Attachment` section.
* After click on the `Submit` button, it will generate a complaint.

Backend Workflow
* To Create the `Complaint Type`, Go to Website -> Complaints -> Complaint Types
* Add Type name and select is it a question or not.
* To view and classify the complaints, Go to Website -> Complaints -> Complaints and it will open list of complaints created through website.
* To take an action, user need to open the complaint form view and there will be multiple action buttons,
  - Review - For classified by the customer service representative
  - In Progress - For addressed with a action plan
  - Solve - For mark as `Solved`, if it's question type complaint, user can provide an answer and mark as `Solved'. But if it's a normal complaint it's mandatory to put the action plan before close. 
  - Dropped - For mark as `Dropped`, if it's not a valid complaint, user can drop it and close.
* To download the `Work Order Report`, Open a complaint form view -> Click on the action icon -> Select `Complaint Work Order Report` option and it will download the pdf report.

Compatibility
-------------
This module is compatible with Odoo version `17.0` enterprise and community editions.