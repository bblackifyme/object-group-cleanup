import ncs
import socket
import time
import re

def flag_ogs_in_box_test(box):
    """
    A function that returns a dictionary of the object groups that are not found
    in any of the inputted device's access lists, organized by object group type.
    """

    #Initializing python lists
    og_list = []
    og_typ = []
    rul_list = []
    ret = {}

    #Creating transaction and setting root to access NSO
    with ncs.maapi.single_read_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #Adding all of the object groups and their types to python lists
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                og_list.append(og.id)
                og_typ.append(str(og))      #str(og) is the object group type

        #print "Total Number of OG's: %d" %len(og_list)
        #Adding each access list's rules to a python list (temp_rul_list) and
        #then adding those lists as elements of another python list (acl_list)
        for acl in root.devices.device[box].config.asa__access_list.access_list_id:
            for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
                print rul.id
                match = re.findall('object-group ([\w:*.*]+[-\w+*.*]*)', rul.id)
                for m in match:
                    rul_list.append(m)

    og_list = set(og_list)
    rul_list = set(rul_list)

    final  = og_list.difference(rul_list)

    print final
    # #Iterating through both object group and object group type lists simultaneously
    # for og, typ in zip(og_list, og_typ):
    #     flag = 0
    #     for acl in acl_list:
    #         #flag indicates whether og was found in an access list
    #
    #         for rule in acl:
    #             if og in rule:
    #                 flag = 1
    #                 break
    #
    #         #flag = banish(og, acl)
    #         #If found, continue to the next object group
    #         if flag:
    #             break
    #     #If not found in any of the access lists, add to the dictionary
    #     if not flag:
    #         #If key has been created already, add og to key
    #         if typ in ret.keys():
    #             ret[typ].append(og)
    #         #Else, create key and append og
    #         else:
    #             ret[typ] = [og]

    return ret

def banish(og, acl):
    """
    A function that iterates through the rules of an acl list checking for the
    object group name within the rule. If found, the function returns true. If
    not found, function returns false.
    """
    for rule in acl:
        if og in rule:
            return True
    return False

def remove_ogs(box, og_id, og_type):
    """
    A function that removes the object group from the object group list using
    the arguments passed: device name, object group name, and object group type.
    """
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        del root.devices.device[box].config.asa__object_group[og_type][og_id]
        try:
            t.apply()
        except TimeoutError:
            print "Timeout Error"
        except:
            print "Error! NSO was unable to remove object groups."

def no_ogs_error(box):
    """
    This function prints an error message if there are no object groups to be removed for a device.
    """
    print "Error: There are no object groups that need to be removed for device ",box,"."

if __name__ == "__main__":
    """
    Main code that is used to test functionality of algorithms.
    """

    b = time.time()
    orphaned_ogs =  flag_ogs_in_box_test('svl-gem-ubvpn-gw1a.cisco.com')
    print orphaned_ogs

    af = time.time()
    print af-b
