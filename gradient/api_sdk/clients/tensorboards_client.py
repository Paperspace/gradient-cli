"""
Tensorboard logic related client handler.

Remember that in code snippets all highlighted lines are required other lines are optional.
"""
from .base_client import BaseClient
from .. import repositories, models


class TensorboardClient(BaseClient):
    """
    Client to handle tensorboard related actions.

    How to create instance of tensorboard client:

    .. code-block:: python
        :linenos:
        :emphasize-lines: 4

        from gradient import TensorboardClient

        tb_client = TensorboardClient(
            api_key='your_api_key_here'
        )

    """

    def create(
            self,
            image=None,
            username=None,
            password=None,
            instance_type=None,
            instance_size=None,
            instances_count=None,
            experiments=None,
    ):
        """
        Method to create tensorboard in paperspace gradient.

        Example create tensorboard:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            tb_id = tb_client.create(
                experiments=['some_experiment_id'],
                image='tensorflow/tensorflow:latest-py3',
                username='your_username',
                password='your_password',
                instance_type='cpu',
                instance_size='small',
                instance_count=1
            )

        :param str image: your tensorboard will run with this image.
            By default it will be run with ``tensorflow/tensorflow:latest-py3``
        :param str username: if you wish to limit access to your tensorboard with base auth then provide username
        :param str password: if you wish to limit access to your tensorboard with base auth then provide password
        :param str instance_type: type of instance on which you want to run tensorboard.
            Available choices:

            .. code-block::

                cpu
                gpu

            By default we use ``cpu`` instance type.
        :param str instance_size: size of instance on which you want to run tensorboard.
            Available choices:

            .. code-block::

                small
                medium
                large

            By default we use ``small`` instance size.
        :param int instances_count: on how many machines you want to run tensorboard. By default ``1`` is used.
        :param list experiments: list of experiments that you wish to add to tensorboard.
            To create tensorboard you need to provide at least one experiment id. This field is **required**.

        :return: Return tensorboard id
        :rtype: str

        :raises: ResourceFetchingError: When there is problem with response from API
        """
        tensorboard = models.Tensorboard(
            image=image,
            username=username,
            password=password,
            instance=models.Instance(
                type=instance_type,
                size=instance_size,
                count=instances_count,
            ),
            experiments=experiments,
        )

        repository = self.build_repository(repositories.CreateTensorboard)
        tensorboard_id = repository.create(tensorboard)
        return tensorboard_id

    def get(self, id):
        """
        Method to get tensorboard details.

        Example get tensorboard details:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            tb = tb_client.get(
                id='your_tb_id'
            )

        :param str id: Tensorboard id of which you want to get details
        :return: Tensorbord object if found
        :rtype: None|Tensorboard

        :raises: ResourceFetchingError: When there is problem with response from API
        """
        repository = self.build_repository(repositories.GetTensorboard)
        tensorboard = repository.get(id=id)
        return tensorboard

    def list(self):
        """
        Method to list your active tensorboards.

        Example usage:

        .. code-block:: python
            :linenos:

            tb_list = tb_client.list()

        :return: list of active tensorboards
        :rtype: list[models.Tensorboard]

        :raises: ResourceFetchingError: When there is problem with response from API
        """
        repository = self.build_repository(repositories.ListTensorboards)
        tensorboards = repository.list()
        return tensorboards

    def add_experiments(self, id, added_experiments):
        """
        Method to add experiments to existing tensorboard.

        Example usage:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2, 3

            tb = tb_client.add_experiments(
                id='your_tb_id',
                added_experiments=['new_experiment_id', 'next_new_experiment_id']
            )

        :param str id: tensorboard id to which you want to add experiments
        :param list added_experiments: list of experiment ids which you want to add to tensroboard

        :return: updated tensorboard
        :rtype: Tensorboard

        :raises: ResourceFetchingError: When there is problem with response from API
        """
        repository = self.build_repository(repositories.UpdateTensorboard)
        tensorboard = repository.update(id=id, added_experiments=added_experiments)
        return tensorboard

    def remove_experiments(self, id, removed_experiments):
        """
        Method to remove experiments from existing tensorboard.

        Example usage:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2, 3

            tb = tb_client.remove_experiments(
                id='your_tb_id',
                removed_experiments=['experiment_id', 'next_experiment_id']
            )

        :param str id: tensorboard id from which you want to remove experiments
        :param list removed_experiments: list of experiment ids which you want to remove from tensroboard

        :return: updated tensorboard
        :rtype: Tensorboard

        :raises: ResourceFetchingError: When there is problem with response from API
        """
        repository = self.build_repository(repositories.UpdateTensorboard)
        tensorboard = repository.update(id=id, removed_experiments=removed_experiments)
        return tensorboard

    def delete(self, id):
        """
        Method to delete tensorboard.

        Example usage:

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            tb_client.delete(
                id='your_tb_id'
            )

        :param str id: Tensoboard id which you want to delete
        """
        repository = self.build_repository(repositories.DeleteTensorboard)
        repository.delete(id_=id)
