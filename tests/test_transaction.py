import base
import unittest
from dnf.yum.constants import *

from dnf.yum.transactioninfo import TransactionData

class TransactionDataTests(unittest.TestCase):
    ''' Test cases for yum.transactioninfo.TransactionData'''

    def setUp(self):
        self.tsInfo = TransactionData()
        self.pkgs = base.mock_packages()

    def testLenght(self):
        ''' test __len__ method '''
        self.tsInfo.addInstall(self.pkgs[0])
        self.tsInfo.addUpdate(self.pkgs[2], self.pkgs[1])
        self.assertEqual(len(self.tsInfo),3)

    def testAddTheSameTwice(self):
        ''' test add the same twice '''
        first = self.tsInfo.addInstall(self.pkgs[0])
        self.tsInfo.addInstall(self.pkgs[1])
        last = self.tsInfo.addInstall(self.pkgs[0])
        self.assertEqual(len(self.tsInfo),2) # only 2 members
        self.assertEqual(first, last)

    def testExists(self):
        ''' test exists method '''
        self.tsInfo.addInstall(self.pkgs[0])
        self.tsInfo.addInstall(self.pkgs[1])
        assert(self.tsInfo.exists(self.pkgs[0].pkgtup))
        assert(self.tsInfo.exists(self.pkgs[1].pkgtup))
        self.assertFalse(self.tsInfo.exists(self.pkgs[2].pkgtup))

    def testRemove(self):
        ''' test remove from transaction '''
        pkg = self.pkgs[0]
        txmbr = self.tsInfo.addInstall(pkg)
        self.tsInfo.remove(pkg.pkgtup)
        self.assertEqual(len(self.tsInfo), 0)

    def testGetFromTransaction(self):
        ''' test getting from Transaction '''
        self.tsInfo.addInstall(self.pkgs[0])
        txmbr = self.tsInfo.getMembers(self.pkgs[0].pkgtup)[0]
        self.assertEqual(txmbr.output_state, TS_INSTALL)

    def testAddUpdatesAndObsoletes(self):
        ''' test addUpdated,addObsoleted'''
        txmbr1 = self.tsInfo.addUpdated(self.pkgs[1], self.pkgs[2])
        txmbr2 = self.tsInfo.addObsoleted(self.pkgs[3], self.pkgs[4])
        self.assertEqual(len(self.tsInfo), 2)
        txmbr = self.tsInfo.getMembersWithState(output_states=[TS_UPDATED])[0]
        self.assertEqual(txmbr.po, self.pkgs[1])
        txmbr = self.tsInfo.getMembersWithState(output_states=[TS_OBSOLETED])[0]
        self.assertEqual(txmbr.po, self.pkgs[3])

    def testMatchNaevr(self):
        ''' test MatchNaevr '''
        self.tsInfo.addInstall(self.pkgs[0])
        self.tsInfo.addUpdated(self.pkgs[2],self.pkgs[1])
        res = self.tsInfo.matchNaevr(name='withinC')
        self.assertEqual(len(res),1)
        res = self.tsInfo.matchNaevr(arch='noarch')
        self.assertEqual(len(res),2)

    def testgetMembersWithState(self):
        ''' test getMembersWithState'''
        self.tsInfo.addInstall(self.pkgs[0])
        self.tsInfo.addUpdate(self.pkgs[2],self.pkgs[1])
        res = self.tsInfo.getMembersWithState(output_states=[TS_INSTALL,TS_UPDATE])
        self.assertEqual(len(res),2)
        res = self.tsInfo.getMembersWithState(output_states=[TS_UPDATED])
        self.assertEqual(len(res),1)
