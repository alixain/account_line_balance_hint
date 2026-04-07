from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    balance_hint = fields.Char(
        string="Balance",
        compute='_compute_balance_hint',
        store=False,
    )

    @api.depends('account_id', 'partner_id', 'company_id')
    def _compute_balance_hint(self):
        """
        Shows partner balance (if partner set) or account balance (if only account set).
        Uses SQL for performance. Balance = sum(debit) - sum(credit) on posted moves.
        """
        for line in self:
            company = line.company_id or self.env.company
            currency = company.currency_id

            if line.partner_id and line.account_id:
                # Partner balance on this specific account
                self._cr.execute("""
                    SELECT COALESCE(SUM(aml.debit - aml.credit), 0.0)
                    FROM account_move_line aml
                    JOIN account_move am ON am.id = aml.move_id
                    WHERE aml.partner_id = %s
                      AND aml.account_id = %s
                      AND aml.company_id = %s
                      AND am.state = 'posted'
                """, (line.partner_id.id, line.account_id.id, company.id))
                balance = self._cr.fetchone()[0]
                sign = '+' if balance >= 0 else ''
                line.balance_hint = (
                    f"{sign}{currency.symbol} "
                    f"{currency.round(balance):,.2f}"
                )

            elif line.partner_id and not line.account_id:
                # Partner overall balance across all receivable/payable accounts
                self._cr.execute("""
                    SELECT COALESCE(SUM(aml.debit - aml.credit), 0.0)
                    FROM account_move_line aml
                    JOIN account_move am ON am.id = aml.move_id
                    JOIN account_account acc ON acc.id = aml.account_id
                    WHERE aml.partner_id = %s
                      AND aml.company_id = %s
                      AND am.state = 'posted'
                      AND acc.account_type IN (
                          'asset_receivable', 'liability_payable'
                      )
                """, (line.partner_id.id, company.id))
                balance = self._cr.fetchone()[0]
                sign = '+' if balance >= 0 else ''
                line.balance_hint = (
                    f"{sign}{currency.symbol} "
                    f"{currency.round(balance):,.2f}"
                )

            elif line.account_id and not line.partner_id:
                # Account balance (posted moves only)
                self._cr.execute("""
                    SELECT COALESCE(SUM(aml.debit - aml.credit), 0.0)
                    FROM account_move_line aml
                    JOIN account_move am ON am.id = aml.move_id
                    WHERE aml.account_id = %s
                      AND aml.company_id = %s
                      AND am.state = 'posted'
                """, (line.account_id.id, company.id))
                balance = self._cr.fetchone()[0]
                sign = '+' if balance >= 0 else ''
                line.balance_hint = (
                    f"{sign}{currency.symbol} "
                    f"{currency.round(balance):,.2f}"
                )

            else:
                line.balance_hint = False