
__author__="UShareSoft"

from ussclicore.argumentParser import ArgumentParser, ArgumentParserError
from ussclicore.cmd import Cmd, CoreGlobal
from texttable import Texttable
from uforgecli.utils.org_utils import org_get
from ussclicore.utils import generics_utils, printer
from uforgecli.utils.uforgecli_utils import *
from uforgecli.utils.compare_utils import compare
from uforgecli.utils.extract_id_utils import extractId
from hurry.filesize import size
from uforgecli.utils import *
import shlex


class Template_Cmd(Cmd, CoreGlobal):
        """Administer templates for a user (list/info/create/delete/generate/share etc)"""

        cmd_name = "template"

        def __init__(self):
                super(Template_Cmd, self).__init__()

        def arg_list(self):
                doParser = ArgumentParser(add_help=True, description="List all the templates created by a user")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', required=True, help="Name of the user")
                optional.add_argument('--os', dest='os', nargs='+', required=False, help="Only display templates that have been built from the operating system(s). You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--name',  dest='name', nargs='+', required=False, help="Only display templates that have the name matching this name. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")

                return doParser

        def do_list(self, args):
                try:
                        doParser = self.arg_list()
                        doArgs = doParser.parse_args(shlex.split(args))

                        userAppliances = self.api.Users(doArgs.account).Appliances.Getall()
                        if userAppliances.total == 0:
                                printer.out("[" + doArgs.account + "] has no template.")
                                return 0
                        userAppliances = userAppliances.appliances.appliance

                        if doArgs.os is not None:
                                userAppliances = compare(userAppliances, doArgs.os, "distributionName")
                        if doArgs.name is not None:
                                userAppliances = compare(userAppliances, doArgs.name, "name")

                        if len(userAppliances) == 0:
                                printer.out("No match with this filters.")
                                return 0
                        printer.out("List of templates created by [" + doArgs.account + "]:")
                        table = Texttable(200)
                        table.set_cols_align(["l", "l", "l", "l", "l", "l", "l", "l", "l", "l"])
                        table.header(["Id", "Name", "Version", "OS", "Created", "Last Modified", "# Imgs", "Updates", "Imp", "Shd"])
                        for appliance in userAppliances:
                                created = appliance.created.strftime("%Y-%m-%d %H:%M:%S")
                                lastModified = appliance.lastModified.strftime("%Y-%m-%d %H:%M:%S")
                                if appliance.imported:
                                        imported = "X"
                                else:
                                        imported = ""
                                if appliance.shared:
                                        shared = "X"
                                else:
                                        shared = ""
                                table.add_row([appliance.dbId, appliance.name, appliance.version, appliance.distributionName + " " + appliance.archName, created, lastModified, str(len(appliance.images.image)), appliance.nbUpdates, imported, shared])
                        print table.draw() + "\n"

                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_list()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_list(self):
                doParser = self.arg_list()
                doParser.print_help()

        def arg_info(self):
                doParser = ArgumentParser(add_help=True, description="Retrieve detailed information of a user's template")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', required=True, help="Name of the user")
                mandatory.add_argument('--id', dest='id', required=True, help="The unique identifier of the template to retrieve")
                optional.add_argument('--all', action="store_true", dest='all', required=False, help="Print out more information contained in the template")

                return doParser

        def do_info(self, args):
                try:
                        doParser = self.arg_info()
                        doArgs = doParser.parse_args(shlex.split(args))

                        userAppliance = self.api.Users(doArgs.account).Appliances(doArgs.id).Get()

                        printer.out("Informations about [" + userAppliance.name + "]:")

                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        table.add_row(["Name", userAppliance.name])
                        table.add_row(["Id", userAppliance.dbId])
                        table.add_row(["Version", userAppliance.version])
                        table.add_row(["Uri", userAppliance.uri])
                        table.add_row(["Created", userAppliance.created.strftime("%Y-%m-%d %H:%M:%S")])
                        table.add_row(["Last Modified", userAppliance.created.strftime("%Y-%m-%d %H:%M:%S")])
                        table.add_row(["Last Package Update", userAppliance.lastPkgUpdate.strftime("%Y-%m-%d %H:%M:%S")])
                        table.add_row(["Available OS Updates", userAppliance.nbUpdates])
                        if userAppliance.shared:
                                shared = "Yes"
                        else:
                                shared = "No"
                        table.add_row(["Shared", shared])
                        if userAppliance.imported:
                                imported = "Yes"
                        else:
                                imported = "No"
                        table.add_row(["Cloned from App Store", imported])
                        table.add_row(["Description", userAppliance.description])
                        print table.draw() + "\n"
                        printer.out("OS Profile", printer.INFO)
                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        table.add_row(["OS", userAppliance.distributionName + " " + userAppliance.archName])
                        if userAppliance.osProfile is not None:
                                table.add_row(["OS Profile Type", userAppliance.osProfile.name])
                        else:
                                table.add_row(["OS Profile", "None"])
                        if userAppliance.osProfile is not None:
                                packagesUri = extractId(userAppliance.osProfile.packagesUri, operation=False)
                                allPkgs = self.api.Users(doArgs.account).Appliances(packagesUri[1]).Osprofile(packagesUri[0]).Pkgs.Getall()
                                table.add_row(["# OS Packages", str(len(allPkgs.pkgs.pkg))])
                        if userAppliance.osProfile is not None:
                                pkgsTotalSize = 0
                                for pkg in allPkgs.pkgs.pkg:
                                        pkgsTotalSize = pkgsTotalSize + pkg.size
                                osTotalSize = pkgsTotalSize + userAppliance.size
                        else:
                                osTotalSize = userAppliance.size
                        table.add_row(["Total OS Profile Size", size(osTotalSize)])
                        pkgNumber = 0
                        allPkgs = generics_utils.order_list_object_by(allPkgs.pkgs.pkg, "name")
                        if doArgs.all:
                                for pkg in allPkgs:
                                        pkgNumber = pkgNumber + 1
                                        table.add_row(["Packages N " + str(pkgNumber), pkg.name + " " + pkg.version + " " + pkg.arch + " (" + size(pkg.size) + ")"])
                        print table.draw() + "\n"

                        printer.out("Install Settings", printer.INFO)
                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        if userAppliance.installProfile.adminPasswordAuto:
                                table.add_row(["Password", userAppliance.installProfile.adminPassword])
                        else:
                                table.add_row(["Password", "asked during first boot or install"])
                        if userAppliance.installProfile.internetSettingsAuto:
                                table.add_row(["Internet Settings", "DHCP"])
                        else:
                                table.add_row(["Internet Settings", "asked during first boot or install"])
                        if userAppliance.installProfile.skipLicenses:
                                table.add_row(["Licensing", "skipped"])
                        else:
                                table.add_row(["Licensing", "shown at first boot or install"])
                        if userAppliance.installProfile.timezoneAuto:
                                table.add_row(["Time Zone", userAppliance.installProfile.timezone])
                        else:
                                table.add_row(["Time Zone", "asked during first boot or install"])
                        if userAppliance.installProfile.partitionTable.disks.disk is not None:
                                diskNumber = 0
                                for disk in userAppliance.installProfile.partitionTable.disks.disk:
                                        diskNumber = diskNumber + 1
                                        table.add_row(["Disk " + str(diskNumber), disk.name + " " + str(disk.size) + " MB " + disk.partitionType])
                                        if disk.partitions.partition is not None:
                                                partitionNumber = 0
                                                for partition in disk.partitions.partition:
                                                        partitionNumber = partitionNumber + 1
                                                        if partition.fstype is not None:
                                                                fstype = partition.fstype
                                                        else:
                                                                fstype = ""
                                                        if partition.mpoint is not None:
                                                                mpoint = partition.mpoint
                                                        else:
                                                                mpoint = ""
                                                        if partition.label is not None:
                                                                label = partition.label
                                                        else:
                                                                label = ""
                                                        if partition.growable:
                                                                growable = "grow"
                                                        else:
                                                                growable = ""
                                                        table.add_row(["Partition " + str(partitionNumber), disk.name + partition.name + " " + str(partition.partitionSize) + " MB " + fstype + " " + mpoint + " " + label + " " + growable])
                                                        if partition.logicalPartitions.logicalPartition is not None:
                                                                logicalPartitionNumber = 0
                                                                for logicalPartition4 in partition.logicalPartitions.logicalPartition:
                                                                        logicalPartitionNumber = logicalPartitionNumber + 1
                                                                        if logicalPartition4.fstype is not None:
                                                                                fstype2 = logicalPartition4.fstype
                                                                        else:
                                                                                fstype2 = ""
                                                                        if logicalPartition4.mpoint is not None:
                                                                                mpoint2 = logicalPartition4.mpoint
                                                                        else:
                                                                                mpoint2 = ""
                                                                        if logicalPartition4.label is not None:
                                                                                label2 = logicalPartition4.label
                                                                        else:
                                                                                label2 = ""
                                                                        if logicalPartition4.growable:
                                                                                growable2 = "grow"
                                                                        else:
                                                                                growable2 = ""
                                                                        table.add_row(["Logical Partition " + str(logicalPartitionNumber), logicalPartition4.name + " " + str(logicalPartition4.partitionSize) + " MB " + fstype2 + " " + mpoint2 + " " + label2 + " " + growable2])

                        print table.draw() + "\n"

                        printer.out("Projects", printer.INFO)
                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        allProjects = self.api.Users(doArgs.account).Appliances(userAppliance.dbId).Projects.Getall()
                        if allProjects is None:
                                totalProjects = "0"
                        else:
                                totalProjects = str(len(allProjects.projects.project))
                        table.add_row(["# Projects", totalProjects])
                        if doArgs.all and totalProjects != "0":
                                projectNumber = 0
                                for project in allProjects.projects.project:
                                        projectNumber = projectNumber + 1
                                        table.add_row(["Project N " + str(projectNumber), project.name + " " + project.version + " (" + project.size + " bytes)"])
                        print table.draw() + "\n"

                        printer.out("My Software", printer.INFO)
                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        allSoftware = self.api.Users(doArgs.account).Appliances(userAppliance.dbId).Mysoftware.Getall()
                        if allSoftware is None:
                                totalSoftwares = "0"
                        else:
                                totalSoftwares = str(len(allSoftware.mySoftwareList.mySoftware))
                        table.add_row(["# Custom Software", totalSoftwares])
                        if doArgs.all and totalSoftwares != "0":
                                softwareNumber = 0
                                for software in allSoftware.mySoftwareList.mySoftware:
                                        softwareNumber = softwareNumber + 1
                                        table.add_row(["Project N " + str(softwareNumber), software.name + " " + software.version + " (" + software.size + " bytes)"])
                        print table.draw() + "\n"

                        printer.out("Configuration", printer.INFO)
                        table = Texttable(200)
                        table.set_cols_align(["l", "l"])
                        if userAppliance.oasPackageUri is None:
                                table.add_row(["OAS Pkg Uploaded", "no"])
                        else:
                                Oas = self.api.Users(doArgs.account).Appliances(userAppliance.dbId).Oas(extractId(userAppliance.oasPackageUri)).Get()
                                if not Oas.uploaded:
                                        table.add_row(["OAS Pkg Uploaded", "no"])
                                else:
                                        table.add_row(["OAS Pkg Uploaded", "yes"])
                                        table.add_row(["OAS Pkg", Oas.name])
                                        table.add_row(["OAS Pkg Size", size(Oas.size)])
                                        if Oas.licenseUploaded:
                                                table.add_row(["OAS Licence Uploaded", "yes"])
                                        else:
                                                table.add_row(["OAS Licence Uploaded", "no"])
                        if userAppliance.bootScriptsUri is None:
                                table.add_row(["# Boot Scripts", "0"])
                        else:
                                bootScripts = self.api.Users(doArgs.account).Appliances(userAppliance.dbId).Bootscripts(extractId(userAppliance.bootScriptsUri)).Getall()
                                table.add_row(["# Boot Scripts", str(len(bootScripts.bootScripts.bootScript))])
                                bootScriptsNumber = 0
                                for item in bootScripts.bootScripts.bootScript:
                                        bootScriptsNumber = bootScriptsNumber + 1
                                        table.add_row(["Boot Script N 1 Details", item.name + " " + item.bootType])
                        print table.draw() + "\n"

                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_info()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_info(self):
                doParser = self.arg_info()
                doParser.print_help()

        def arg_images(self):
                doParser = ArgumentParser(add_help=True, description="Retrieve list of images generated from the template")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', required=True, help="Name of the user.")
                mandatory.add_argument('--id', dest='id', required=True, help="Id of the appliance.")
                optional.add_argument('--os', dest='os', nargs='+', required=False, help="Only display templates that have been built from the operating system(s). You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--name',  dest='name', nargs='+', required=False, help="Only display templates that have the name matching this name. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--format',  dest='format', nargs='+', required=False, help="Only display images that have been generated by the following format(s). You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                return doParser

        def do_images(self, args):
                try:
                        doParser = self.arg_images()
                        doArgs = doParser.parse_args(shlex.split(args))

                        printer.out("Getting images list...")
                        allImages = self.api.Users(doArgs.account).Appliances(doArgs.id).Images.Getall()

                        appliancesList = self.api.Users(doArgs.account).Appliances.Getall()
                        appliancesList = appliancesList.appliances.appliance

                        if allImages is None or len(allImages.images.image) == 0:
                                printer.out("No images found for user [" + doArgs.account + "].")
                                return 0

                        allImages = generics_utils.order_list_object_by(allImages.images.image, "name")

                        if doArgs.name is not None:
                                allImages = compare(allImages, doArgs.name, "name")
                        if doArgs.format is not None:
                                allImages = compare(allImages, doArgs.format, "format", "name")
                        if doArgs.os is not None:
                                allImages = compare(list=allImages, values=doArgs.os, attrName='distributionName', subattrName=None, otherList=appliancesList, linkProperties=['applianceUri', 'uri'])

                        if allImages is None or len(allImages) == 0:
                                printer.out("No images found for user [" + doArgs.account + "] with these filters.")
                                return 0

                        printer.out("Images list :")
                        table = Texttable(200)
                        table.set_cols_align(["l", "l", "l", "l", "l", "l", "l", "l", "l", "l"])
                        table.header(["ID", "Name", "Version", "Rev", "OS", "Format", "Created", "Size", "Compressed", "Status"])
                        for image in allImages:
                                created = image.created.strftime("%Y-%m-%d %H:%M:%S")
                                if image.compress:
                                        compressed = "X"
                                else:
                                        compressed = ""
                                if image.status.error:
                                        status = "Error"
                                elif image.status.cancelled:
                                        status = "Cancelled"
                                elif image.status.complete:
                                        status = "Done"
                                else:
                                        status = "Generating"
                                appliance = self.api.Users(doArgs.account).Appliances(doArgs.id).Get()
                                osImage = appliance.distributionName + " " + appliance.archName
                                table.add_row([image.dbId, image.name, image.version, image.revision, osImage, image.targetFormat.name, created, size(image.size), compressed, status])
                        print table.draw() + "\n"

                        printer.out("Found " + str(len(allImages)) + " images.")
                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_images()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_images(self):
                doParser = self.arg_images()
                doParser.print_help()

        def arg_pimages(self):
                doParser = ArgumentParser(add_help=True, description="Retrieve list of images published to cloud environments from the template")

                mandatory = doParser.add_argument_group("mandatory arguments")
                optional = doParser.add_argument_group("optional arguments")

                mandatory.add_argument('--account', dest='account', required=True, help="Name of the user.")
                mandatory.add_argument('--id', dest='id', required=True, help="Id of the appliance.")
                optional.add_argument('--os', dest='os', nargs='+', required=False, help="Only display templates that have been built from the operating system(s). You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--name',  dest='name', nargs='+', required=False, help="Only display templates that have the name matching this name. You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")
                optional.add_argument('--format',  dest='format', nargs='+', required=False, help="Only display images that have been generated by the following format(s). You can use Unix matching system (*,?,[seq],[!seq]) and multiple match separating by space.")

                return doParser

        def do_pimages(self, args):
                try:
                        doParser = self.arg_pimages()
                        doArgs = doParser.parse_args(shlex.split(args))

                        printer.out("Getting published images list...")
                        allPimages = self.api.Users(doArgs.account).Appliances(doArgs.id).Pimages.Getall()

                        appliancesList = self.api.Users(doArgs.account).Appliances.Getall()
                        appliancesList = appliancesList.appliances.appliance

                        if allPimages is None or len(allPimages.publishImages.publishImage) == 0:
                                printer.out("No published image found.")
                                return 0
                        allPimages = generics_utils.order_list_object_by(allPimages.publishImages.publishImage, "name")

                        if doArgs.name is not None:
                                allPimages = compare(allPimages, doArgs.name, "name")
                        if doArgs.format is not None:
                                allPimages = compare(allPimages, doArgs.format, "format", "name")
                        if doArgs.os is not None:
                                allPimages = compare(list=allPimages, values=doArgs.os, attrName='distributionName', subattrName=None, otherList=appliancesList, linkProperties=['applianceUri', 'uri'])

                        printer.out("Published images list :")
                        table = Texttable(200)
                        table.set_cols_align(["l", "l", "l", "l", "l", "l", "l", "l", "l"])
                        table.header(["ID", "Name", "Version", "Rev", "OS", "Cloud", "Published", "Size", "Status"])
                        for image in allPimages:
                                cloud = image.created.strftime("%Y-%m-%d %H:%M:%S")
                                if image.status.error:
                                        status = "Error"
                                elif image.status.cancelled:
                                        status = "Cancelled"
                                elif image.status.complete:
                                        status = "Done"
                                else:
                                        status = "Generating"
                                appliance = self.api.Users(doArgs.account).Appliances(doArgs.id).Get()
                                osImage = appliance.distributionName + " " + appliance.archName
                                table.add_row([image.dbId, image.name, image.version, image.revision, osImage, image.targetFormat.name, cloud, size(image.size), status])
                        print table.draw() + "\n"
                        return 0

                except ArgumentParserError as e:
                        printer.out("ERROR: In Arguments: " + str(e), printer.ERROR)
                        self.help_pimages()
                except Exception as e:
                        return handle_uforge_exception(e)

        def help_pimages(self):
                doParser = self.arg_pimages()
                doParser.print_help()
