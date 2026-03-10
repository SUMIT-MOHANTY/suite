from django.db.models import Sum
from .models import Statement, Invoice
from django.utils import timezone
import decimal

class InvoiceService:
    @staticmethod
    def get_balance_forward(policy_id):
        """Calculate outstanding balance for policy"""
        invoices = Invoice.objects.filter(policy_id=policy_id)
        total_paid = invoices.filter(status='paid').aggregate(
            total=Sum('lines__0__amount')
        )['total'] or decimal.Decimal('0.00')
        
        total_invoiced = invoices.exclude(status='cancelled').aggregate(
            total=Sum('lines__0__amount')
        )['total'] or decimal.Decimal('0.00')
        
        return str(total_invoiced - total_paid)

class StatementService:
    @staticmethod
    def generate_annual_statement(captive_id, year):
        """Generate monthly statements for a captive"""
        statements = []
        
        for month in range(1, 13):
            # Get all invoices for this month/year
            invoices = Invoice.objects.filter(
                captive_id=captive_id,
                issued_at__year=year,
                issued_at__month=month
            )
            
            # Aggregate by line type
            lines = {}
            for invoice in invoices:
                for line in invoice.lines:
                    line_type = line['type']
                    amount = decimal.Decimal(line['amount'])
                    
                    if line_type not in lines:
                        lines[line_type] = {
                            'type': line_type,
                            'amount': '0.00',
                            'vat': '0.00'
                        }
                    
                    current_amount = decimal.Decimal(lines[line_type]['amount'])
                    lines[line_type]['amount'] = str(current_amount + amount)
            
            statement, created = Statement.objects.get_or_create(
                captive_id=captive_id,
                year=year,
                month=month,
                defaults={
                    'lines': list(lines.values()),
                    'generated_at': timezone.now()
                }
            )
            
            if not created:
                statement.lines = list(lines.values())
                statement.generated_at = timezone.now()
                statement.save()
            
            statements.append(statement)
        
        return statements
