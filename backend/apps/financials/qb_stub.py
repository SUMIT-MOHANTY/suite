import logging

logger = logging.getLogger(__name__)

class QBClient:
    def __init__(self, api_token: str, sandbox: bool = None):
        self.api_token = api_token
        self.sandbox = sandbox if sandbox is not None else self._get_flag()
    
    def _get_flag(self):
        import os
        return os.getenv('QB_SANDBOX', 'true').lower() == 'true'
    
    def create_invoice(self, invoice):
        if self.sandbox:
            logger.info('QB sync disabled - skipping invoice sync')
            return {'soap_id': None, 'synced': False}
        
        # Real QB integration would go here
        logger.info('QB sync not enabled')
        return {'soap_id': None, 'synced': False}
    
    def create_statement(self, statement):
        if self.sandbox:
            logger.info('QB sync disabled - skipping statement sync')
            return {'soap_id': None, 'synced': False}
        
        # Real QB integration would go here
        logger.info('QB sync not enabled')
        return {'soap_id': None, 'synced': False}
