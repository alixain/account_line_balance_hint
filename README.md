# Journal Line Balance Hint

## Overview
**Journal Line Balance Hint** is an Odoo 16 module that enhances the user experience when working with journal entry lines. It displays the current balance of an account or a partner as a hint directly when selecting them on journal entry lines, allowing for better visibility and quicker decision-making during data entry.

## Features
- **Account Balance Hint**: Instantly view the current balance of the selected account on journal lines.
- **Partner Balance Hint**: Quickly see the partner's outstanding balance when assigning a partner to a journal item.
- Seamless integration with the default Odoo Accounting application.

## Requirements
- **Odoo Version**: 16.0
- **Dependencies**: `account` (Odoo Accounting)

## Installation
1. Place the `account_line_balance_hint` folder into your Odoo `addons` directory.
2. Restart the Odoo service.
3. Turn on **Developer Mode** in your Odoo instance.
4. Navigate to **Apps** > **Update Apps List** and click on "Update".
5. Search for "Journal Line Balance Hint" in the Apps list.
6. Click **Install**.

## Usage
Once the module is installed, there is no additional configuration required. 
1. Navigate to **Accounting** > **Accounting** > **Journal Entries** (or anywhere you can edit journal items).
2. Create or edit a journal entry.
3. In the journal items list, click on the **Account** or **Partner** fields. 
4. The remaining/current balance will be shown as a hint/badge directly on the interface, giving immediate context of the financial position.

## Author
* **Aspire Analytica** - [Website](https://www.aspireanalytica.com)

## License
This module is licensed under the LGPL-3 License. See the `__manifest__.py` file for more details.
