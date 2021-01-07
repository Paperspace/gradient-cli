from .common import BaseRepository, ListResources
from .. import config, serializers


class ListWorkflows(ListResources):
    def get_request_url(self, **kwargs):
        return "/workflows"

class ListWorkflowRuns(ListResources):
    def get_request_url(self, **kwargs):
        return "/workflows/{}/runs".format(kwargs.get("workflow_id"))
