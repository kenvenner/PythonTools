import kvgmailsend
import unittest

class TestKVGmailSend(unittest.TestCase):

    def testGmailSend_p01_init(self):
        self.assertEqual( kvgmailsend.GmailSend( 'valid@email.com', 'password' )._from, 'valid@email.com')
    def testGmailSend_p02_init_populated(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        self.assertEqual( m._sendfrom, 'valid@email.com')
        self.assertEqual( m._sendpass, 'password')
        self.assertEqual( m._replyto, None)
        self.assertEqual( m._textBody, None)
        self.assertEqual( m._htmlBody, None)
        self.assertEqual( m._subject, '')
        self.assertEqual( m._to, [])
        self.assertEqual( m._cc, [])
        self.assertEqual( m._bcc, [])
        self.assertEqual( m._attach, [])
    def testGmailSend_f01_init_invalid_sendfrom(self):
        with self.assertRaises(Exception) as context:
            m = kvgmailsend.GmailSend( 'invalid.email.com', 'password' )


    def testGmailSend_p01_setSubject(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setSubject('this is my subject')
        self.assertEqual( m._subject, 'this is my subject' )
        
    def testGmailSend_p01_setFrom(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setFrom('new@address.com')
        self.assertEqual( m._from, 'new@address.com' )
        
    def testGmailSend_p01_setReplyTo(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setReplyTo('new@address.com')
        self.assertEqual( m._replyto, 'new@address.com' )
        
    def testGmailSend_p01_addRecipient_none(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipient('valid@address.com')
        self.assertEqual( m._to, ['valid@address.com'] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p02_addRecipient_to(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipient('valid@address.com', 'to')
        self.assertEqual( m._to, ['valid@address.com'] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p03_addRecipient_cc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipient('valid@address.com', 'cc')
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, ['valid@address.com'] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p04_addRecipient_bcc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipient('valid@address.com', 'bcc')
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, ['valid@address.com'] )
        
    def testGmailSend_p01_addRecipients_none(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'])
        self.assertEqual( m._to, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p02_addRecipients_to(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'], 'to')
        self.assertEqual( m._to, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p03_addRecipients_cc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'], 'cc')
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p04_addRecipients_bcc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'], 'bcc')
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, ['valid@address.com','new@address.com'] )

    def testGmailSend_p01_clearRecipients_none(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'])
        m.addRecipients(['valid@address.com','new@address.com'],'cc')
        m.addRecipients(['valid@address.com','new@address.com'],'bcc')
        m.clearRecipients()
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, [] )
    def testGmailSend_p02_clearRecipients_to(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'])
        m.addRecipients(['valid@address.com','new@address.com'],'cc')
        m.addRecipients(['valid@address.com','new@address.com'],'bcc')
        m.clearRecipients('to')
        self.assertEqual( m._to, [] )
        self.assertEqual( m._cc, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._bcc, ['valid@address.com','new@address.com'] )
    def testGmailSend_p03_clearRecipients_cc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'])
        m.addRecipients(['valid@address.com','new@address.com'],'cc')
        m.addRecipients(['valid@address.com','new@address.com'],'bcc')
        m.clearRecipients('cc')
        self.assertEqual( m._to, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._cc, [] )
        self.assertEqual( m._bcc, ['valid@address.com','new@address.com'] )
    def testGmailSend_p04_clearRecipients_bcc(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addRecipients(['valid@address.com','new@address.com'])
        m.addRecipients(['valid@address.com','new@address.com'],'cc')
        m.addRecipients(['valid@address.com','new@address.com'],'bcc')
        m.clearRecipients('bcc')
        self.assertEqual( m._to, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._cc, ['valid@address.com','new@address.com'] )
        self.assertEqual( m._bcc, [] )


    def testGmailSend_p01_setTextBody_value(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        self.assertEqual( m._textBody, 'Field is populated' )
        self.assertEqual( m._htmlBody, None )
    def testGmailSend_p02_setTextBody_None(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody(None)
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, None )

    def testGmailSend_p01_setHtmlBody_value(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setHtmlBody('Field is populated')
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, 'Field is populated' )
    def testGmailSend_p02_setHtmlBody_None(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setHtmlBody(None)
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, None )

    def testGmailSend_p01_clearBody_none(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody()
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, None )
    def testGmailSend_p02_clearBody_text(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('text')
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, 'Field is populated' )
    def testGmailSend_p03_clearBody_plain(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('plain')
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, 'Field is populated' )
    def testGmailSend_p04_clearBody_html(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('html')
        self.assertEqual( m._textBody, 'Field is populated' )
        self.assertEqual( m._htmlBody, None )
    def testGmailSend_p05_clearBody_TEXT(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('TEXT')
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, 'Field is populated' )
    def testGmailSend_p06_clearBody_PLAIN(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('PLAIN')
        self.assertEqual( m._textBody, None )
        self.assertEqual( m._htmlBody, 'Field is populated' )
    def testGmailSend_p07_clearBody_HTML(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('HTML')
        self.assertEqual( m._textBody, 'Field is populated' )
        self.assertEqual( m._htmlBody, None )
    def testGmailSend_p08_clearBody_invalid_value(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.setTextBody('Field is populated')
        m.setHtmlBody('Field is populated')
        m.clearBody('invalid')
        self.assertEqual( m._textBody, 'Field is populated' )
        self.assertEqual( m._htmlBody, 'Field is populated' )
        
    def testGmailSend_p01_addAttachment_fname_none(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addAttachment( None, None )
        self.assertEqual( m._attach, [] )
    def testGmailSend_p02_addAttachment_fname_no_attachname(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addAttachment( 'ken.txt', None )
        self.assertEqual( m._attach, [('ken.txt',None)] )
    def testGmailSend_p03_addAttachment_fname_and_attachname(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addAttachment( 'ken.txt', 'ken.txt' )
        self.assertEqual( m._attach, [('ken.txt', 'ken.txt')] )
        

    def testGmailSend_p01_clearAttachments_empty(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.clearAttachments()
        self.assertEqual( m._attach, [] )
    def testGmailSend_p02_clearAttachments_has_values(self):
        m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
        m.addAttachment( 'ken.txt', 'ken.txt' )
        m.addAttachment( 'ken2.txt', 'ken2.txt' )
        m.clearAttachments()
        self.assertEqual( m._attach, [] )
        
    def testGmailSend_f01_send_bodys_none(self):
        with self.assertRaises(Exception) as context:
            m = kvgmailsend.GmailSend( 'valie@email.com', 'password' )
            m.send()
    def testGmailSend_f01_send_no_recipient(self):
        with self.assertRaises(Exception) as context:
            m = kvgmailsend.GmailSend( 'valid@email.com', 'password' )
            m.setTextBody('Field is populated')
            m.send()
        
if __name__ == '__main__':
    unittest.main()
