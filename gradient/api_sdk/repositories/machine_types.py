from operator import itemgetter

from .. import config, serializers
from ..repositories.common import ListResources


class ListMachineTypes(ListResources):
    SERIALIZER_CLS = serializers.VmTypeSchema

    def get_request_url(self, **kwargs):
        return "vmTypes/getVmTypesByClusters"

    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_HOST

    def _get_instance_dicts(self, data, cluster_id=None, **kwargs):
        vm_types_dicts = {}  # vmType["label"]: vmType dict
        for cluster_list_of_vms in data.values():
            current_cluster_id = cluster_list_of_vms[0]["clusters"][0]["id"]

            for vm in cluster_list_of_vms:
                vm_type = vm["vmType"]
                vm_type_label = vm_type["label"]
                vm_types_dicts.setdefault(vm_type_label, vm_type)

                clusters = vm_types_dicts[vm_type_label].setdefault("clusters", [])
                if current_cluster_id not in clusters:
                    clusters.append(current_cluster_id)

        vm_types = list(vm_types_dicts.values())
        if cluster_id is not None:
            vm_types = [vm_type for vm_type in vm_types
                        if cluster_id in vm_type["clusters"]]

        vm_types.sort(key=itemgetter("label"))
        for vm_type in vm_types:
            vm_type["clusters"].sort()

        return vm_types
