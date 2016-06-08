# Didn't find a way to run all the testSuite at once in the main.
# So to run a test enter command : python -m unittest test.<NAME OF THE TEST SUITE>.

import unittest
import sys
import os

from uforgecli.commands.user.user import User_Cmd
from uforgecli.commands.user.user_targetFormat import User_TargetFormat_Cmd
from uforgecli.commands.user.user_targetPlatform import User_TargetPlatform_Cmd
from uforgecli.commands.user.user_quota import User_Quota_Cmd
from uforgecli.commands.user.user_admin import User_Admin_Cmd
from uforgecli.commands.user.user_os import User_Os_Cmd
from uforgecli.commands.user.user_role import User_Role_Cmd
from uforgecli.commands.user.user_api import User_Api_Cmd
from uforgecli.commands.user.user_org import User_Org_Cmd
from uforgecli.commands.entitlement.entitlement import Entitlement_Cmd
from uforgecli.commands.subscription.subscription import Subscription_Cmd
from uforgecli.commands.subscription.subscription_admin import Subscription_Admins
from uforgecli.commands.subscription.subscription_role import Subscription_Roles
from uforgecli.commands.subscription.subscription_targetFormat import Subscription_TargetFormat
from uforgecli.commands.subscription.subscription_targetPlatform import Subscription_TargetPlatform
from uforgecli.commands.subscription.subscription_os import Subscription_Os
from uforgecli.commands.subscription.subscription_quota import Subscription_Quota
from uforgecli.commands.role.role import Role_Cmd
from uforgecli.commands.role.role_entitlement import Role_Entitlement_Cmd
from uforgecli.commands.images.images import Images_Cmd
from uforgecli.commands.org.org import Org_Cmd
from uforgecli.commands.org.org_user import Org_User_Cmd
from uforgecli.commands.org.org_category import Org_Category_Cmd
from uforgecli.commands.org.org_golden import Org_Golden_Cmd
from uforgecli.commands.org.org_os import Org_Os_Cmd
from uforgecli.commands.org.org_repo import Org_Repo_Cmd
from uforgecli.commands.org.org_repo_os import Org_Repo_Os_Cmd
from uforgecli.commands.org.org_format import Org_Format_Cmd
from uforgecli.commands.org.org_targetFormat import Org_TargetFormat_Cmd
from uforgecli.commands.org.org_targetPlatform import Org_TargetPlatform_Cmd
from uforgecli.commands.os.os import Os_Cmd
from uforgecli.commands.os.os_milestone import Os_Milestone_Cmd
from uforgecli.commands.pimages.pimages import Pimages_Cmd
from uforgecli.commands.usergrp.usergrp import Usergrp_Cmd
from uforgecli.commands.usergrp.usergrp_user import UserGroup_User_Cmd
from uforgecli.commands.template.template import Template_Cmd
from uforge.application import Api

if not "TEST_USER" in os.environ or not "TEST_PASSWORD" in os.environ or not "TEST_URL" in os.environ:
        print "Set env variable [TEST_USER], [TEST_PASSWORD], and [TEST_URL]"
        sys.exit(1)

login = os.environ['TEST_USER']
password = os.environ['TEST_PASSWORD']
url = os.environ['TEST_URL']
timeout = 10

def get_targetFormat_id(targetFormat, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        targetFormat.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id

def get_targetPlatform_id(targetPlatform, name):
        stdout = sys.stdout
        sys.stdout = open('stdout_file', 'w')
        targetPlatform.do_list(None)
        sys.stdout = stdout
        cmd = os.popen("cat stdout_file | grep "+name+" | grep -v Getting | cut -d '|' -f2")
        id = cmd.read().rstrip()
        os.remove("stdout_file")
        return id

userTest = 'root'
userTest2 = 'pedro'
userToCreate = 'Frankenstein'
userToCreatePassword = "Hakunamatata"

userTargetFormatsTest = 'VirtualBox Cloudwatt'
userTargetPlatformsTest = 'Amazon Eucalyptus'

subscriptionTest = "test"

userQuotaTypeTest = 'scan'
userQuotaLimitTest = '50'
userRoleTest1 = 'consumer'
userRoleTest2 = 'designer'

userSubscriptionQuotaUpdate = '--name default --type scan --unlimited'

subscriptionAdminTest1 = 'pedro'
subscriptionAdminTest2 = 'root'
subscriptionRoleTest1 = 'consumer'
subscriptionRoleTest2 = 'designer'
subscriptionTargetFormatTest1 = 'Cloudwatt'
subscriptionTargetFormatTest2 = 'ISO'
subscriptionTargetPlatformTest1 = 'Flexiant'
subscriptionTargetPlatformTest2 = 'Nimbula'
subscriptionOsTest1 = 'Windows'

roleRoleTest = 'partner'
roleRoleCreateTest = 'mundir'

roleEntitlementCreateTest1 = 'image_generate'
roleEntitlementCreateTest2 = 'marketplace_access'

imagesIdTest = '5'

orgCreate = 'kangourou'
orgNumber = '01'

orgCategoryTest = 'kangouro'
orgCategoryTestCategoryName = 'pedro'

orgGoldenListArgs = '--arch x86_64 --version 5.6 --name CentOS'
orgGoldenCreate = '--arch x86_64 --version 5.6 --name CentOS --edition Standard --goldenDate 2014-04-28 --goldenName Pedro --language English --type Core'

orgOsCreate = '--arch x86_64 --name CentOS --version 2'
orgOsEnableDisable = '--name CentOS'

orgRepoName = '--name pedro'
orgRepoCreate = orgRepoName + ' --repoUrl http://distros-repository.usharesoft.com/pedro --type RPM'
orgRepoUpdate = '--id 1 --repoUrl http://distros-repository.usharesoft.com/pedro2'

orgRepoOsRepoId = '2'
orgRepoOsAttachDetach = '--arch x86_64 --name CentOS --version 5'

osMilestoneVersion = '--darch x86_64 --dname CentOS --dversion 7'
osMilestoneAddNewName = 'SuperVersion'
osMilestoneAddNewDate = '2015-05-11'
osMilestoneModifyNewDate = '2015-08-27'

usergrpTest = 'userGrpTest'
usergrpTestAddAccounts = 'root'

usergrpTestUserAddAfter = 'dimitri'

orgFormatEnableDisable = 'qcow2 ovf09'
orgTargetFormatCategoryVirtual = 'Virtual'
orgTargetFormatCategoryCloud = 'Cloud'
orgTargetFormatCategoryPhysical = 'Physical'
orgTargetFormatCreateVirtual = 'VirtualBoxTest'
orgTargetFormatCreateCloud = 'OpenstackQcow2Test'
orgTargetFormatCreatePhysical = 'IsoTest'
orgTargetFormatAbiquo = 'Abiquo'
orgTargetFormatsEnableDisable = 'VirtualBox Cloudwatt'
orgTargetPlatformCreateAbiquo = 'AbiquoTest'
orgTargetPlatformOpenStack = 'OpenStack'
orgTargetPlatformsEnableDisable = 'Amazon Eucalyptus'

class UserTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestUser,
                                                     ("test_user_02_targetFormat_disable",
                                                      "test_user_03_targetFormat_enable",
                                                      "test_user_05_targetPlatform_disable",
                                                      "test_user_06_targetPlatform_enable",
                                                      "test_user_08_disable",
                                                      "test_user_07_enable",
                                                      "test_user_13_admin_demote",
                                                      "test_user_14_admin_promote",
                                                      "test_user_16_os_disable",
                                                      "test_user_17_os_enable",
                                                      "test_user_19_role_add",
                                                      "test_user_20_role_remove",
                                                      "test_user_23_org_add",
                                                      "test_user_24_org_remove",
                                                      "test_user_01_targetFormat_list",
                                                      "test_user_04_targetPlatform_list",
                                                      "test_user_09_quota_list",
                                                      "test_user_10_list",
                                                      "test_user_11_info",
                                                      "test_user_12_quota_modify",
                                                      "test_user_15_os_list",
                                                      "test_user_18_role_list",
                                                      "test_user_21_api_quota",
                                                      "test_user_22_org_list",
                                                      "test_user_25_create")))



class TestMotherClass(unittest.TestCase):
        global api
        api = Api(url, username = login, password = password, disable_ssl_certificate_validation = True, timeout = timeout)


class TestUser(TestMotherClass):

        def test_user_01_targetFormat_list(self):
                user_targetFormat = User_TargetFormat_Cmd()
                user_targetFormat.set_globals(api)
                t = user_targetFormat.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_02_targetFormat_disable(self):
                user_targetFormat = User_TargetFormat_Cmd()
                user_targetFormat.set_globals(api)
                t = user_targetFormat.do_disable("--account "+userTest+" --targetFormats "+userTargetFormatsTest)
                self.assertEquals(t,0)

        def test_user_03_targetFormat_enable(self):
                user_targetFormat = User_TargetFormat_Cmd()
                user_targetFormat.set_globals(api)
                t = user_targetFormat.do_enable("--account "+userTest+" --targetFormats "+userTargetFormatsTest)
                self.assertEquals(t,0)

        def test_user_04_targetPlatform_list(self):
                user_targetPlatform = User_TargetPlatform_Cmd()
                user_targetPlatform.set_globals(api)
                t = user_targetPlatform.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_05_targetPlatform_disable(self):
                user_targetPlatform = User_TargetPlatform_Cmd()
                user_targetPlatform.set_globals(api)
                t = user_targetPlatform.do_disable("--account "+userTest+" --targetPlatforms "+userTargetPlatformsTest)
                self.assertEquals(t,0)

        def test_user_06_targetPlatform_enable(self):
                user_targetPlatform = User_TargetPlatform_Cmd()
                user_targetPlatform.set_globals(api)
                t = user_targetPlatform.do_enable("--account "+userTest+" --targetPlatforms "+userTargetPlatformsTest)
                self.assertEquals(t,0)

        def test_user_07_enable(self):
                user = User_Cmd()
                user.set_globals(api)
                t = user.do_enable("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_08_disable(self):
                user = User_Cmd()
                user.set_globals(api)
                t = user.do_disable("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_09_quota_list(self):
                user_quota = User_Quota_Cmd()
                user_quota.set_globals(api)
                t = user_quota.do_list("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_10_list(self):
                user = User_Cmd()
                user.set_globals(api)
                t = user.do_list(None)
                self.assertEquals(t,0)

        def test_user_11_info(self):
                user = User_Cmd()
                user.set_globals(api)
                t = user.do_info("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_12_quota_modify(self):
                user_quota = User_Quota_Cmd()
                user_quota.set_globals(api)
                t = user_quota.do_modify("--account "+userTest2+" --type "+userQuotaTypeTest+" --limit "+userQuotaLimitTest)
                self.assertEquals(t,0)

        def test_user_13_admin_demote(self):
                user_admin = User_Admin_Cmd()
                user_admin.set_globals(api)
                t = user_admin.do_demote("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_14_admin_promote(self):
                user_admin = User_Admin_Cmd()
                user_admin.set_globals(api)
                t = user_admin.do_promote("--account "+userTest2)
                self.assertEquals(t,0)

        def test_user_15_os_list(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api)
                t = user_os.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_16_os_disable(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api)
                t = user_os.do_disable("--account "+userTest+" --name Cen*")
                self.assertEquals(t,0)

        def test_user_17_os_enable(self):
                user_os = User_Os_Cmd()
                user_os.set_globals(api)
                t = user_os.do_enable("--account "+userTest+" --name Cen*")
                self.assertEquals(t,0)

        def test_user_18_role_list(self):
                user_role = User_Role_Cmd()
                user_role.set_globals(api)
                t = user_role.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_19_role_add(self):
                user_role= User_Role_Cmd()
                user_role.set_globals(api)
                t = user_role.do_add("--account "+userTest+" --roles "+userRoleTest1+" "+userRoleTest2)
                self.assertEquals(t,0)

        def test_user_20_role_remove(self):
                user_role = User_Role_Cmd()
                user_role.set_globals(api)
                t = user_role.do_remove("--account "+userTest+" --roles "+userRoleTest1+" "+userRoleTest2)
                self.assertEquals(t,0)

        def test_user_21_api_quota(self):
                user_api = User_Api_Cmd()
                user_api.set_globals(api)
                t = user_api.do_quota("--account "+userTest+" --apimax 50")
                self.assertEquals(t,0)

        def test_user_22_org_list(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api)
                t = user_org.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_user_23_org_add(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api)
                t = user_org.do_add("--account "+userTest2+" --admin")
                self.assertEquals(t,0)

        def test_user_24_org_remove(self):
                user_org = User_Org_Cmd()
                user_org.set_globals(api)
                t = user_org.do_remove("--account "+userTest2+" --admin")
                self.assertEquals(t,0)

        def test_user_25_create(self):
                userList = api.Users.Getall()
                exist = False
                for item in userList.users.user:
                        if item.loginName == userToCreate:
                                exist = True
                if not exist:
                        user = User_Cmd()
                        user.set_globals(api)
                        t = user.do_create("--account " + userToCreate + " --code default --email " + userToCreate + "@usharesoft.com --accountPassword " + userToCreatePassword)
                        self.assertEquals(t,0)
                else:
                        unittest.skip("User Has already been created.")

class EntitlementTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestEntitlement, ("test_entitlement_01_list",)))

class TestEntitlement(TestMotherClass):

        def test_entitlement_01_list(self):
                entitlement = Entitlement_Cmd()
                entitlement.set_globals(api)
                t = entitlement.do_list("")
                self.assertEquals(t,0)

class SubscriptionTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestSubscription,
                                                     ("test_subscription_03_create",
                                                      "test_subscription_01_list",
                                                      "test_subscription_04_update",
                                                      "test_subscription_02_info",
                                                      "test_subscription_06_disable",
                                                      "test_subscription_07_enable",
                                                      "test_subscription_08_admin_add",
                                                      "test_subscription_09_admin_remove",
                                                      "test_subscription_10_role_add",
                                                      "test_subscription_11_role_remove",
                                                      "test_subscription_12_targetFormat_add",
                                                      "test_subscription_13_targetFormat_remove",
                                                      "test_subscription_14_targetPlatform_add",
                                                      "test_subscription_15_targetPlatform_remove",
                                                      "test_subscription_16_os_add",
                                                      "test_subscription_17_os_remove",
                                                      "test_subscription_05_delete",
                                                      )))

class TestSubscription(TestMotherClass):

        def test_subscription_01_list(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_list("")
                self.assertEquals(t,0)

        def test_subscription_02_info(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_info("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_03_create(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_create("--name "+subscriptionTest+" --code test")
                self.assertEquals(t,0)

        def test_subscription_04_update(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_update("--name "+subscriptionTest+" --active")
                self.assertEquals(t,0)

        def test_subscription_05_delete(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_delete("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_06_disable(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_disable("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_07_enable(self):
                subscription = Subscription_Cmd()
                subscription.set_globals(api)
                t = subscription.do_enable("--name "+subscriptionTest)
                self.assertEquals(t,0)

        def test_subscription_08_admin_add(self):
                subscription_admin = Subscription_Admins()
                subscription_admin.set_globals(api)
                t = subscription_admin.do_add("--name "+subscriptionTest+" --admins "+subscriptionAdminTest1+" "+subscriptionAdminTest2)
                self.assertEquals(t,0)

        def test_subscription_09_admin_remove(self):
                subscription_admin = Subscription_Admins()
                subscription_admin.set_globals(api)
                t = subscription_admin.do_remove("--name "+subscriptionTest+" --admins "+subscriptionAdminTest1+" "+subscriptionAdminTest2)
                self.assertEquals(t,0)

        def test_subscription_10_role_add(self):
                subscription_role = Subscription_Roles()
                subscription_role.set_globals(api)
                t = subscription_role.do_add("--name "+subscriptionTest+" --roles "+subscriptionRoleTest1+" "+subscriptionRoleTest2)
                self.assertEquals(t,0)

        def test_subscription_11_role_remove(self):
                subscription_role = Subscription_Roles()
                subscription_role.set_globals(api)
                t = subscription_role.do_remove("--name "+subscriptionTest+" --roles "+subscriptionRoleTest1+" "+subscriptionRoleTest2)
                self.assertEquals(t,0)

        def test_subscription_12_targetFormat_add(self):
                subscription_targetFormat = Subscription_TargetFormat()
                subscription_targetFormat.set_globals(api)
                t = subscription_targetFormat.do_add("--name "+subscriptionTest+" --targetFormats "+subscriptionTargetFormatTest1+" "+subscriptionTargetFormatTest2)
                self.assertEquals(t,0)

        def test_subscription_13_targetFormat_remove(self):
                subscription_targetFormat = Subscription_TargetFormat()
                subscription_targetFormat.set_globals(api)
                t = subscription_targetFormat.do_remove("--name "+subscriptionTest+" --targetFormats "+subscriptionTargetFormatTest1+" "+subscriptionTargetFormatTest2)
                self.assertEquals(t,0)

        def test_subscription_14_targetPlatform_add(self):
                subscription_targetPlatform = Subscription_TargetPlatform()
                subscription_targetPlatform.set_globals(api)
                t = subscription_targetPlatform.do_add("--name "+subscriptionTest+" --targetPlatforms "+subscriptionTargetPlatformTest1+" "+subscriptionTargetPlatformTest2)
                self.assertEquals(t,0)

        def test_subscription_15_targetPlatform_remove(self):
                subscription_targetPlatform = Subscription_TargetPlatform()
                subscription_targetPlatform.set_globals(api)
                t = subscription_targetPlatform.do_remove("--name "+subscriptionTest+" --targetPlatforms "+subscriptionTargetPlatformTest1+" "+subscriptionTargetPlatformTest2)
                self.assertEquals(t,0)

        def test_subscription_16_os_add(self):
                subscription_os = Subscription_Os()
                subscription_os.set_globals(api)
                t = subscription_os.do_add("--name "+subscriptionTest+" --os "+subscriptionOsTest1)
                self.assertEquals(t,0)

        def test_subscription_17_os_remove(self):
                subscription_os = Subscription_Os()
                subscription_os.set_globals(api)
                t = subscription_os.do_remove("--name "+subscriptionTest+" --os "+subscriptionOsTest1)
                self.assertEquals(t,0)

        def test_subscription_18_quota_update(self):
                subscription_quota = Subscription_Quota()
                subscription_quota.set_globals(api)
                t = subscription_quota.do_update(userSubscriptionQuotaUpdate)
                self.assertEquals(t,0)

class RoleTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestRole,
                                                     ("test_role_01_list",
                                                      "test_role_02_info",
                                                      "test_role_03_create",
                                                      "test_role_05_entitlement_add",
                                                      "test_role_06_entitlement_remove",
                                                      "test_role_04_delete"
                                                      )))

class TestRole(TestMotherClass):

        def test_role_01_list(self):
                role = Role_Cmd()
                role.set_globals(api)
                t = role.do_list("")
                self.assertEquals(t,0)

        def test_role_02_info(self):
                role = Role_Cmd()
                role.set_globals(api)
                t = role.do_info("--name "+roleRoleTest)
                self.assertEquals(t,0)

        def test_role_03_create(self):
                roleList = api.Orgs(orgNumber).Roles.Getall()
                exist = False
                for item in roleList.roles.role:
                        if item.name == roleRoleCreateTest:
                                exist = True
                if exist:
                        unittest.skip("Role has already been created.")
                else:
                        role = Role_Cmd()
                        role.set_globals(api)
                        t = role.do_create("--name "+roleRoleCreateTest)
                        self.assertEquals(t,0)

        def test_role_05_entitlement_add(self):
                role_entitlement = Role_Entitlement_Cmd()
                role_entitlement.set_globals(api)
                t = role_entitlement.do_add("--name "+roleRoleCreateTest+" --entitlements "+roleEntitlementCreateTest1+" "+roleEntitlementCreateTest2)
                self.assertEquals(t,0)

        def test_role_06_entitlement_remove(self):
                role_entitlement = Role_Entitlement_Cmd()
                role_entitlement.set_globals(api)
                t = role_entitlement.do_remove("--name "+roleRoleCreateTest+" --entitlements "+roleEntitlementCreateTest1+" "+roleEntitlementCreateTest2)
                self.assertEquals(t,0)

        def test_role_04_delete(self):
                role = Role_Cmd()
                role.set_globals(api)
                t = role.do_delete("--name "+roleRoleCreateTest)
                self.assertEquals(t,0)

class ImagesTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestImages,
                                                     ("test_images_01_list",
                                                      "test_images_02_info"
                                                      )))

class TestImages(TestMotherClass):

        def test_images_01_list(self):
                images = Images_Cmd()
                images.set_globals(api)
                t = images.do_list("--account "+userTest)
                self.assertEquals(t,0)

        def test_images_02_info(self):
                images = Images_Cmd()
                images.set_globals(api)
                t = images.do_info("--account "+userTest+" --id "+imagesIdTest)
                self.assertEquals(t,0)

class OrgTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestOrg,
                                                     ("test_org_44_create",
                                                      "test_org_05_category_create",
                                                      "test_org_04_category_list",
                                                      "test_org_06_category_delete",
                                                      "test_org_07_category_reset",
                                                      "test_org_02_info",
                                                      "test_org_01_list",
                                                      "test_org_03_user_list",
                                                      "test_org_09_golden_create",
                                                      "test_org_08_golden_list",
                                                      "test_org_11_os_add",
                                                      "test_org_12_os_disable",
                                                      "test_org_13_os_enable",
                                                      "test_org_10_os_list",
                                                      "test_org_15_repo_create",
                                                      "test_org_16_repo_update",
                                                      "test_org_14_repo_list",
                                                      "test_org_18_repo_os_list",
                                                      "test_org_20_repo_os_detach",
                                                      "test_org_17_repo_delete",
                                                      "test_org_22_format_enable",
                                                      "test_org_21_format_list",
                                                      "test_org_23_format_disable",
                                                      "test_org_25_targetFormat_createVirtual",
                                                      "test_org_26_targetFormat_createCloud",
                                                      "test_org_27_targetFormat_createPhysical",
                                                      "test_org_24_targetFormat_list",
                                                      "test_org_28_targetFormat_update",
                                                      "test_org_29_targetFormat_addTargetPlatform",
                                                      "test_org_30_targetFormat_listTargetPlatform",
                                                      "test_org_31_targetFormat_removeTargetPlatform",
                                                      "test_org_32_targetFormat_disable",
                                                      "test_org_33_targetFormat_enable",
                                                      "test_org_34_targetFormat_delete",
                                                      "test_org_36_targetPlatform_create",
                                                      "test_org_35_targetPlatform_list",
                                                      "test_org_37_targetPlatform_update",
                                                      "test_org_38_targetPlatform_addTargetFormat",
                                                      "test_org_39_targetPlatform_listTargetFormat",
                                                      "test_org_40_targetPlatform_removeTargetFormat",
                                                      "test_org_41_targetPlatform_disable",
                                                      "test_org_42_targetPlatform_enable",
                                                      "test_org_43_targetPlatform_delete",
                                                      )))

class TestOrg(TestMotherClass):

        def test_org_01_list(self):
                org = Org_Cmd()
                org.set_globals(api)
                t = org.do_list("")
                self.assertEquals(t,0)

        def test_org_02_info(self):
                org = Org_Cmd()
                org.set_globals(api)
                t = org.do_info("")
                self.assertEquals(t,0)

        def test_org_03_user_list(self):
                org_user = Org_User_Cmd()
                org_user.set_globals(api)
                t = org_user.do_list("")
                self.assertEquals(t,0)

        def test_org_04_category_list(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api)
                t = org_category.do_list("")
                self.assertEquals(t,0)

        def test_org_05_category_create(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api)
                t = org_category.do_create("--name " +orgCategoryTestCategoryName + " --org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_06_category_delete(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api)
                t = org_category.do_delete("--name " +orgCategoryTestCategoryName + " --org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_07_category_reset(self):
                org_category = Org_Category_Cmd()
                org_category.set_globals(api)
                t = org_category.do_reset("--org " + orgCreate)
                self.assertEquals(t,0)

        def test_org_08_golden_list(self):
                org_golden = Org_Golden_Cmd()
                org_golden.set_globals(api)
                t = org_golden.do_list(orgGoldenListArgs)
                self.assertEquals(t,0)

        def test_org_09_golden_create(self):
                org_golden = Org_Golden_Cmd()
                org_golden.set_globals(api)
                t = org_golden.do_create(orgGoldenCreate)
                self.assertEquals(t,0)

        def test_org_10_os_list(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api)
                t = org_os.do_list("")
                self.assertEquals(t,0)

        def test_org_11_os_add(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api)
                t = org_os.do_add(orgOsCreate)
                self.assertEquals(t,0)

        def test_org_12_os_disable(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api)
                t = org_os.do_disable(orgOsEnableDisable)
                self.assertEquals(t,0)

        def test_org_13_os_enable(self):
                org_os = Org_Os_Cmd()
                org_os.set_globals(api)
                t = org_os.do_enable(orgOsEnableDisable)
                self.assertEquals(t,0)

        def test_org_14_repo_list(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api)
                t = org_repo.do_list("")
                self.assertEquals(t,0)

        def test_org_15_repo_create(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api)
                t = org_repo.do_create(orgRepoCreate)
                self.assertEquals(t,0)

        def test_org_16_repo_update(self):
                org_repo = Org_Repo_Cmd()
                org_repo.set_globals(api)
                t = org_repo.do_update(orgRepoUpdate)
                self.assertEquals(t,0)

        def test_org_17_repo_delete(self):

                all_repos = api.Orgs(orgNumber).Repositories.Getall()
                exist = False
                for item in all_repos.repositories.repository:
                        if item.name == orgRepoName:
                                exist = True
                                orgRepoDeleteId = item.dbId
                                org_repo = Org_Repo_Cmd()
                                org_repo.set_globals(api)
                                t = org_repo.do_delete("--ids " + orgRepoDeleteId)
                                self.assertEquals(t,0)
                if not exist:
                        unittest.SkipTest("Repo ID not found, maybe a problem at repo creation.")

        def test_org_18_repo_os_list(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api)
                t = org_repo_os.do_list("--repoId " + orgRepoOsRepoId)
                self.assertEquals(t,0)

        def test_org_19_repo_os_attach(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api)
                t = org_repo_os.do_attach("--repoIds " + orgRepoOsRepoId + " " + orgRepoOsAttachDetach)
                self.assertEquals(t,0)

        def test_org_20_repo_os_detach(self):
                org_repo_os = Org_Repo_Os_Cmd()
                org_repo_os.set_globals(api)
                t = org_repo_os.do_detach("--repoIds " + orgRepoOsRepoId + " " + orgRepoOsAttachDetach)
                self.assertEquals(t,0)

        def test_org_21_format_list(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api)
                t = org_format.do_list("")
                self.assertEquals(t,0)

        def test_org_22_format_enable(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api)
                t = org_format.do_enable("--format " + orgFormatEnableDisable)
                self.assertEquals(t,0)

        def test_org_23_format_disable(self):
                org_format = Org_Format_Cmd()
                org_format.set_globals(api)
                t = org_format.do_disable("--format " + orgFormatEnableDisable)
                self.assertEquals(t,0)

        def test_org_24_targetFormat_list(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_list(None)
                self.assertEquals(t,0)

        def test_org_25_targetFormat_createVirtual(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_create("--name " + orgTargetFormatCreateVirtual + " --format vbox --category " + orgTargetFormatCategoryVirtual + " --type virtual")
                self.assertEquals(t,0)

        def test_org_26_targetFormat_createCloud(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_create("--name " + orgTargetFormatCreateCloud + " --format openstackqcow2 --category " + orgTargetFormatCategoryCloud + " --type cloud -- credAccountType openstack --file data/UShareSoft.svg")
                self.assertEquals(t,0)

        def test_org_27_targetFormat_createPhysical(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_create("--name " + orgTargetFormatCreatePhysical + " --format ISO --category " + orgTargetFormatCategoryPhysical + " --type physical")
                self.assertEquals(t,0)

        def test_org_28_targetFormat_update(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreatePhysical)
                if id is not None and id !="":
                        t = org_targetFormat.do_update("--id " + id + " --name " + orgTargetFormatCreatePhysical+"Updated")
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target format to update")

        def test_org_29_targetFormat_addTargetPlatform(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreateCloud)
                if id is not None and id !="":
                        t = org_targetFormat.do_addTargetPlatform("--id " + id + " --targetPlatforms " + orgTargetPlatformOpenStack)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target format to add target platforms")

        def test_org_30_targetFormat_listTargetPlatform(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreateCloud)
                if id is not None and id !="":
                        t = org_targetFormat.do_listTargetPlatform("--id " + id)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target format to list target platforms")

        def test_org_31_targetFormat_removeTargetPlatform(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreateCloud)
                if id is not None and id !="":
                        t = org_targetFormat.do_removeTargetPlatform("--id " + id + " --targetPlatforms " + orgTargetPlatformOpenStack)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target format to remove target platforms")

        def test_org_32_targetFormat_disable(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_disable("--targetFormats " + orgTargetFormatsEnableDisable)
                self.assertEquals(t,0)

        def test_org_33_targetFormat_enable(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                t = org_targetFormat.do_enable("--targetFormats " + orgTargetFormatsEnableDisable)
                self.assertEquals(t,0)

        def test_org_34_targetFormat_delete(self):
                org_targetFormat = Org_TargetFormat_Cmd()
                org_targetFormat.set_globals(api)
                msgNoDeleted = None
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreateVirtual)
                if id is not None and id !="":
                        t = org_targetFormat.do_delete("--id " + id)
                        self.assertEquals(t,0)
                else:
                        msgNoDeleted = "virtual "
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreatePhysical+"Updated")
                if id is not None and id !="":
                        t = org_targetFormat.do_delete("--id " + id)
                        self.assertEquals(t,0)
                else:
                        msgNoDeleted = msgNoDeleted + "physical "
                id = get_targetFormat_id(org_targetFormat, orgTargetFormatCreateCloud)
                if id is not None and id !="":
                        t = org_targetFormat.do_delete("--id " + id)
                        self.assertEquals(t,0)
                else:
                        msgNoDeleted = msgNoDeleted + "cloud"
                if msgNoDeleted is not None:
                        raise unittest.SkipTest("no target format of type " + msgNoDeleted + " to delete")

        def test_org_35_targetPlatform_list(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                t = org_targetPlatform.do_list(None)
                self.assertEquals(t,0)

        def test_org_36_targetPlatform_create(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                t = org_targetPlatform.do_create("--name " + orgTargetPlatformCreateAbiquo + " --type abiquo --file data/UShareSoft.svg")
                self.assertEquals(t,0)

        def test_org_37_targetPlatform_update(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                id = get_targetPlatform_id(org_targetPlatform, orgTargetPlatformCreateAbiquo)
                if id is not None and id !="":
                        t = org_targetPlatform.do_update("--id " + id + " --name " + orgTargetPlatformCreateAbiquo+"Updated")
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target platform to update")

        def test_org_38_targetPlatform_addTargetFormat(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                id = get_targetPlatform_id(org_targetPlatform, orgTargetPlatformCreateAbiquo+"Updated")
                if id is not None and id !="":
                        t = org_targetPlatform.do_addTargetFormat("--id " + id + " --targetFormats " + orgTargetFormatAbiquo)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target platform to add target formats")

        def test_org_39_targetPlatform_listTargetFormat(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                id = get_targetPlatform_id(org_targetPlatform, orgTargetPlatformCreateAbiquo+"Updated")
                if id is not None and id !="":
                        t = org_targetPlatform.do_listTargetFormat("--id " + id)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target platform to list target formats")

        def test_org_40_targetPlatform_removeTargetFormat(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                id = get_targetPlatform_id(org_targetPlatform, orgTargetPlatformCreateAbiquo+"Updated")
                if id is not None and id !="":
                        t = org_targetPlatform.do_removeTargetFormat("--id " + id + " --targetFormats " + orgTargetFormatAbiquo)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("No target platform to remove target formats")

        def test_org_41_targetPlatform_disable(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                t = org_targetPlatform.do_disable("--targetPlatforms " + orgTargetPlatformsEnableDisable)
                self.assertEquals(t,0)

        def test_org_42_targetPlatform_enable(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                t = org_targetPlatform.do_enable("--targetPlatforms " + orgTargetPlatformsEnableDisable)
                self.assertEquals(t,0)

        def test_org_43_targetPlatform_delete(self):
                org_targetPlatform = Org_TargetPlatform_Cmd()
                org_targetPlatform.set_globals(api)
                msgNoDeleted = None
                id = get_targetPlatform_id(org_targetPlatform, orgTargetPlatformCreateAbiquo+"Updated")
                if id is not None and id !="":
                        t = org_targetPlatform.do_delete("--id " + id)
                        self.assertEquals(t,0)
                else:
                        raise unittest.SkipTest("no target platform to delete")

        def test_org_44_create(self):
                orgs = api.Orgs(orgNumber).Getall()
                exist = False
                for item in orgs.orgs.org:
                        if item.name == orgCreate:
                                exist = True
                if exist:
                        unittest.skip("Organization already created.")
                else:
                        org = Org_Cmd()
                        org.set_globals(api)
                        t = org.do_create("--org " + orgCreate)
                        self.assertEquals(t,0)

class OsTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestOs,
                                                     ("test_os_01_list",
                                                      "test_os_02_milestone_add",
                                                      "test_os_03_milestone_list",
                                                      "test_os_04_milestone_modify",
                                                      "test_os_05_milestone_remove"
                                                      )))

class TestOs(TestMotherClass):

        def test_os_01_list(self):
                org = Os_Cmd()
                org.set_globals(api)
                t = org.do_list("")
                self.assertEquals(t,0)

        def test_os_02_milestone_add(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api)
                t = os_milestone.do_add(osMilestoneVersion + " --date " + osMilestoneAddNewDate + " --name " + osMilestoneAddNewName)
                self.assertEquals(t,0)

        def test_os_03_milestone_list(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api)
                t = os_milestone.do_list(osMilestoneVersion)
                self.assertEquals(t,0)

        def test_os_04_milestone_modify(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api)
                t = os_milestone.do_modify(osMilestoneVersion + " --date " + osMilestoneModifyNewDate + " --name " + osMilestoneAddNewName)
                self.assertEquals(t,0)

        def test_os_05_milestone_remove(self):
                os_milestone = Os_Milestone_Cmd()
                os_milestone.set_globals(api)
                t = os_milestone.do_remove(osMilestoneVersion + " --name " + osMilestoneAddNewDate)
                self.assertEquals(t,0)

class PimagesTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestPimages,
                                                     ("test_pimages_01_list",
                                                      "test_pimages_02_info"
                                                      )))

class TestPimages(TestMotherClass):

        def test_pimages_01_list(self):
                pimages = Pimages_Cmd()
                pimages.set_globals(api)
                t = pimages.do_list("--account " + userTest)
                self.assertEquals(t,0)

        def test_pimages_02_info(self):
                pimages = Pimages_Cmd()
                pimages.set_globals(api)
                t = pimages.do_info("--account " + userTest + " --id 3")
                self.assertEquals(t,0)

class UserGroupTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestUserGroup,
                                                     ("test_usergrp_01_create",
                                                      "test_usergrp_02_list",
                                                      "test_usergrp_05_user_add",
                                                      "test_usergrp_03_info",
                                                      "test_usergrp_06_user_remove",
                                                      "test_usergrp_04_delete"
                                                      )))

class TestUserGroup(TestMotherClass):

        def test_usergrp_01_create(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api)
                t = usergrp.do_create("--name " + usergrpTest + " --email " + usergrpTest + "@usharesoft.com --usergrpPassword " + usergrpTest + " --accounts " + usergrpTestAddAccounts)
                self.assertEquals(t,0)

        def test_usergrp_02_list(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api)
                t = usergrp.do_list("")
                self.assertEquals(t,0)

        def test_usergrp_03_info(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api)
                t = usergrp.do_info("--name " + usergrpTest)
                self.assertEquals(t,0)

        def test_usergrp_04_delete(self):
                usergrp = Usergrp_Cmd()
                usergrp.set_globals(api)
                t = usergrp.do_delete("--name " + usergrpTest)
                self.assertEquals(t,0)

        def test_usergrp_05_user_add(self):
                usergrp_user = UserGroup_User_Cmd()
                usergrp_user.set_globals(api)
                t = usergrp_user.do_add("--name " + usergrpTest + " --accounts " + usergrpTestUserAddAfter)
                self.assertEquals(t,0)

        def test_usergrp_06_user_remove(self):
                usergrp_user = UserGroup_User_Cmd()
                usergrp_user.set_globals(api)
                t = usergrp_user.do_add("--name " + usergrpTest + " --accounts " + usergrpTestUserAddAfter)
                self.assertEquals(t,0)

class TemplateTestSuite(unittest.TestSuite):
        def __init__(self):
                unittest.TestSuite.__init__(self,map(TestTemplate,
                                                     ("test_template_01_list",
                                                      "test_template_02_info",
                                                      "test_template_03_images",
                                                      "test_template_04_pimages"
                                                      )))

class TestTemplate(TestMotherClass):

        def test_template_01_list(self):
                template = Template_Cmd()
                template.set_globals(api)
                t = template.do_list("--account root")
                self.assertEquals(t,0)

        def test_template_02_info(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api)
                        t = template.do_info("--account " + userTest + " --id " + templateID + "")
                        self.assertEquals(t,0)

        def test_template_03_images(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api)
                        t = template.do_images("--account " + userTest + " --id " + templateID)
                        self.assertEquals(t,0)

        def test_template_04_pimages(self):
                templateList = api.Users(userTest).Appliances.Getall()
                templateList = templateList.appliances.appliance
                if len(templateList) == 0:
                        unittest.skip("No Template list for userTest.")
                else:
                        templateID = str(templateList[0].dbId)
                        template = Template_Cmd()
                        template.set_globals(api)
                        t = template.do_pimages("--account " + userTest + " --id " + templateID)
                        self.assertEquals(t,0)

if __name__ == '__main__':
        v = sys.version_info

        import xmlrunner
        runner = unittest.TextTestRunner()
        userTestSuite = UserTestSuite()
        subscriptionTestSuite = SubscriptionTestSuite()
        osTestSuite = OsTestSuite()
        userGroupTestSuite = UserGroupTestSuite()
        templateTestSuite = TemplateTestSuite()
        pimagesTestSuite = PimagesTestSuite()
        entitlementTestSuite = EntitlementTestSuite()
        imagesTestSuite = ImagesTestSuite()
        runner.run = unittest.TestSuite([userTestSuite,
                                         subscriptionTestSuite,
                                         osTestSuite,
                                         userGroupTestSuite,
                                         templateTestSuite,
                                         pimagesTestSuite,
                                         entitlementTestSuite,
                                         imagesTestSuite])


if v >= (2,7):
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
else:
        unittest.main()
