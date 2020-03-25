from gradient.api_sdk import config, serializers
from gradient.api_sdk.repositories.common import ListResources


class ListMachineTypes(ListResources):
    SERIALIZER_CLS = serializers.VmTypeSchema

    def get_request_url(self, **kwargs):
        return "vmTypes/getVmTypesByClusters"

    def _get_api_url(self, **kwargs):
        return config.config.CONFIG_HOST

    def _get_instance_dicts(self, data, clusters_ids=None, **kwargs):
        vm_types_dicts = {}  # vmType["label"]: vmType dict
        for cluster_list_of_vms in data.values():
            cluster_id = cluster_list_of_vms[0]["clusters"][0]["id"]
            if clusters_ids and cluster_id not in clusters_ids:
                continue

            for vm in cluster_list_of_vms:
                vm_type = vm["vmType"]
                vm_type_label = vm_type["label"]
                if vm_type_label not in vm_types_dicts:
                    vm_types_dicts[vm_type_label] = vm_type

                vm_types_dicts[vm_type_label].setdefault("clusters", []).append(cluster_id)

        vm_types = list(vm_types_dicts.values())
        return vm_types
