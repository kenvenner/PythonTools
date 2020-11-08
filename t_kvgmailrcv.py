import kvgmailrcv
import unittest
import re
import os
import sys
import imaplib

# set the module version number
AppVersion = '1.06'

user = 'wines@vennerllc.com'
password = 'win3s3arch*'

msgPathValid = 'c:/temp/gmail'

folder_msgs = 'Testing'
folder_NoMsgs = 'Invalid'

debug = False

# utility to create/set/update commmand line passed in parameters
def set_argv( position, value ):
    for pos in range(len(sys.argv),position+1):
        sys.argv.append('arg%02d'%pos)
    sys.argv[position] = value
        
# test class
class TestKVGmailRcv(unittest.TestCase):
    def test_GmailImap_init_p01_simple(self):
        imap = kvgmailrcv.GmailImap()
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, None)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
    def test_GmailImap_init_p02_imap_folder_is_None(self):
        imap = kvgmailrcv.GmailImap( {'imap_folder':None} )
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, None)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, None)
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
    def test_GmailImap_init_p03_user_no_password(self):
        imap = kvgmailrcv.GmailImap( {'user':user} )
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, user)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
    def test_GmailImap_init_p04_user_valid_password_verbose(self):
        if debug: print('test_GmailImap_init_p04_user_valid_password_verbose:start')
        # verbose needs to remain True below
        imap = kvgmailrcv.GmailImap( {'verbose' : True, 'user':user, 'password' : password} )
        self.assertEqual(imap.loggedIn, True)
        self.assertEqual(imap.folder_current,'inbox')
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, user)
        self.assertEqual(imap.password, password)
        self.assertEqual(imap.verbose, True)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
        if debug: print('test_GmailImap_init_p04_user_valid_password_verbose:end')
    def test_GmailImap_init_p05_user_valid_password_invalid_folder_verbose(self):
        if debug: print('test_GmailImap_init_p05_user_valid_password_invalid_folder_verbose:start')
        # verbose needs to remain True below
        imap = kvgmailrcv.GmailImap( {'verbose' : True, 'user':user, 'password' : password, 'imap_folder':'invalid'} )
        self.assertEqual(imap.loggedIn, True)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, "select_folder:folder-selection-problem:[b'[NONEXISTENT] Unknown Mailbox: invalid (Failure)']")
        self.assertEqual(imap.user, user)
        self.assertEqual(imap.password, password)
        self.assertEqual(imap.verbose, True)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'invalid')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
        if debug: print('test_GmailImap_init_p05_user_valid_password_invalid_folder_verbose:end')
    def test_GmailImap_init_p06_simple_msgpath_valid(self):
        imap = kvgmailrcv.GmailImap({'msgPath' : msgPathValid})
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, None)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
        self.assertTrue(os.path.exists(os.path.join(msgPathValid, '')))
    def test_GmailImap_init_p07_simple_include_exclude_lists(self):
        imap = kvgmailrcv.GmailImap({ 'fromIncludeEmails' : ['debbie_venner@yahoo.com'],'fromIncludeDomains' : ['vennerllc.com'],'fromExcludeIfNotInclude' : False,'fromExcludeEmails' : ['ken_venner@yahoo.com'],'fromExcludeDomains' : ['spacex.com'] })
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, None)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
        self.assertTrue(os.path.exists(os.path.join(msgPathValid, '')))
        self.assertEqual(imap.fromIncludeEmails, ['debbie_venner@yahoo.com'])
        self.assertEqual(imap.fromIncludeDomains, ['vennerllc.com'])
        self.assertEqual(imap.fromExcludeIfNotInclude, False)
        self.assertEqual(imap.fromExcludeEmails, ['ken_venner@yahoo.com'])
        self.assertEqual(imap.fromExcludeDomains, ['spacex.com'])
    def test_GmailImap_init_p08_simple_include_exclude_strings(self):
        if debug: print('GmailImap_init_p08_simple_include_exclude_strings')
        imap = kvgmailrcv.GmailImap({ 'fromIncludeEmails' : 'debbie_venner@yahoo.com','fromIncludeDomains' : 'vennerllc.com','fromExcludeIfNotInclude' : False,'fromExcludeEmails' : 'ken_venner@yahoo.com','fromExcludeDomains' : 'spacex.com' })
        self.assertEqual(imap.loggedIn, False)
        self.assertEqual(imap.folder_current, None)
        self.assertEqual(imap.mail_ids, [])
        self.assertEqual(imap.msgUID, None)
        self.assertEqual(imap.msgGUID, None)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.user, None)
        self.assertEqual(imap.password, None)
        self.assertEqual(imap.verbose, None)
        self.assertEqual(imap.imap_server, 'imap.gmail.com')
        self.assertEqual(imap.folder_read, 'inbox')
        self.assertEqual(imap.folder_pass, None)
        self.assertEqual(imap.folder_fail, None)
        self.assertTrue(isinstance(imap.imapobj,imaplib.IMAP4_SSL))
        self.assertTrue(os.path.exists(os.path.join(msgPathValid, '')))
        self.assertEqual(imap.fromIncludeEmails, ['debbie_venner@yahoo.com'])
        self.assertEqual(imap.fromIncludeDomains, ['vennerllc.com'])
        self.assertEqual(imap.fromExcludeIfNotInclude, False)
        self.assertEqual(imap.fromExcludeEmails, ['ken_venner@yahoo.com'])
        self.assertEqual(imap.fromExcludeDomains, ['spacex.com'])

    def test_GmailImap_login_p01_select_folder(self):
        if debug: print('test_GmailImap_login_p01_select_folder(self)')
        imap = kvgmailrcv.GmailImap( {'verbose' : False, 'user':user, 'password' : password, 'imap_folder' : folder_msgs} )
        imap.select_folder(folder_msgs)
        if debug: print('imap.mail_ids', imap.mail_ids)
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.folder_read, folder_msgs)
        self.assertNotEqual(imap.mail_ids, [])
        
    def test_GmailImap_login_p01_getNextMessage(self):
        if debug: print('test_GmailImap_login_p01_getNextMessage')
        imap = kvgmailrcv.GmailImap( {'verbose' : False, 'user':user, 'password' : password, 'imap_folder' : folder_msgs} )
        msgNotFound=imap.getNextMessage()
        if msgNotFound:
            print('+'*80)
            print('test_GmailImap_login_p01_getNextMessage')
            print('must put messages in folder:', folder_msgs)
            print('+'*80)
            self.assertFalse( msgNotFound )
        if debug: print('dump the mparse variable')
        kvgmailrcv.dump_mparse(imap.mparse, 'test_GmailImap_login_p01_getNextMessage')
        if debug: print('dump is done')
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.msgParsed, True)
    def test_GmailImap_login_p02_getNextMessage_no_message(self):
        if debug: print('test_GmailImap_login_p02_getNextMessage_no_message')
        imap = kvgmailrcv.GmailImap( {'verbose' : False, 'user':user, 'password' : password, 'imap_folder' : folder_NoMsgs} )
        imap.getNextMessage()
        if debug: print('dump the mparse variable')
        kvgmailrcv.dump_mparse(imap.mparse, 'test_GmailImap_login_p02_getNextMessage_no_message')
        if debug: print('dump is done')
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.msgParsed, False)

    def test_GmailImap_login_p01_getNextMessage_saveMessage(self):
        if debug: print('test_GmailImap_login_p01_getNextMessage')
        imap = kvgmailrcv.GmailImap( {'verbose' : False, 'user':user, 'password' : password, 'imap_folder' : folder_msgs, 'msgPath' : msgPathValid} )
        msgNotFound=imap.getNextMessage()
        if msgNotFound:
            print('+'*80)
            print('test_GmailImap_login_p01_getNextMessage_saveMessage')
            print('must put messages in folder:', folder_msgs)
            print('+'*80)
            self.assertFalse( msgNotFound )
        if debug: print('dump the mparse variable')
        kvgmailrcv.dump_mparse(imap.mparse, 'test_GmailImap_login_p01_getNextMessage')
        if debug: print('dump is done')
        self.assertEqual(imap.errmsg, '')
        self.assertEqual(imap.msgParsed, True)
        # calculate this value
        bodyfilename = ''.join(['msg-', imap.mparse.uid, '.mime'])
        # now save the file
        imap.saveMessage()
        self.assertTrue( os.path.exists(imap.uidPath) )
        self.assertTrue( os.path.exists(os.path.join(imap.uidPath, bodyfilename)) )
        self.assertEqual( imap.msgSaved, True )

    def test_GmailImap_setIncludeExclude_p01_simple(self):
        imap = kvgmailrcv.GmailImap()
        imap.setIncludeExclude(['KEN@vennerllc.com'],['VennerLLC.com'],False,['kvenner@Spacex.com'],['spacex.com'])
        self.assertEqual(imap.fromIncludeEmails, ['ken@vennerllc.com'])
        self.assertEqual(imap.fromIncludeDomains, ['vennerllc.com'])
        self.assertEqual(imap.fromExcludeIfNotInclude, False)
        self.assertEqual(imap.fromExcludeEmails, ['kvenner@spacex.com'])
        self.assertEqual(imap.fromExcludeDomains, ['spacex.com'])
    def test_GmailImap_setIncludeExclude_p02_strings(self):
        imap = kvgmailrcv.GmailImap()
        imap.setIncludeExclude('KEN@vennerllc.com','VennerLLC.com',False,'kvenner@Spacex.com','spacex.com')
        if debug: print('imap.fromIncludeEmails',imap.fromIncludeEmails)
        self.assertEqual(imap.fromIncludeEmails, ['ken@vennerllc.com'])
        self.assertEqual(imap.fromIncludeDomains, ['vennerllc.com'])
        self.assertEqual(imap.fromExcludeIfNotInclude, False)
        self.assertEqual(imap.fromExcludeEmails, ['kvenner@spacex.com'])
        self.assertEqual(imap.fromExcludeDomains, ['spacex.com'])

    def test_GmailImap_excludeMessage_p01_simple(self):
        if debug: print('test_GmailImap_excludeMessage_p01_simple(self)')
        imap = kvgmailrcv.GmailImap( {'verbose' : False, 'user':user, 'password' : password, 'imap_folder' : folder_msgs} )
        imap.setIncludeExclude(['KEN@vennerllc.com'],['VennerLLC.com'],False,['kvenner@Spacex.com'],['spacex.com'])
        msgNotFound=imap.getNextMessage()
        if msgNotFound:
            print('+'*80)
            print('test_GmailImap_excludeMessage_p01_simple')
            print('must put messages in folder:', folder_msgs)
            print('+'*80)
            self.assertFalse( msgNotFound )
        # got a message can continue
        imap.mparse.from_email = 'KEN@vennerllc.com'
        self.assertFalse( imap.excludeMessage() )
        imap.mparse.from_email = 'wines@vennerllc.com'
        self.assertFalse( imap.excludeMessage() )
        imap.mparse.from_email = 'ken@gmail.com'
        self.assertFalse( imap.excludeMessage() )
        imap.mparse.from_email = 'kvenner@spacex.com'
        self.assertTrue( imap.excludeMessage() )
        imap.mparse.from_email = 'gwynne@spacex.com'
        self.assertTrue( imap.excludeMessage() )
    def test_GmailImap_excludeMessage_p02_ExcludeIfNotInclude(self):
        if debug: print('test_GmailImap_excludeMessage_p02_ExcludeIfNotInclude(self)')
        imap = kvgmailrcv.GmailImap( {'verbose' : True, 'user':user, 'password' : password, 'imap_folder' : folder_msgs} )
        imap.setIncludeExclude(['KEN@vennerllc.com'],['VennerLLC.com'],True,['kvenner@Spacex.com'],['spacex.com'])
        msgNotFound=imap.getNextMessage()
        if msgNotFound:
            print('+'*80)
            print('test_GmailImap_excludeMessage_p02_ExcludeIfNotInclude')
            print('must put messages in folder:', folder_msgs)
            print('+'*80)
            self.assertFalse( msgNotFound )
        imap.mparse.from_email = 'KEN@vennerllc.com'
        self.assertFalse( imap.excludeMessage() )
        imap.mparse.from_email = 'wines@vennerllc.com'
        self.assertFalse( imap.excludeMessage() )
        imap.mparse.from_email = 'ken@gmail.com'
        self.assertTrue( imap.excludeMessage() )
        imap.mparse.from_email = 'kvenner@spacex.com'
        self.assertTrue( imap.excludeMessage() )
        imap.mparse.from_email = 'gwynne@spacex.com'
        self.assertTrue( imap.excludeMessage() )

if __name__ == '__main__':
    unittest.main()
    print('assure you have messages in:{}:{}'.format(user,folder_msgs))
        
