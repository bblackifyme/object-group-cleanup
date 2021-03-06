import unittest
import sys
sys.path.append('../python')
import ncs
import socket
import obj_cleanup
if __name__ == '__main__':
    device_typ = "device"
    device_name = "asa-netsim-1"
    ret = {}
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        device = root.devices.device[device_name]
        input1 = root.Object_group_cleaner.search.get_input()
        new_obj = input1.inputs.create()
        new_obj.input_type = device_typ
        new_obj.value = device_name

        print dir(root.Object_group_cleaner.cleanup)
        print dir(root.Object_group_cleaner.cleanup(input1))
        output1 = root.Object_group_cleaner.cleanup(input1)
        end_time = output1.end_time
        org_gps = output1.number_of_ogs_deleted
        for og in org_gps:
            if og.og_type in ret.keys():
                ret[og.og_type].append(og.object_group)
            #Else, create key and append og
            else:
                ret[og.og_type] = [og.object_group]
        #print ret
        run_time = output1.run_time
        start_time = output1.start_time
        """
        print run_time
        print output1.orphaned_object_groups
        print dir(output1.orphaned_object_groups)
        print type(output1.orphaned_object_groups)
"""
