__author__="UShareSoft"

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from texttable import Texttable
from uforgecli.utils.org_utils import org_get
from ussclicore.utils import generics_utils, printer, ascii_bar_graph
from uforgecli.utils.uforgecli_utils import *
from uforgecli.utils import *
from hurry.filesize import size
from uforgecli.utils import constants
import shlex



class User_Quota_Cmd(Cmd, CoreGlobal):
        """List the status of all the quotas that can be set for the user (disk usage, generations, scans and number of templates)"""

        cmd_name = "quota"

        def __init__(self):
                super(User_Quota_Cmd, self).__init__()

        def arg_list(self):
                doParser = ArgumentParser(add_help = True, description="Displays the user's quota information")
                mandatory = doParser.add_argument_group("mandatory arguments")
                mandatory.add_argument('--account', dest='account', type=str, required=True, help="User name of the account to see quotas")
                return doParser

        def do_list(self, args):
                try:
                        doParser = self.arg_list()
                        doArgs = doParser.parse_args(shlex.split(args))
                        #call UForge API
                        printer.out("Getting quotas for ["+doArgs.account+"] ...")
                        quotas = self.api.Users(doArgs.account).Quotas.Get()
                        if quotas is None or len(quotas.quotas.quota) == 0:
                                printer.out("No quotas available for ["+doArgs.account+"].")
                        else:
                                printer.out("List of quotas available for ["+doArgs.account+"] :")

                                values = {}
                                for quota in quotas.quotas.quota:
                                        if quota.limit == -1:
                                                nb = " (" + str(quota.nb) + ")"
                                        else:
                                                nb = " (" + str(quota.nb) + "/" + str(quota.limit) + ")"

                                        if quota.type == constants.QUOTAS_SCAN:
                                                text = "Scan" + ("s" if quota.nb > 1 else "") + nb
                                        elif quota.type == constants.QUOTAS_TEMPLATE:
                                                text = "Template" + ("s" if quota.nb > 1 else "") + nb
                                        elif quota.type == constants.QUOTAS_GENERATION:
                                                text = "Generation" + ("s" if quota.nb > 1 else "") + nb
                                        elif quota.type == constants.QUOTAS_DISK_USAGE:
                                                text = "Disk usage (" + size(quota.nb) + ")"

                                        if quota.limit != -1:
                                                nb = float(quota.nb)
                                                limit = float(quota.limit)
                                                values[text] = (nb/limit) * 50
                                        else:
                                                values[text] = -1

                                ascii_bar_graph.print_graph(values)
                        return 0

                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_list()
                        return 0

                except Exception as e:
                        return handle_uforge_exception(e)

        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()

        def arg_modify(self):
                doParser = ArgumentParser(add_help = True, description="Modify a user quota")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', type=str, required=True, help="user name of the account for which the current command should be executed")
                mandatory.add_argument('--type', dest='type', type=str, required=False, help="Quota type. Possible values: appliance|generation|scan|diskusage)")

                optional.add_argument('--unlimited', dest='unlimited', action="store_true", required=False, help="Flag to remove any quota from a resource (becomes unlimited)")
                optional.add_argument('--limit', dest='limit', type=int, required=False, help="Quota limit (ex: --limit 10).  Note, for disk usage this is in bytes.")
                optional.add_argument('--nb', dest='nb', type=int, required=False, help="Set the current consumption of a resource including appliance templates, generations, scans and disk usage (ex: --nb 2). This can be used for discounts or in the case of errors etc")
                return doParser

        def do_modify(self, args):
                try:
                        doParser = self.arg_modify()
                        doArgs = doParser.parse_args(shlex.split(args))

                        if not doArgs.unlimited and doArgs.limit is None and doArgs.nb is None:
                                printer.out("You must specify a modification (unlimited|limit|nb).", printer.ERROR)
                                return 0
                        printer.out("Getting quotas for ["+doArgs.account+"] ...")
                        quotas = self.api.Users(doArgs.account).Quotas.Get()

                        if quotas is None or len(quotas.quotas.quota) == 0 :
                                printer.out("No quotas available for ["+doArgs.account+"].", printer.ERROR)
                        else:
                                typeExist = False
                                for item in quotas.quotas.quota:
                                        if item.type == doArgs.type:
                                                typeExist = True
                                                if doArgs.nb is not None:
                                                        item.nb = doArgs.nb
                                                if doArgs.unlimited and doArgs.limit is None:
                                                        item.limit = -1
                                                elif doArgs.limit is not None and not doArgs.unlimited:
                                                        item.limit = doArgs.limit
                                                elif doArgs.limit is not None and doArgs.unlimited:
                                                        printer.out("You can't set a defined limit and on the other hand set an unlimited limit.", printer.ERROR)
                                                        return 2

                                if not typeExist:
                                        printer.out("Type is not defined or correct.", printer.ERROR)
                                        return 2
                                else:
                                        quotas = self.api.Users(doArgs.account).Quotas.Update(body=quotas)
                                        printer.out("Changes done.", printer.OK)

                                        quotas = generics_utils.order_list_object_by(quotas.quotas.quota, "type")
                                        table = Texttable(200)
                                        table.set_cols_align(["c", "c", "c"])
                                        table.header(["Type", "Consumed", "Limit"])
                                        for item in quotas:
                                                if item.limit == -1:
                                                        limit = "unlimited"
                                                else:
                                                        limit = item.limit
                                                if item.nb > 1:
                                                        name = item.type+"s"
                                                else:
                                                        name = item.type
                                                table.add_row([name, item.nb, limit])
                                        print table.draw() + "\n"
                        return 0

                except ArgumentParserError as e:
                        printer.out("In Arguments: "+str(e), printer.ERROR)
                        self.help_modify()
                        return 0
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_modify(self):
                doParser = self.arg_modify()
                doParser.print_help()
